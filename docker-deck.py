#!/usr/bin/env python3
"""
Docker Deck - Docker containers control panel
Using Control Deck framework with Docker theming
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from control_deck import ControlDeck, DeckConfig
from plugins.docker_dynamic import get_docker_containers

# Docker blue theme CSS
DOCKER_CSS = """
@define-color docker_blue #0db7ed;
@define-color docker_dark #002c66;
@define-color docker_darker #001833;

window {
    background-color: @docker_darker;
}

headerbar {
    background-color: @docker_dark;
    color: @docker_blue;
}

.suggested-action {
    background-color: @docker_blue;
    color: white;
}

switch:checked {
    background-color: @docker_blue;
}

.success {
    color: @docker_blue;
}

frame {
    background-color: rgba(13, 183, 237, 0.05);
    border: 1px solid rgba(13, 183, 237, 0.2);
}

frame:hover {
    background-color: rgba(13, 183, 237, 0.1);
    border: 1px solid rgba(13, 183, 237, 0.3);
}
"""

def main():
    config = DeckConfig(
        title="🐳 Docker Deck",
        app_id="com.docker.deck",
        width=600,
        height=500,
        refresh_interval=10,
        dark_mode=True,
        css=DOCKER_CSS
    )
    
    # Create deck and load all Docker containers
    deck = ControlDeck(config)
    
    # Get all containers dynamically
    for container in get_docker_containers(include_stopped=True):
        deck.add_module(container)
    
    deck.run()

if __name__ == "__main__":
    main()