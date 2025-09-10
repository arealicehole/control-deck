#!/usr/bin/env python3
"""
Voice Deck - Voice services control panel
Using Control Deck framework
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from control_deck import ControlDeck, DeckConfig
from plugins.voice_services import WhisperModule, VocoderModule

def main():
    config = DeckConfig(
        title="Voice Deck",
        app_id="com.voice.deck",
        width=400,
        height=300,
        refresh_interval=5
    )
    
    # Create deck with voice modules
    deck = ControlDeck(config)
    deck.add_module(WhisperModule())
    deck.add_module(VocoderModule())
    
    deck.run()

if __name__ == "__main__":
    main()