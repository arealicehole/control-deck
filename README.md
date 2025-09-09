# Control Deck 🎛️

Universal service control panel framework for GTK4/Adwaita.

## Features

- 🧩 **Plugin Architecture** - Extend with custom service modules
- 🎨 **Themeable** - Custom CSS support, dark mode
- 🔄 **Auto-refresh** - Configurable refresh intervals
- 📦 **Modular** - Single framework, multiple apps

## Quick Start

### Voice Services Control
```bash
./voice-deck.py
```

### Docker Container Manager
```bash
./docker-deck.py
```

## Architecture

```
control-deck/
├── control_deck.py      # Core framework
├── plugins/              # Service modules
│   ├── voice_services.py
│   └── docker_dynamic.py
├── voice-deck.py        # Voice app
└── docker-deck.py       # Docker app
```

## Creating a Custom Deck

```python
from control_deck import ControlDeck, DeckConfig, ServiceModule

class MyService(ServiceModule):
    def get_name(self) -> str:
        return "My Service"
    
    def get_id(self) -> str:
        return "my-service"
    
    def check_status(self) -> bool:
        # Check if running
        return True
    
    def start(self) -> bool:
        # Start service
        return True
    
    def stop(self) -> bool:
        # Stop service
        return True

# Create deck
config = DeckConfig(title="My Deck")
deck = ControlDeck(config)
deck.add_module(MyService())
deck.run()
```

## Plugin Development

Create a new file in `plugins/` extending `ServiceModule`:

```python
from control_deck import ServiceModule

class CustomModule(ServiceModule):
    # Implement required methods
    pass
```

## Requirements

- Python 3.9+
- GTK4 and libadwaita
- Service-specific requirements (Docker, systemd, etc.)

## Installation

```bash
# Make scripts executable
chmod +x *.py

# Install dependencies (Fedora)
sudo dnf install python3-gobject gtk4 libadwaita
```

## Examples

### Voice Deck
Controls voice transcription services:
- Whisper AI (Docker container)
- Vocoder (systemd service)

### Docker Deck  
Auto-discovers and manages all Docker containers with:
- Start/Stop/Restart controls
- Docker blue theming
- Container removal

## License

MIT