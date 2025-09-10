# Examples

Complete, working examples for Control Deck applications and plugins.

## Basic Examples

### Minimal Application

```python
#!/usr/bin/env python3
"""Minimal Control Deck application"""

from control_deck import ControlDeck, ServiceModule

class HelloWorld(ServiceModule):
    def get_name(self):
        return "Hello World"
    
    def get_id(self):
        return "hello"
    
    def check_status(self):
        return False
    
    def start(self):
        print("Hello, World!")
        return True
    
    def stop(self):
        print("Goodbye, World!")
        return True

# Create and run
deck = ControlDeck()
deck.add_module(HelloWorld())
deck.run()
```

### With Configuration

```python
#!/usr/bin/env python3
"""Configured deck with custom settings"""

from control_deck import ControlDeck, DeckConfig, ServiceModule

config = DeckConfig(
    title="My Custom Deck",
    width=700,
    height=500,
    dark_mode=True,
    refresh_interval=3
)

class ConfiguredService(ServiceModule):
    def __init__(self):
        self.running = False
    
    def get_name(self):
        return "Configured Service"
    
    def get_id(self):
        return "configured"
    
    def check_status(self):
        return self.running
    
    def start(self):
        self.running = True
        return True
    
    def stop(self):
        self.running = False
        return True
    
    def get_details(self):
        return "Custom configuration example"

deck = ControlDeck(config)
deck.add_module(ConfiguredService())
deck.run()
```

## Service Plugins

### System Service Manager

```python
"""System service plugin for systemd services"""

__plugin_name__ = "System Services"
__description__ = "Manage systemd services"
__author__ = "Control Deck Team"
__version__ = "1.0.0"

from control_deck import ServiceModule
import subprocess
from typing import List

class SystemdService(ServiceModule):
    def __init__(self, service_name: str, use_user: bool = False):
        self.service_name = service_name
        self.use_user = use_user
        self.systemctl = ["systemctl", "--user"] if use_user else ["systemctl"]
    
    def get_name(self):
        return self.service_name.replace(".service", "").title()
    
    def get_id(self):
        return f"systemd-{self.service_name}"
    
    def check_status(self):
        try:
            result = subprocess.run(
                [*self.systemctl, "is-active", self.service_name],
                capture_output=True,
                text=True
            )
            return result.stdout.strip() == "active"
        except:
            return False
    
    def start(self):
        try:
            subprocess.run(
                [*self.systemctl, "start", self.service_name],
                check=True
            )
            return True
        except:
            return False
    
    def stop(self):
        try:
            subprocess.run(
                [*self.systemctl, "stop", self.service_name],
                check=True
            )
            return True
        except:
            return False
    
    def restart(self):
        try:
            subprocess.run(
                [*self.systemctl, "restart", self.service_name],
                check=True
            )
            return True
        except:
            return False
    
    def get_details(self):
        try:
            result = subprocess.run(
                [*self.systemctl, "status", self.service_name],
                capture_output=True,
                text=True
            )
            # Extract relevant line from status output
            for line in result.stdout.split('\n'):
                if "Active:" in line:
                    return line.strip()
            return ""
        except:
            return "Status unavailable"
    
    def get_icon(self):
        return "application-x-executable-symbolic"

# Factory function to create multiple services
def get_services() -> List[ServiceModule]:
    """Return configured system services"""
    services = [
        # System services
        SystemdService("docker.service"),
        SystemdService("nginx.service"),
        SystemdService("postgresql.service"),
        
        # User services
        SystemdService("syncthing.service", use_user=True),
        SystemdService("podman.service", use_user=True),
    ]
    return [s for s in services if _service_exists(s.service_name)]

def _service_exists(service_name: str) -> bool:
    """Check if a systemd service exists"""
    try:
        result = subprocess.run(
            ["systemctl", "list-unit-files", service_name],
            capture_output=True,
            text=True
        )
        return service_name in result.stdout
    except:
        return False
```

### Docker Container Manager

