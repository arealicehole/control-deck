# API Reference

Complete API documentation for Control Deck framework.

## Core Classes

### `ControlDeck`

Main application class that manages the UI and service modules.

```python
class ControlDeck:
    def __init__(self, config: DeckConfig = None)
    def add_module(self, module: ServiceModule) -> None
    def load_plugins_from_directory(self, path: Path) -> None
    def run(self) -> None
```

#### Methods

##### `__init__(config: DeckConfig = None)`
Initialize a new Control Deck application.

**Parameters:**
- `config`: Optional configuration object

**Example:**
```python
deck = ControlDeck(DeckConfig(title="My Deck"))
```

##### `add_module(module: ServiceModule) -> None`
Add a service module to the deck.

**Parameters:**
- `module`: Instance of a ServiceModule subclass

**Example:**
```python
deck.add_module(MyServiceModule())
```

##### `load_plugins_from_directory(path: Path) -> None`
Load all plugin modules from a directory.

**Parameters:**
- `path`: Path to directory containing plugin files

**Example:**
```python
deck.load_plugins_from_directory(Path("plugins"))
```

##### `run() -> None`
Start the GTK application main loop.

### `DeckConfig`

Configuration dataclass for customizing deck appearance and behavior.

```python
@dataclass
class DeckConfig:
    title: str = "Control Deck"
    width: int = 500
    height: int = 600
    dark_mode: bool = True
    auto_refresh: bool = True
    refresh_interval: int = 5
    show_header: bool = True
    show_status_bar: bool = True
    custom_css: Optional[str] = None
    icon_theme: Optional[str] = None
```

#### Fields

- `title`: Window title
- `width`: Initial window width in pixels
- `height`: Initial window height in pixels
- `dark_mode`: Enable dark theme
- `auto_refresh`: Enable automatic status refresh
- `refresh_interval`: Refresh interval in seconds
- `show_header`: Show header bar with controls
- `show_status_bar`: Show status bar at bottom
- `custom_css`: Path to custom CSS file
- `icon_theme`: GTK icon theme name

**Example:**
```python
config = DeckConfig(
    title="Voice Services",
    width=600,
    height=400,
    dark_mode=True,
    refresh_interval=3
)
```

### `ServiceModule` (Abstract Base Class)

Base class for all service modules. All plugins must extend this class.

```python
from abc import ABC, abstractmethod

class ServiceModule(ABC):
    @abstractmethod
    def get_name(self) -> str
    @abstractmethod
    def get_id(self) -> str
    @abstractmethod
    def check_status(self) -> bool
    @abstractmethod
    def start(self) -> bool
    @abstractmethod
    def stop(self) -> bool
    
    # Optional methods
    def get_details(self) -> str
    def get_icon(self) -> Optional[str]
    def restart(self) -> bool
    def can_remove(self) -> bool
    def remove(self) -> bool
```

#### Required Methods

##### `get_name() -> str`
Return the display name for the UI.

**Returns:** Human-readable service name

##### `get_id() -> str`
Return unique identifier for this service.

**Returns:** Unique string identifier

##### `check_status() -> bool`
Check if the service is currently running.

**Returns:** `True` if running, `False` otherwise

##### `start() -> bool`
Start the service.

**Returns:** `True` if successful, `False` otherwise

##### `stop() -> bool`
Stop the service.

**Returns:** `True` if successful, `False` otherwise

#### Optional Methods

##### `get_details() -> str`
Return additional status information.

**Returns:** Status details string

**Default:** Returns empty string

##### `get_icon() -> Optional[str]`
Return GTK icon name.

**Returns:** Icon name or None

**Default:** Returns None

##### `restart() -> bool`
Restart the service.

**Returns:** `True` if successful, `False` otherwise

**Default:** Calls `stop()` then `start()`

##### `can_remove() -> bool`
Check if service can be removed.

**Returns:** `True` if removable, `False` otherwise

**Default:** Returns `False`

##### `remove() -> bool`
Remove the service permanently.

**Returns:** `True` if successful, `False` otherwise

**Default:** Returns `False`

## Plugin System

### Plugin Discovery

Plugins are Python files containing classes that extend `ServiceModule`.

#### Discovery Rules

1. Files must be in the plugins directory
2. Files must have `.py` extension
3. Files starting with `_` are ignored
4. Each file can contain multiple module classes

#### Module Detection

Classes are detected as modules if they:
1. Extend `ServiceModule`
2. Are not abstract classes
3. Have all required methods implemented

### Plugin Metadata

Optional module-level variables for plugin information:

```python
__plugin_name__ = "Plugin Display Name"
__description__ = "What this plugin does"
__author__ = "Author Name"
__version__ = "1.0.0"
__url__ = "https://github.com/..."
```

