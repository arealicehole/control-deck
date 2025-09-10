"""
Windows Services Plugin - Control Windows services
"""

import subprocess
import platform
from control_deck import ServiceModule

class WindowsServiceModule(ServiceModule):
    """Base class for Windows services"""
    
    def __init__(self, service_name: str, display_name: str):
        self.service_name = service_name
        self.display_name = display_name
        
    def get_name(self) -> str:
        return self.display_name
    
    def get_id(self) -> str:
        return self.service_name
    
    def check_status(self) -> bool:
        """Check if Windows service is running"""
        if platform.system() != "Windows":
            return False
        try:
            result = subprocess.run(
                ["sc", "query", self.service_name],
                capture_output=True, text=True, shell=True
            )
            return "RUNNING" in result.stdout
        except:
            return False
    
    def start(self) -> bool:
        """Start Windows service (requires admin)"""
        if platform.system() != "Windows":
            return False
        try:
            subprocess.run(
                ["net", "start", self.service_name],
                shell=True, check=True
            )
            return True
        except:
            return False
    
    def stop(self) -> bool:
        """Stop Windows service (requires admin)"""
        if platform.system() != "Windows":
            return False
        try:
            subprocess.run(
                ["net", "stop", self.service_name],
                shell=True, check=True
            )
            return True
        except:
            return False

# Example Windows services
class WindowsDockerService(WindowsServiceModule):
    def __init__(self):
        super().__init__("com.docker.service", "Docker Desktop Service")

class WindowsSSHService(WindowsServiceModule):
    def __init__(self):
        super().__init__("sshd", "OpenSSH Server")

class WindowsDefenderService(WindowsServiceModule):
    def __init__(self):
        super().__init__("WinDefend", "Windows Defender")