```python
"""Docker container management plugin"""

__plugin_name__ = "Docker Containers"
__description__ = "Manage Docker containers dynamically"
__author__ = "Control Deck Team"
__version__ = "2.0.0"

from control_deck import ServiceModule
import subprocess
import json
from typing import List, Optional

class DockerContainer(ServiceModule):
    def __init__(self, container_data: dict):
        self.data = container_data
        self.container_id = container_data.get("ID", "")[:12]
        self.container_name = container_data.get("Names", "unknown")
        self.image = container_data.get("Image", "unknown")
        self.state = container_data.get("State", "unknown")
        self.status = container_data.get("Status", "")
    
    def get_name(self):
        return f"🐳 {self.container_name}"
    
    def get_id(self):
        return f"docker-{self.container_id}"
    
    def check_status(self):
        return self.state.lower() == "running"
    
    def start(self):
        try:
            subprocess.run(
                ["docker", "start", self.container_id],
                check=True,
                capture_output=True
            )
            self.state = "running"
            return True
        except:
            return False
    
    def stop(self):
        try:
            subprocess.run(
                ["docker", "stop", self.container_id],
                check=True,
                capture_output=True
            )
            self.state = "exited"
            return True
        except:
            return False
    
    def restart(self):
        try:
            subprocess.run(
                ["docker", "restart", self.container_id],
                check=True,
                capture_output=True
            )
            return True
        except:
            return False
    
    def can_remove(self):
        return self.state.lower() != "running"
    
    def remove(self):
        if not self.can_remove():
            return False
        try:
            subprocess.run(
                ["docker", "rm", self.container_id],
                check=True,
                capture_output=True
            )
            return True
        except:
            return False
    
    def get_details(self):
        details = [f"Image: {self.image}"]
        if self.status:
            details.append(f"Status: {self.status}")
        
        # Get port mappings
        try:
            result = subprocess.run(
                ["docker", "port", self.container_id],
                capture_output=True,
                text=True
            )
            if result.stdout.strip():
                details.append(f"Ports: {result.stdout.strip()}")
        except:
            pass
        
        return " • ".join(details)
    
    def get_icon(self):
        if self.check_status():
            return "media-playback-start-symbolic"
        return "media-playback-stop-symbolic"

def get_docker_containers() -> List[ServiceModule]:
    """Factory function to get all Docker containers"""
    try:
        # Check if Docker is running
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        
        # Get all containers
        result = subprocess.run(
            ["docker", "ps", "-a", "--format", "json"],
            capture_output=True,
            text=True
        )
        
        containers = []
        for line in result.stdout.strip().split('\n'):
            if line:
                data = json.loads(line)
                containers.append(DockerContainer(data))
        
        return containers
    except:
        return []

# Export the factory function
get_services = get_docker_containers
```

### Network Services Monitor

```python
"""Network services monitoring plugin"""

__plugin_name__ = "Network Monitor"
__description__ = "Monitor network services and ports"
__author__ = "Control Deck Team"
__version__ = "1.2.0"

from control_deck import ServiceModule
import socket
import subprocess
from typing import Optional

class NetworkService(ServiceModule):
    def __init__(self, name: str, host: str, port: int, 
                 start_cmd: Optional[str] = None,
                 stop_cmd: Optional[str] = None):
        self.service_name = name
        self.host = host
        self.port = port
        self.start_cmd = start_cmd
        self.stop_cmd = stop_cmd
        self.last_response_time = None
    
    def get_name(self):
        return self.service_name
    
    def get_id(self):
        return f"net-{self.service_name.lower().replace(' ', '-')}"
    
    def check_status(self):
        """Check if service is reachable"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.host, self.port))
            sock.close()
            return result == 0
        except:
            return False
    
    def start(self):
        if not self.start_cmd:
            return False
        try:
            subprocess.run(self.start_cmd, shell=True, check=True)
            return True
        except:
            return False
    
    def stop(self):
        if not self.stop_cmd:
            return False
        try:
            subprocess.run(self.stop_cmd, shell=True, check=True)
            return True
        except:
            return False
    
    def get_details(self):
        details = [f"{self.host}:{self.port}"]
        
        # Check response time
        if self.check_status():
            import time
            start = time.time()
            self.check_status()
            response_time = (time.time() - start) * 1000
            details.append(f"Response: {response_time:.0f}ms")
        
        return " • ".join(details)
    
    def get_icon(self):
        return "network-server-symbolic"

# Define services to monitor
def get_services():
    return [
        NetworkService(
            "Web Server",
            "localhost",
            80,
            "sudo systemctl start nginx",
            "sudo systemctl stop nginx"
        ),
        NetworkService(
            "Database",
            "localhost",
            5432,
            "sudo systemctl start postgresql",
            "sudo systemctl stop postgresql"
        ),
        NetworkService(
            "Redis Cache",
            "localhost",
            6379,
            "sudo systemctl start redis",
            "sudo systemctl stop redis"
        ),
        NetworkService(
            "SSH Server",
            "localhost",
            22
        ),
        NetworkService(
            "API Gateway",
            "localhost",
            8080
        )
    ]
```

