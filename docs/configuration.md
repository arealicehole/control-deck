# Configuration Guide

Comprehensive guide to configuring Control Deck applications.

## Configuration Methods

### 1. Code Configuration

Pass a `DeckConfig` object when creating your deck:

```python
from control_deck import ControlDeck, DeckConfig

config = DeckConfig(
    title="My Services",
    width=600,
    height=400,
    dark_mode=True,
    refresh_interval=3
)

deck = ControlDeck(config)
```

### 2. Configuration File

Create a `config.yaml` file:

```yaml
title: My Services
width: 600
height: 400
dark_mode: true
auto_refresh: true
refresh_interval: 3
show_header: true
show_status_bar: true
```

Load it in your code:

```python
import yaml
from pathlib import Path

config_path = Path("config.yaml")
if config_path.exists():
    with open(config_path) as f:
        config_data = yaml.safe_load(f)
    config = DeckConfig(**config_data)
else:
    config = DeckConfig()
```

### 3. Environment Variables

Override configuration with environment variables:

```bash
export DECK_TITLE="Production Services"
export DECK_DARK_MODE=true
export DECK_REFRESH_INTERVAL=10
```

```python
import os

config = DeckConfig(
    title=os.getenv("DECK_TITLE", "Control Deck"),
    dark_mode=os.getenv("DECK_DARK_MODE", "true").lower() == "true",
    refresh_interval=int(os.getenv("DECK_REFRESH_INTERVAL", "5"))
)
```

## Configuration Options

### Window Settings

#### `title`
- **Type:** `str`
- **Default:** `"Control Deck"`
- **Description:** Window title displayed in the title bar

#### `width`
- **Type:** `int`
- **Default:** `500`
- **Description:** Initial window width in pixels

#### `height`
- **Type:** `int`
- **Default:** `600`
- **Description:** Initial window height in pixels

#### `resizable`
- **Type:** `bool`
- **Default:** `True`
- **Description:** Whether the window can be resized

#### `start_maximized`
- **Type:** `bool`
- **Default:** `False`
- **Description:** Start with maximized window

### Theme Settings

#### `dark_mode`
- **Type:** `bool`
- **Default:** `True`
- **Description:** Enable dark theme

#### `custom_css`
- **Type:** `Optional[str]`
- **Default:** `None`
- **Description:** Path to custom CSS file

#### `icon_theme`
- **Type:** `Optional[str]`
- **Default:** `None`
- **Description:** GTK icon theme name

Example custom CSS:

```css
/* custom.css */
.service-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 16px;
    margin: 8px;
}

.service-running {
    border-left: 4px solid #10b981;
}

.service-stopped {
    border-left: 4px solid #ef4444;
}
```

### Refresh Settings

#### `auto_refresh`
- **Type:** `bool`
- **Default:** `True`
- **Description:** Enable automatic status refresh

#### `refresh_interval`
- **Type:** `int`
- **Default:** `5`
- **Description:** Seconds between automatic refreshes

#### `refresh_on_action`
- **Type:** `bool`
- **Default:** `True`
- **Description:** Refresh after start/stop actions

### UI Components

#### `show_header`
- **Type:** `bool`
- **Default:** `True`
- **Description:** Show header bar with controls

#### `show_status_bar`
- **Type:** `bool`
- **Default:** `True`
- **Description:** Show status bar at bottom

#### `show_plugin_button`
- **Type:** `bool`
- **Default:** `True`
- **Description:** Show plugin manager button

#### `show_refresh_button`
- **Type:** `bool`
- **Default:** `True`
- **Description:** Show manual refresh button

#### `compact_mode`
- **Type:** `bool`
- **Default:** `False`
- **Description:** Use compact card layout

### Plugin Settings

#### `plugin_directory`
- **Type:** `Optional[Path]`
- **Default:** `"plugins"`
- **Description:** Directory to load plugins from

#### `auto_load_plugins`
- **Type:** `bool`
- **Default:** `True`
- **Description:** Automatically load plugins on startup

#### `plugin_filter`
- **Type:** `Optional[List[str]]`
- **Default:** `None`
- **Description:** Only load specific plugins by filename

Example:

```python
config = DeckConfig(
    plugin_directory=Path("/usr/share/control-deck/plugins"),
    plugin_filter=["docker.py", "systemd.py"]
)
```

## Advanced Configuration

### Service Grouping

Group services by category:

```python
from control_deck import ControlDeck, DeckConfig, ServiceGroup

config = DeckConfig(
    title="Infrastructure",
    groups=[
        ServiceGroup("Web Services", ["nginx", "apache"]),
        ServiceGroup("Databases", ["postgresql", "redis"]),
        ServiceGroup("Monitoring", ["prometheus", "grafana"])
    ]
)
```

### Custom Actions

Add custom actions to the header bar:

```python
config = DeckConfig(
    custom_actions=[
        {
            "label": "Logs",
            "icon": "document-open-symbolic",
            "callback": open_logs
        },
        {
            "label": "Settings",
            "icon": "preferences-system-symbolic",
            "callback": open_settings
        }
    ]
)
```

### Notification Settings

Configure desktop notifications:

```python
config = DeckConfig(
    notifications={
        "enabled": True,
        "on_start": True,
        "on_stop": True,
        "on_error": True,
        "sound": False
    }
)
```

### Logging Configuration

Set up logging:

```python
config = DeckConfig(
    logging={
        "level": "INFO",
        "file": "/var/log/control-deck.log",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "rotate": True,
        "max_size": "10MB"
    }
)
```

## Platform-Specific Configuration

### Linux

```python
config = DeckConfig(
    # Use system theme
    dark_mode=None,
    # Integration with systemd
    use_systemd=True,
    # Desktop file for launcher
    create_desktop_file=True
)
```

### Windows

```python
config = DeckConfig(
    # Windows-specific icon
    icon_file="app.ico",
    # Start with Windows
    auto_start=True,
    # System tray integration
    minimize_to_tray=True
)
```

### macOS

```python
config = DeckConfig(
    # macOS menu bar
    use_menu_bar=True,
    # Dock icon
    dock_icon="AppIcon.icns",
    # Native notifications
    use_native_notifications=True
)
```

## Configuration Profiles

Support multiple configurations:

```python
import sys

profiles = {
    "development": DeckConfig(
        title="Dev Services",
        refresh_interval=2,
        dark_mode=True
    ),
    "production": DeckConfig(
        title="Production Services",
        refresh_interval=10,
        show_header=False
    ),
    "minimal": DeckConfig(
        title="Services",
        compact_mode=True,
        show_status_bar=False
    )
}

# Select profile from command line
profile_name = sys.argv[1] if len(sys.argv) > 1 else "development"
config = profiles.get(profile_name, profiles["development"])
```

## Configuration Validation

Validate configuration before use:

```python
def validate_config(config: DeckConfig) -> bool:
    """Validate configuration values"""
    
    if config.width < 300 or config.width > 3840:
        print(f"Invalid width: {config.width}")
        return False
    
    if config.height < 200 or config.height > 2160:
        print(f"Invalid height: {config.height}")
        return False
    
    if config.refresh_interval < 1 or config.refresh_interval > 3600:
        print(f"Invalid refresh interval: {config.refresh_interval}")
        return False
    
    if config.custom_css and not Path(config.custom_css).exists():
        print(f"CSS file not found: {config.custom_css}")
        return False
    
    return True

# Use validation
config = DeckConfig(width=600, height=400)
if validate_config(config):
    deck = ControlDeck(config)
    deck.run()
```

## Dynamic Configuration

Update configuration at runtime:

```python
class ConfigurableDeck(ControlDeck):
    def update_config(self, **kwargs):
        """Update configuration dynamically"""
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
        
        # Apply changes
        self.apply_theme()
        self.restart_refresh_timer()

# Usage
deck = ConfigurableDeck(config)

# Later, update configuration
deck.update_config(
    dark_mode=False,
    refresh_interval=10
)
```

## Configuration Persistence

Save and load user preferences:

```python
import json
from pathlib import Path

class PersistentConfig:
    CONFIG_PATH = Path.home() / ".config" / "control-deck" / "preferences.json"
    
    @classmethod
    def save(cls, config: DeckConfig):
        """Save configuration to disk"""
        cls.CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "title": config.title,
            "width": config.width,
            "height": config.height,
            "dark_mode": config.dark_mode,
            "refresh_interval": config.refresh_interval
        }
        
        with open(cls.CONFIG_PATH, "w") as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load(cls) -> DeckConfig:
        """Load configuration from disk"""
        if cls.CONFIG_PATH.exists():
            with open(cls.CONFIG_PATH) as f:
                data = json.load(f)
            return DeckConfig(**data)
        return DeckConfig()

# Usage
config = PersistentConfig.load()
deck = ControlDeck(config)

# Save on exit
def on_quit():
    PersistentConfig.save(deck.config)
```

## Best Practices

1. **Provide defaults:** Always have sensible defaults
2. **Validate early:** Check configuration before starting
3. **Document options:** Comment configuration files
4. **Use type hints:** Ensure type safety
5. **Support overrides:** Allow environment variables
6. **Keep it simple:** Don't over-configure
7. **Version configs:** Track configuration changes

## Example: Full Configuration

```python
#!/usr/bin/env python3
"""Fully configured Control Deck application"""

from control_deck import ControlDeck, DeckConfig
from pathlib import Path
import os

# Build configuration from multiple sources
config = DeckConfig(
    # Basic settings
    title=os.getenv("DECK_TITLE", "My Services"),
    width=800,
    height=600,
    
    # Theme
    dark_mode=True,
    custom_css=Path("styles/custom.css"),
    
    # Refresh
    auto_refresh=True,
    refresh_interval=5,
    
    # UI Components
    show_header=True,
    show_status_bar=True,
    compact_mode=False,
    
    # Plugins
    plugin_directory=Path("plugins"),
    auto_load_plugins=True,
    
    # Advanced
    notifications={"enabled": True, "on_error": True},
    logging={"level": "INFO", "file": "deck.log"}
)

# Create and run
deck = ControlDeck(config)
deck.run()
```

## See Also

- [Getting Started](getting-started.md)
- [Theming Guide](theming.md)
- [API Reference](api-reference.md)