### Factory Functions

Plugins can provide factory functions to create multiple modules:

```python
def get_services():
    """Return list of service modules"""
    return [
        ServiceA(),
        ServiceB(),
        ServiceC()
    ]
```

## UI Components

### ServiceCard

Visual representation of a service module.

**Structure:**
```
┌─────────────────────────┐
│ [icon] Service Name     │
│ Status: Running         │
│ Details text            │
│ [Start] [Stop] [Remove] │
└─────────────────────────┘
```

**CSS Classes:**
- `.service-card` - Main card container
- `.service-header` - Header with name
- `.service-status` - Status label
- `.service-details` - Details text
- `.service-controls` - Button container

### HeaderBar

Application header with controls.

**Components:**
- Title label
- Refresh button
- Plugin manager button
- Menu button (optional)

**CSS Classes:**
- `.header-bar` - Main header
- `.refresh-button` - Refresh button
- `.plugin-button` - Plugin manager button

### StatusBar

Bottom bar showing aggregate status.

**Format:** `"{running} running, {total} total"`

**CSS Class:** `.status-bar`

## Event System

### Signals

Control Deck emits signals for plugin interactions:

- `service-started`: When a service starts
- `service-stopped`: When a service stops
- `service-removed`: When a service is removed
- `refresh-completed`: After status refresh

### Callbacks

Modules can register callbacks:

```python
class CallbackModule(ServiceModule):
    def on_started(self):
        """Called after successful start"""
        pass
    
    def on_stopped(self):
        """Called after successful stop"""
        pass
```

## Threading

### Main Thread

All UI operations must happen on the main thread:

```python
from gi.repository import GLib

def background_task():
    # Do work
    GLib.idle_add(update_ui, result)
```

### Background Operations

Long-running operations should use threads:

```python
import threading

def start(self):
    thread = threading.Thread(target=self._start_async)
    thread.daemon = True
    thread.start()
    return True
```

## Error Handling

### Exception Types

- `ModuleLoadError`: Failed to load plugin
- `ServiceError`: Service operation failed
- `ConfigError`: Invalid configuration

### Best Practices

1. Always catch exceptions in module methods
2. Return `False` on failure
3. Log errors for debugging
4. Provide user-friendly error messages

```python
def start(self) -> bool:
    try:
        # Start logic
        return True
    except PermissionError:
        print("Permission denied")
        return False
    except Exception as e:
        print(f"Start failed: {e}")
        return False
```

## Platform Differences

### Linux

- Default platform
- Full systemd support
- Native GTK4 performance

### Windows

- Requires MSYS2
- Limited systemd (use services.msc)
- Some icon themes unavailable

### macOS

- Requires Homebrew
- Use launchctl instead of systemd
- May need XQuartz for X11 apps

## Performance

### Optimization Tips

1. **Cache status checks:**
```python
def __init__(self):
    self._status_cache = None
    self._cache_time = 0

def check_status(self):
    if time.time() - self._cache_time < 1:
        return self._status_cache
    # Check status
    self._status_cache = result
    self._cache_time = time.time()
    return result
```

2. **Use subprocess efficiently:**
```python
# Good - single call
result = subprocess.run(["docker", "ps", "-a"], capture_output=True)

# Bad - multiple calls
for container in containers:
    subprocess.run(["docker", "inspect", container])
```

3. **Batch operations:**
```python
def get_all_statuses(self):
    # Get all statuses in one call
    return subprocess.run(["systemctl", "list-units"], ...)
```

## Security

### Best Practices

1. Never store credentials in code
2. Use subprocess with shell=False
3. Validate all user input
4. Use minimal privileges
5. Don't expose sensitive information in UI

### Permission Handling

```python
def start(self):
    try:
        subprocess.run(["systemctl", "start", "service"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        if "permission denied" in str(e).lower():
            # Could prompt for elevated privileges
            pass
        return False
```

## Debugging

### Enable Debug Output

```python
import logging
logging.basicConfig(level=logging.DEBUG)

class DebugModule(ServiceModule):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        self.logger.debug("Starting service")
        # ...
```

### GTK Inspector

Launch with GTK Inspector:
```bash
GTK_DEBUG=interactive ./my-deck.py
```

### Common Issues

1. **Module not loading:** Check console for errors
2. **UI not updating:** Ensure using GLib.idle_add
3. **Buttons not working:** Check method return values
4. **Icon not showing:** Verify icon name exists

## Version History

- **2.0.0** - Plugin architecture, UI refresh
- **1.5.0** - Added plugin manager
- **1.0.0** - Initial release

## See Also

- [Getting Started](getting-started.md)
- [Plugin Development](plugin-development.md)
- [Examples](examples.md)