## Complete Applications

### Development Environment Manager

```python
#!/usr/bin/env python3
"""Development environment control deck"""

from control_deck import ControlDeck, DeckConfig, ServiceModule
import subprocess
import os
from pathlib import Path

class DevService(ServiceModule):
    """Base class for development services"""
    
    def __init__(self, name: str, check_cmd: str, 
                 start_cmd: str, stop_cmd: str):
        self.name = name
        self.check_cmd = check_cmd
        self.start_cmd = start_cmd
        self.stop_cmd = stop_cmd
    
    def get_name(self):
        return self.name
    
    def get_id(self):
        return self.name.lower().replace(" ", "-")
    
    def check_status(self):
        try:
            result = subprocess.run(
                self.check_cmd,
                shell=True,
                capture_output=True
            )
            return result.returncode == 0
        except:
            return False
    
    def start(self):
        try:
            subprocess.Popen(
                self.start_cmd,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except:
            return False
    
    def stop(self):
        try:
            subprocess.run(
                self.stop_cmd,
                shell=True,
                check=True
            )
            return True
        except:
            return False

class NodeProject(DevService):
    """Node.js project service"""
    
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.project_name = project_path.name
        
        super().__init__(
            name=f"Node: {self.project_name}",
            check_cmd=f"pgrep -f 'node.*{project_path}'",
            start_cmd=f"cd {project_path} && npm start",
            stop_cmd=f"pkill -f 'node.*{project_path}'"
        )
    
    def get_details(self):
        package_json = self.project_path / "package.json"
        if package_json.exists():
            import json
            with open(package_json) as f:
                data = json.load(f)
                version = data.get("version", "unknown")
                return f"v{version} • {self.project_path}"
        return str(self.project_path)
    
    def get_icon(self):
        return "application-x-javascript-symbolic"

class DockerCompose(DevService):
    """Docker Compose stack"""
    
    def __init__(self, compose_path: Path):
        self.compose_path = compose_path
        self.stack_name = compose_path.parent.name
        
        super().__init__(
            name=f"Stack: {self.stack_name}",
            check_cmd=f"cd {compose_path.parent} && docker-compose ps --services --filter status=running | grep -q .",
            start_cmd=f"cd {compose_path.parent} && docker-compose up -d",
            stop_cmd=f"cd {compose_path.parent} && docker-compose down"
        )
    
    def get_details(self):
        try:
            result = subprocess.run(
                f"cd {self.compose_path.parent} && docker-compose ps --services",
                shell=True,
                capture_output=True,
                text=True
            )
            services = result.stdout.strip().split('\n')
            return f"{len(services)} services"
        except:
            return "Status unknown"
    
    def restart(self):
        try:
            subprocess.run(
                f"cd {self.compose_path.parent} && docker-compose restart",
                shell=True,
                check=True
            )
            return True
        except:
            return False

class DatabaseServer(DevService):
    """Database server management"""
    
    def __init__(self, db_type: str, port: int):
        self.db_type = db_type
        self.port = port
        
        commands = {
            "postgresql": {
                "check": "pg_isready -p {}",
                "start": "pg_ctl start -D /var/lib/postgresql/data",
                "stop": "pg_ctl stop -D /var/lib/postgresql/data"
            },
            "mysql": {
                "check": "mysqladmin ping -h localhost -P {}",
                "start": "systemctl start mysql",
                "stop": "systemctl stop mysql"
            },
            "mongodb": {
                "check": "mongosh --port {} --eval 'db.runCommand({{ping: 1}})'",
                "start": "mongod --fork --logpath /var/log/mongodb.log",
                "stop": "mongosh --eval 'db.shutdownServer()'"
            }
        }
        
        cmds = commands.get(db_type, commands["postgresql"])
        
        super().__init__(
            name=f"{db_type.title()} Database",
            check_cmd=cmds["check"].format(port),
            start_cmd=cmds["start"],
            stop_cmd=cmds["stop"]
        )
    
    def get_details(self):
        return f"Port {self.port}"
    
    def get_icon(self):
        return "network-server-symbolic"

# Main application
def main():
    # Configure deck
    config = DeckConfig(
        title="Development Environment",
        width=800,
        height=600,
        dark_mode=True,
        refresh_interval=5
    )
    
    # Create deck
    deck = ControlDeck(config)
    
    # Auto-discover Node projects
    projects_dir = Path.home() / "projects"
    for package_json in projects_dir.glob("*/package.json"):
        deck.add_module(NodeProject(package_json.parent))
    
    # Auto-discover Docker Compose stacks
    for compose_file in projects_dir.glob("*/docker-compose.yml"):
        deck.add_module(DockerCompose(compose_file))
    
    # Add database servers
    deck.add_module(DatabaseServer("postgresql", 5432))
    deck.add_module(DatabaseServer("mysql", 3306))
    deck.add_module(DatabaseServer("mongodb", 27017))
    
    # Run
    deck.run()

if __name__ == "__main__":
    main()
```

