# Getting Started with Control Deck

This guide will help you create your first Control Deck application.

## Prerequisites

### Linux (Fedora/RHEL)
```bash
sudo dnf install python3-gobject gtk4 libadwaita
```

### Linux (Ubuntu/Debian)
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 libadwaita-1-0
```

### Windows
1. Install [MSYS2](https://www.msys2.org/)
2. Run in MSYS2 terminal:
```bash
pacman -S mingw-w64-x86_64-gtk4 mingw-w64-x86_64-libadwaita mingw-w64-x86_64-python-gobject
```

### macOS
```bash
brew install gtk4 libadwaita pygobject3
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/arealicehole/control-deck.git
cd control-deck
```

2. Make scripts executable:
```bash
chmod +x *.py
```

## Your First Control Deck

### Option 1: Minimal Example

Create a file `my-deck.py`:

```python
#!/usr/bin/env python3
from control_deck import ControlDeck, DeckConfig, ServiceModule

class HelloService(ServiceModule):
    def get_name(self):
        return "Hello Service"
    
    def get_id(self):
        return "hello"
    
    def check_status(self):
        # Check if your service is running
        return True
    
    def start(self):
        # Start your service
        print("Starting Hello Service")
        return True
    
    def stop(self):
        # Stop your service
        print("Stopping Hello Service")
        return True

# Create and run
deck = ControlDeck(DeckConfig(title="My First Deck"))
deck.add_module(HelloService())
deck.run()
```

Run it:
```bash
python3 my-deck.py
```

### Option 2: Using Plugins

1. Create a plugin file `plugins/my_service.py`:

```python
"""My custom service plugin"""

__plugin_name__ = "My Service"
__description__ = "Controls my custom service"
__author__ = "Your Name"
__version__ = "1.0"

from control_deck import ServiceModule
import subprocess

class MyServiceModule(ServiceModule):
    def get_name(self):
        return "My Service"
    
    def get_id(self):
        return "my-service"
    
    def check_status(self):
        # Example: Check if a process is running
        try:
            result = subprocess.run(["pgrep", "my-service"], 
                                  capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def start(self):
        try:
            subprocess.run(["systemctl", "--user", "start", "my-service"])
            return True
        except:
            return False
    
    def stop(self):
        try:
            subprocess.run(["systemctl", "--user", "stop", "my-service"])
            return True
        except:
            return False
    
    def get_details(self):
        return "Custom service details"
```

2. Create your deck app:

```python
#!/usr/bin/env python3
from control_deck import ControlDeck, DeckConfig
from pathlib import Path

# Configure
config = DeckConfig(
    title="My Services",
    width=500,
    height=400,
    dark_mode=True
)

# Create deck
deck = ControlDeck(config)

# Load plugins automatically
plugin_dir = Path(__file__).parent / "plugins"
deck.load_plugins_from_directory(plugin_dir)

# Run
deck.run()
```

## Using Pre-built Examples

The repository includes example implementations:

### Voice Services Control
```bash
./voice-deck.py
```
Controls:
- Whisper AI transcription (Docker)
- Vocoder push-to-talk (systemd)

### Docker Container Manager
```bash
./docker-deck.py
```
Auto-discovers and manages all Docker containers.

## Project Structure

After setup, your project should look like:

```
control-deck/
├── control_deck.py       # Framework (don't modify)
├── my-deck.py           # Your app
├── plugins/             # Service modules
│   ├── my_service.py
│   └── another_service.py
└── docs/                # Documentation
```

## Next Steps

- Learn [Plugin Development](plugin-development.md)
- Explore [Configuration Options](configuration.md)
- Try [Custom Theming](theming.md)
- Use the [Plugin Manager](plugin-manager.md)

## Common Issues

### "No module named 'gi'"
You need to install Python GObject bindings. See Prerequisites above.

### "Namespace Gtk not available"
GTK4 is not installed. Install `gtk4` package for your system.

### "Namespace Adw not available"
libadwaita is not installed. Install `libadwaita` package.

### Services don't show up
- Check that plugin files are in the `plugins/` directory
- Ensure plugin files don't start with underscore (`_`)
- Verify the plugin has a class extending `ServiceModule`

## Getting Help

- Check [Troubleshooting](troubleshooting.md)
- Review [API Reference](api-reference.md)
- See [Examples](examples.md)