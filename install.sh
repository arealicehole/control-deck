#!/bin/bash
# Install Control Deck apps to your system

echo "Installing Control Deck apps..."

# Create desktop files
cat > ~/.local/share/applications/voice-deck-new.desktop << EOF
[Desktop Entry]
Name=Voice Deck (New)
Comment=Voice services control panel
Exec=/home/ice/dev/control-deck/voice-deck.py
Icon=audio-input-microphone
Terminal=false
Type=Application
Categories=AudioVideo;Audio;Utility;
EOF

cat > ~/.local/share/applications/docker-deck-new.desktop << EOF
[Desktop Entry]
Name=Docker Deck (New)
Comment=Docker container manager
Exec=/home/ice/dev/control-deck/docker-deck.py
Icon=docker
Terminal=false
Type=Application
Categories=System;Development;
EOF

echo "✅ Installed! You can now find:"
echo "   - 'Voice Deck (New)' in your apps"
echo "   - 'Docker Deck (New)' in your apps"
echo ""
echo "Or run directly:"
echo "   ./voice-deck.py"
echo "   ./docker-deck.py"