"""
Voice Services Plugin - Whisper and Vocoder controls
"""

import subprocess
import json
from control_deck import ServiceModule

class WhisperModule(ServiceModule):
    """Whisper-Blackwell Docker service"""
    
    def get_name(self) -> str:
        return "Whisper AI"
    
    def get_id(self) -> str:
        return "whisper-blackwell"
    
    def get_icon(self) -> str:
        return "audio-input-microphone-symbolic"
    
    def check_status(self) -> bool:
        try:
            result = subprocess.run(
                ["docker", "ps", "--filter", "name=whisper-blackwell", "--format", "{{.Names}}"],
                capture_output=True, text=True, timeout=2
            )
            return "whisper-blackwell" in result.stdout
        except:
            return False
    
    def start(self) -> bool:
        try:
            subprocess.run(["docker", "start", "whisper-blackwell"], timeout=5)
            return True
        except:
            return False
    
    def stop(self) -> bool:
        try:
            subprocess.run(["docker", "stop", "whisper-blackwell"], timeout=5)
            return True
        except:
            return False
    
    def get_details(self) -> str:
        try:
            result = subprocess.run(
                ["curl", "-s", "http://127.0.0.1:8771/health"],
                capture_output=True, text=True, timeout=1
            )
            if result.stdout:
                data = json.loads(result.stdout)
                model = data.get('model', '?')
                gpu = data.get('gpu', {}).get('device_name', 'CPU')
                return f"Model: {model}, GPU: {gpu}"
        except:
            pass
        return "Port 8771"

class VocoderModule(ServiceModule):
    """Vocoder systemd service"""
    
    def get_name(self) -> str:
        return "Vocoder"
    
    def get_id(self) -> str:
        return "vocoder"
    
    def get_icon(self) -> str:
        return "audio-headphones-symbolic"
    
    def check_status(self) -> bool:
        try:
            result = subprocess.run(
                ["systemctl", "--user", "is-active", "vocoder.service"],
                capture_output=True, text=True, timeout=2
            )
            return result.stdout.strip() == "active"
        except:
            return False
    
    def start(self) -> bool:
        try:
            subprocess.run(["systemctl", "--user", "start", "vocoder.service"], timeout=5)
            return True
        except:
            return False
    
    def stop(self) -> bool:
        try:
            subprocess.run(["systemctl", "--user", "stop", "vocoder.service"], timeout=5)
            return True
        except:
            return False
    
    def get_details(self) -> str:
        return "Push-to-talk (Super+Space)"