### Multi-Tab Service Manager

```python
#!/usr/bin/env python3
"""Multi-tab deck with service categories"""

from control_deck import ControlDeck, DeckConfig, ServiceModule
from gi.repository import Gtk, Adw
from typing import Dict, List

class TabbedDeck(ControlDeck):
    """Extended deck with tabbed interface"""
    
    def __init__(self, config: DeckConfig):
        super().__init__(config)
        self.tabs: Dict[str, List[ServiceModule]] = {}
    
    def add_tab(self, name: str, modules: List[ServiceModule]):
        """Add a tab with modules"""
        self.tabs[name] = modules
        for module in modules:
            self.add_module(module)
    
    def build_ui(self):
        """Override to build tabbed interface"""
        # Create notebook for tabs
        notebook = Gtk.Notebook()
        notebook.set_scrollable(True)
        
        for tab_name, modules in self.tabs.items():
            # Create page for this tab
            page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            
            # Add modules to page
            for module in modules:
                card = self.create_service_card(module)
                page.append(card)
            
            # Add page to notebook
            label = Gtk.Label(label=tab_name)
            notebook.append_page(page, label)
        
        # Add notebook to window
        self.window.set_content(notebook)

# Usage
def main():
    config = DeckConfig(
        title="Service Control Center",
        width=900,
        height=600
    )
    
    deck = TabbedDeck(config)
    
    # Web Services tab
    web_services = [
        SystemdService("nginx"),
        SystemdService("apache2"),
        SystemdService("caddy")
    ]
    deck.add_tab("Web Servers", web_services)
    
    # Database tab
    databases = [
        DatabaseServer("postgresql", 5432),
        DatabaseServer("mysql", 3306),
        DatabaseServer("redis", 6379)
    ]
    deck.add_tab("Databases", databases)
    
    # Docker tab
    docker_services = get_docker_containers()
    deck.add_tab("Containers", docker_services)
    
    deck.run()

if __name__ == "__main__":
    main()
```

## Advanced Patterns

### Service with Dependencies

```python
class DependentService(ServiceModule):
    """Service that depends on other services"""
    
    def __init__(self, name: str, dependencies: List[str]):
        self.name = name
        self.dependencies = dependencies
    
    def check_dependencies(self) -> bool:
        """Check if all dependencies are running"""
        for dep in self.dependencies:
            result = subprocess.run(
                ["systemctl", "is-active", dep],
                capture_output=True,
                text=True
            )
            if result.stdout.strip() != "active":
                return False
        return True
    
    def start(self):
        # Start dependencies first
        if not self.check_dependencies():
            for dep in self.dependencies:
                subprocess.run(["systemctl", "start", dep])
        
        # Then start this service
        return super().start()
    
    def get_details(self):
        if not self.check_dependencies():
            missing = [d for d in self.dependencies 
                      if not self._is_running(d)]
            return f"Missing: {', '.join(missing)}"
        return "All dependencies met"
```

