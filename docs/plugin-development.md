# Plugin Development Guide

Learn how to create powerful service modules for Control Deck.

## Plugin Basics

A plugin is a Python file containing one or more classes that extend `ServiceModule`.

### Minimal Plugin Structure

```python
from control_deck import ServiceModule

class MyModule(ServiceModule):
    def get_name(self) -> str:
        return "Display Name"
    
    def get_id(self) -> str:
        return "unique-id"
    
    def check_status(self) -> bool:
        return True  # or False
    
    def start(self) -> bool:
        # Start logic
        return True  # Success
    
    def stop(self) -> bool:
        # Stop logic
        return True  # Success
```

## Required Methods

### `get_name() -> str`
Returns the display name shown in the UI.

```python
def get_name(self) -> str:
    return "Docker Engine"
```

### `get_id() -> str`
Returns a unique identifier for this service.

```python
def get_id(self) -> str:
    return "docker-engine"
```

### `check_status() -> bool`
Checks if the service is currently running.

```python
def check_status(self) -> bool:
    try:
        subprocess.run(["docker", "info"], check=True, capture_output=True)
        return True
    except:
        return False
```

### `start() -> bool`
Starts the service. Return `True` on success.

```python
def start(self) -> bool:
    try:
        subprocess.run(["systemctl", "start", "docker"], check=True)
        return True
    except:
        return False
```

### `stop() -> bool`
Stops the service. Return `True` on success.

```python
def stop(self) -> bool:
    try:
        subprocess.run(["systemctl", "stop", "docker"], check=True)
        return True
    except:
        return False
```

## Optional Methods

### `get_details() -> str`
Provides additional status information.

```python
def get_details(self) -> str:
    if self.check_status():
        return "Port 8080 • 4 connections"
    return "Service stopped"
```

### `get_icon() -> Optional[str]`
Returns a GTK icon name.

```python
def get_icon(self) -> Optional[str]:
    return "network-server-symbolic"
```

Common icons:
- `"application-x-addon-symbolic"` - Generic service
- `"network-server-symbolic"` - Server/network service
- `"folder-remote-symbolic"` - Remote/cloud service
- `"media-playback-start-symbolic"` - Media service
- `"system-run-symbolic"` - System service

### `restart() -> bool`
Custom restart logic (default: stop then start).

```python
def restart(self) -> bool:
    try:
        subprocess.run(["systemctl", "restart", "myservice"], check=True)
        return True
    except:
        return False
```

### `can_remove() -> bool` and `remove() -> bool`
For removable services (like Docker containers).

```python
def can_remove(self) -> bool:
    return not self.check_status()  # Can remove if stopped

def remove(self) -> bool:
    try:
        subprocess.run(["docker", "rm", self.container_id], check=True)
        return True
    except:
        return False
```

## Plugin Metadata

Add metadata for better plugin manager display:

```python
"""My Service Plugin"""

__plugin_name__ = "My Service Manager"
__description__ = "Manages the My Service daemon and related processes"
__author__ = "Your Name"
__version__ = "2.0.1"
```

## Advanced Patterns

### Dynamic Service Discovery

Create multiple modules from one plugin:

```python
def get_docker_containers():
    """Factory function to create modules"""
    modules = []
    result = subprocess.run(["docker", "ps", "-a", "--format", "json"],
                          capture_output=True, text=True)
    
    for line in result.stdout.strip().split('\n'):
        if line:
            data = json.loads(line)
            modules.append(DockerContainerModule(data))
    
    return modules
```

### Stateful Services

Store state in the module:

```python
class StatefulModule(ServiceModule):
    def __init__(self):
        self.start_time = None
        self.connection_count = 0
    
    def start(self) -> bool:
        if super().start():
            self.start_time = datetime.now()
            return True
        return False
    
    def get_details(self) -> str:
        if self.start_time:
            uptime = datetime.now() - self.start_time
            return f"Uptime: {uptime}, Connections: {self.connection_count}"
        return "Not started"
```

### Async Operations

For long-running operations:

```python
import threading

class AsyncModule(ServiceModule):
    def start(self) -> bool:
        # Start async operation
        thread = threading.Thread(target=self._long_start)
        thread.daemon = True
        thread.start()
        return True  # Return immediately
    
    def _long_start(self):
        # Long operation here
        time.sleep(5)
        # Update internal state when done
```

### Configuration Support

Read from config files:

```python
import configparser

class ConfigurableModule(ServiceModule):
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('~/.config/myservice/config.ini')
    
    def get_name(self) -> str:
        return self.config.get('service', 'name', fallback='My Service')
```

## Best Practices

### 1. Error Handling
Always handle exceptions gracefully:

```python
def check_status(self) -> bool:
    try:
        # Your check here
        return True
    except FileNotFoundError:
        return False  # Service not installed
    except PermissionError:
        return False  # No permission
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
```

### 2. Performance
- Cache expensive operations
- Use timeouts for subprocess calls
- Don't block the UI thread

```python
def check_status(self) -> bool:
    # Use timeout to prevent hanging
    try:
        result = subprocess.run(
            ["service", "status"],
            capture_output=True,
            timeout=2  # 2 second timeout
        )
        return "running" in result.stdout.decode()
    except subprocess.TimeoutExpired:
        return False
```

### 3. Cross-Platform Support

```python
import platform

class CrossPlatformModule(ServiceModule):
    def start(self) -> bool:
        system = platform.system()
        
        if system == "Linux":
            return self._start_linux()
        elif system == "Windows":
            return self._start_windows()
        elif system == "Darwin":
            return self._start_macos()
        
        return False
```

### 4. User Feedback

Provide meaningful details:

```python
def get_details(self) -> str:
    if not self.check_status():
        if not self._is_installed():
            return "Not installed"
        elif not self._has_permission():
            return "Permission denied"
        else:
            return "Stopped"
    
    # Running - show useful info
    return f"Port {self.port} • PID {self.pid}"
```

## Testing Your Plugin

### Manual Testing

1. Place plugin in `plugins/` directory
2. Run a test deck:

```python
#!/usr/bin/env python3
from control_deck import ControlDeck, DeckConfig
from plugins.my_plugin import MyModule

deck = ControlDeck(DeckConfig(title="Test"))
deck.add_module(MyModule())
deck.run()
```

### Unit Testing

```python
import unittest
from my_plugin import MyModule

class TestMyModule(unittest.TestCase):
    def setUp(self):
        self.module = MyModule()
    
    def test_name(self):
        self.assertEqual(self.module.get_name(), "Expected Name")
    
    def test_id_unique(self):
        self.assertIsNotNone(self.module.get_id())
    
    def test_status_returns_bool(self):
        self.assertIsInstance(self.module.check_status(), bool)
```

## Plugin Examples

See the `examples/plugins/` directory for complete examples:

- `voice_services.py` - systemd and Docker services
- `docker_dynamic.py` - Dynamic container discovery
- `windows_services.py` - Windows service control

## Publishing Your Plugin

1. Add metadata headers
2. Include a docstring
3. Handle errors gracefully
4. Test on target platforms
5. Share on GitHub or package registries

## Getting Help

- Review [API Reference](api-reference.md)
- Check [Examples](examples.md)
- See [Troubleshooting](troubleshooting.md)