# Control Deck 🎛️

A lightweight, extensible service control panel framework for GTK4/Adwaita.

## What It Is

Control Deck is just the **shell** - a framework for building control panels. You add your own service modules as plugins.

## Quick Start

```python
#!/usr/bin/env python3
from control_deck import ControlDeck, DeckConfig, ServiceModule

# Define your service
class MyService(ServiceModule):
    def get_name(self) -> str:
        return "My Service"
    
    def get_id(self) -> str:
        return "my-service"
    
    def check_status(self) -> bool:
        # Your logic here
        return True
    
    def start(self) -> bool:
        # Your logic here
        return True
    
    def stop(self) -> bool:
        # Your logic here
        return True

# Create and run
deck = ControlDeck(DeckConfig(title="My Control Panel"))
deck.add_module(MyService())
deck.run()
```

## Features

- 🎨 **Themeable** - Custom CSS, dark mode support
- 🔌 **Plugin-based** - Drop Python files in `plugins/` 
- 🔄 **Auto-refresh** - Configurable intervals
- 🧩 **Simple API** - Just implement 5 methods

## Project Structure

```
control-deck/
├── control_deck.py    # The framework (this is all you need)
├── plugins/           # Your service modules go here
└── examples/          # Example implementations
    ├── docker-deck.py
    ├── voice-deck.py
    └── plugins/
        ├── docker_dynamic.py
        ├── voice_services.py
        └── windows_services.py
```

## Creating a Service Module

Extend `ServiceModule` and implement:
- `get_name()` - Display name
- `get_id()` - Unique identifier  
- `check_status()` - Is it running?
- `start()` - Start the service
- `stop()` - Stop the service

Optional:
- `get_details()` - Status details
- `get_icon()` - Icon name
- `restart()` - Restart logic
- `can_remove()` / `remove()` - Removal support

## Configuration

```python
DeckConfig(
    title="My Deck",          # Window title
    app_id="com.mydeck",      # App ID
    width=500,                # Window width
    height=400,               # Window height
    refresh_interval=10,      # Auto-refresh seconds
    dark_mode=True,          # Force dark mode
    css="..."                # Custom CSS
)
```

## Requirements

- Python 3.9+
- GTK4 and libadwaita
- Any additional requirements for your services

## Installation

```bash
# Install dependencies (Fedora/RHEL)
sudo dnf install python3-gobject gtk4 libadwaita

# Install dependencies (Ubuntu/Debian)
sudo apt install python3-gi gtk4 libadwaita-1-0

# Install dependencies (Windows via MSYS2)
pacman -S mingw-w64-x86_64-gtk4 mingw-w64-x86_64-python-gobject
```

## License

MIT - Use it for anything!