### Service with Metrics

```python
class MetricsService(ServiceModule):
    """Service that collects and displays metrics"""
    
    def __init__(self):
        self.metrics = {
            "uptime": 0,
            "requests": 0,
            "errors": 0,
            "cpu_usage": 0.0,
            "memory_mb": 0
        }
    
    def update_metrics(self):
        """Update service metrics"""
        if self.check_status():
            # Get process metrics
            try:
                import psutil
                process = psutil.Process(self.get_pid())
                self.metrics["cpu_usage"] = process.cpu_percent()
                self.metrics["memory_mb"] = process.memory_info().rss / 1024 / 1024
                # Update other metrics...
            except:
                pass
    
    def get_details(self):
        self.update_metrics()
        return (f"CPU: {self.metrics['cpu_usage']:.1f}% • "
                f"RAM: {self.metrics['memory_mb']:.0f}MB • "
                f"Requests: {self.metrics['requests']}")
```

### Service with Logs

```python
class LoggingService(ServiceModule):
    """Service with log viewing capabilities"""
    
    def __init__(self, log_file: Path):
        self.log_file = log_file
    
    def get_recent_logs(self, lines: int = 10) -> str:
        """Get recent log entries"""
        if not self.log_file.exists():
            return "No logs available"
        
        try:
            result = subprocess.run(
                ["tail", "-n", str(lines), str(self.log_file)],
                capture_output=True,
                text=True
            )
            return result.stdout
        except:
            return "Error reading logs"
    
    def get_details(self):
        # Show last error from logs
        logs = self.get_recent_logs(50)
        for line in logs.split('\n'):
            if 'ERROR' in line:
                return f"Last error: {line[:50]}..."
        return "No recent errors"
```

## Testing Examples

### Unit Test for Module

```python
import unittest
from unittest.mock import patch, MagicMock

class TestServiceModule(unittest.TestCase):
    def setUp(self):
        self.module = MyServiceModule()
    
    def test_get_name(self):
        self.assertEqual(self.module.get_name(), "Expected Name")
    
    def test_get_id(self):
        self.assertIsNotNone(self.module.get_id())
        self.assertIsInstance(self.module.get_id(), str)
    
    @patch('subprocess.run')
    def test_check_status_running(self, mock_run):
        mock_run.return_value.returncode = 0
        self.assertTrue(self.module.check_status())
    
    @patch('subprocess.run')
    def test_check_status_stopped(self, mock_run):
        mock_run.return_value.returncode = 1
        self.assertFalse(self.module.check_status())
    
    @patch('subprocess.run')
    def test_start_success(self, mock_run):
        mock_run.return_value.returncode = 0
        self.assertTrue(self.module.start())
    
    @patch('subprocess.run')
    def test_start_failure(self, mock_run):
        mock_run.side_effect = Exception("Start failed")
        self.assertFalse(self.module.start())

if __name__ == '__main__':
    unittest.main()
```

### Integration Test

```python
def test_integration():
    """Test complete deck with plugins"""
    
    # Create test deck
    config = DeckConfig(title="Test Deck")
    deck = ControlDeck(config)
    
    # Load test plugins
    test_plugin_dir = Path("test_plugins")
    deck.load_plugins_from_directory(test_plugin_dir)
    
    # Verify plugins loaded
    assert len(deck.modules) > 0
    
    # Test each module
    for module in deck.modules:
        # Verify required methods exist
        assert hasattr(module, 'get_name')
        assert hasattr(module, 'check_status')
        assert hasattr(module, 'start')
        assert hasattr(module, 'stop')
        
        # Test method returns
        assert isinstance(module.get_name(), str)
        assert isinstance(module.check_status(), bool)
    
    print("All tests passed!")

if __name__ == "__main__":
    test_integration()
```

## See Also

- [Getting Started](getting-started.md)
- [Plugin Development](plugin-development.md)
- [API Reference](api-reference.md)
- [Troubleshooting](troubleshooting.md)