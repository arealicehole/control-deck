#!/usr/bin/env python3
"""
Cross-Platform Deck - Works on Linux, Windows, macOS
"""

import sys
import platform
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from control_deck import ControlDeck, DeckConfig

def main():
    config = DeckConfig(
        title=f"Control Deck ({platform.system()})",
        app_id="com.control.deck.universal",
        width=500,
        height=400
    )
    
    deck = ControlDeck(config)
    
    # Load platform-specific plugins
    system = platform.system()
    
    if system == "Linux":
        from plugins.voice_services import WhisperModule, VocoderModule
        deck.add_module(WhisperModule())
        deck.add_module(VocoderModule())
        
    elif system == "Windows":
        from plugins.windows_services import (
            WindowsDockerService,
            WindowsSSHService,
            WindowsDefenderService
        )
        deck.add_module(WindowsDockerService())
        deck.add_module(WindowsSSHService())
        deck.add_module(WindowsDefenderService())
        
    elif system == "Darwin":  # macOS
        # Add macOS services here
        pass
    
    # Docker works everywhere
    from plugins.docker_dynamic import get_docker_containers
    for container in get_docker_containers():
        deck.add_module(container)
    
    deck.run()

if __name__ == "__main__":
    main()