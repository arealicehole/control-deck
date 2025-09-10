"""
Docker Dynamic Plugin - Auto-discovers all Docker containers
"""

__plugin_name__ = "Docker Containers"
__description__ = "Auto-discover and manage all Docker containers on the system"
__author__ = "Control Deck"
__version__ = "1.0"

import subprocess
import json
from typing import List
from control_deck import ServiceModule

class DockerContainerModule(ServiceModule):
    """Represents a single Docker container"""
    
    def __init__(self, container_data: dict):
        self.id = container_data.get('ID', '')[:12]
        self.name = container_data.get('Names', 'unknown')
        self.image = container_data.get('Image', 'unknown')
        self.status = container_data.get('Status', 'unknown')
        self.is_running = 'Up' in self.status
        self.ports = container_data.get('Ports', '')
    
    def get_name(self) -> str:
        return self.name
    
    def get_id(self) -> str:
        return f"docker-{self.id}"
    
    def get_icon(self) -> str:
        return "application-x-addon-symbolic"
    
    def check_status(self) -> bool:
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", f"name={self.name}", "--format", "{{.Status}}"],
                capture_output=True, text=True, timeout=2
            )
            return "Up" in result.stdout
        except:
            return False
    
    def start(self) -> bool:
        try:
            subprocess.run(["docker", "start", self.name], timeout=10, check=True)
            return True
        except:
            return False
    
    def stop(self) -> bool:
        try:
            subprocess.run(["docker", "stop", self.name], timeout=10, check=True)
            return True
        except:
            return False
    
    def restart(self) -> bool:
        try:
            subprocess.run(["docker", "restart", self.name], timeout=10, check=True)
            return True
        except:
            return False
    
    def get_details(self) -> str:
        details = self.image
        if self.ports:
            details += f" • {self.ports}"
        return details
    
    def can_remove(self) -> bool:
        return not self.check_status()  # Can only remove stopped containers
    
    def remove(self) -> bool:
        try:
            subprocess.run(["docker", "rm", self.name], timeout=5, check=True)
            return True
        except:
            return False

def get_docker_containers(include_stopped: bool = True) -> List[DockerContainerModule]:
    """Factory function to get all Docker containers as modules"""
    modules = []
    try:
        cmd = ["docker", "ps", "--format", "json"]
        if include_stopped:
            cmd.append("-a")
            
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        for line in result.stdout.strip().split('\n'):
            if line:
                data = json.loads(line)
                modules.append(DockerContainerModule(data))
    except Exception as e:
        print(f"Error getting containers: {e}")
    
    return modules