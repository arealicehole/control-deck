# Plugin Manager Guide

Learn how to use the built-in Plugin Manager to discover, install, enable, and manage plugins.

## Opening the Plugin Manager

### From the UI

Click the plugin button (🧩) in the header bar of any Control Deck application.

### Programmatically

```python
from plugin_manager import PluginManager

def open_plugin_manager():
    manager = PluginManager(parent_window)
    manager.present()
```

## Plugin Manager Interface

```
┌─────────────────────────────────────────┐
│ 🧩 Plugin Manager                   [X] │
├─────────────────────────────────────────┤
│ [↻ Refresh] [+ Add Plugin] [⚙ Settings] │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │ ☑ Docker Services         v2.0.1    │ │
│ │   Manages Docker containers         │ │
│ │   By: John Doe                      │ │
│ │   [Configure] [Disable] [Remove]    │ │
│ └─────────────────────────────────────┘ │
│ ┌─────────────────────────────────────┐ │
│ │ ☐ System Monitor          v1.5.0    │ │
│ │   Monitor system resources          │ │
│ │   By: Jane Smith                    │ │
│ │   [Enable] [Remove]                 │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Managing Plugins

### Viewing Installed Plugins

The main view shows all detected plugins with:
- **Name:** Plugin display name
- **Version:** Plugin version number
- **Description:** What the plugin does
- **Author:** Plugin creator
- **Status:** Enabled (☑) or Disabled (☐)

### Enabling/Disabling Plugins

Toggle plugins without removing them:

```python
# Click the checkbox or toggle button
# Disabled plugins won't load on next startup
```

Disabled plugins remain in the plugins directory but aren't loaded.

### Removing Plugins

Permanently delete a plugin:

1. Select the plugin
2. Click "Remove"
3. Confirm the action

**Warning:** This deletes the plugin file permanently.

## Adding Plugins

### Method 1: Add Plugin Button

1. Click "Add Plugin" in the Plugin Manager
2. Select a `.py` file containing the plugin
3. The file is copied to the plugins directory
4. Plugin appears in the list

### Method 2: URL Installation

Enter a plugin URL:

```
https://github.com/user/repo/raw/main/plugin.py
```

The manager downloads and installs it.

### Method 3: Drag and Drop

Drag plugin files directly into the Plugin Manager window.

### Method 4: Manual Copy

Place plugin files in the `plugins/` directory:

```bash
cp my_plugin.py ~/.config/control-deck/plugins/
```

## Plugin Discovery

### Local Plugins

The manager searches these locations:

1. `./plugins/` - Current directory
2. `~/.config/control-deck/plugins/` - User plugins
3. `/usr/share/control-deck/plugins/` - System plugins
4. Custom paths via configuration

### Online Repositories

Configure plugin repositories:

```python
plugin_repos = [
    "https://plugins.control-deck.io/",
    "https://github.com/control-deck/plugins/",
    "https://custom-repo.example.com/"
]
```

## Plugin Information

### Viewing Details

Click on a plugin to see:

```
Plugin: Docker Manager
Version: 2.0.1
Author: John Doe
License: MIT
URL: https://github.com/johndoe/docker-manager
Description: Complete Docker container management
Dependencies: docker-py >= 5.0.0

Provides modules:
- DockerContainer (dynamic)
- DockerImage
- DockerNetwork

Settings:
- Auto-refresh: Yes
- Show stopped: No
- Group by stack: Yes
```

### Plugin Metadata

Plugins should include metadata:

```python
__plugin_name__ = "My Plugin"
__description__ = "Does something useful"
__author__ = "Your Name"
__version__ = "1.0.0"
__license__ = "MIT"
__url__ = "https://github.com/..."
__dependencies__ = ["requests>=2.0.0", "pyyaml"]
```

## Plugin Configuration

### Per-Plugin Settings

Some plugins have configurable options:

1. Select the plugin
2. Click "Configure"
3. Adjust settings
4. Click "Save"

Example configuration dialog:

```python
class PluginConfig(Adw.PreferencesWindow):
    def __init__(self, plugin):
        super().__init__()
        
        # Create settings page
        page = Adw.PreferencesPage()
        page.set_title("Docker Settings")
        
        # Add settings groups
        group = Adw.PreferencesGroup()
        group.set_title("Display Options")
        
        # Add switches, entries, etc.
        switch = Adw.SwitchRow()
        switch.set_title("Show stopped containers")
        group.add(switch)
        
        page.add(group)
        self.add(page)
```

### Global Plugin Settings

Access via Settings button:

- **Plugin directory:** Where to store plugins
- **Auto-update:** Check for plugin updates
- **Update interval:** How often to check
- **Repositories:** Plugin sources
- **Security:** Verification settings

## Plugin Security

### Verification

The manager can verify plugin signatures:

```python
# Plugin with signature
__signature__ = "-----BEGIN PGP SIGNATURE-----..."
```

### Permissions

Control what plugins can do:

```python
plugin_permissions = {
    "network": True,      # Allow network access
    "filesystem": True,   # Allow file system access
    "subprocess": True,   # Allow running commands
    "system": False      # Deny system modifications
}
```

### Sandboxing

Run plugins in restricted environment:

```python
sandbox_config = {
    "enabled": True,
    "timeout": 30,  # Max execution time
    "memory_limit": "100M",
    "cpu_limit": 0.5
}
```

## Plugin Updates

### Checking for Updates

The manager can check for plugin updates:

1. Click "Refresh" to check all plugins
2. Updates shown with "Update available" badge
3. Click "Update" to install new version

### Automatic Updates

Enable in settings:

```python
auto_update_config = {
    "enabled": True,
    "check_interval": 86400,  # Daily
    "auto_install": False,     # Notify only
    "backup_before_update": True
}
```

## Plugin Development Tools

### Plugin Template Generator

Create new plugins from the manager:

1. Click "Create Plugin"
2. Choose template type
3. Enter plugin details
4. Generate skeleton code

### Plugin Validator

Test plugins before distribution:

```python
from plugin_manager import PluginValidator

validator = PluginValidator()
result = validator.validate("my_plugin.py")

if result.is_valid:
    print("Plugin is valid!")
else:
    print(f"Issues found: {result.errors}")
```

### Plugin Packager

Package plugins for distribution:

```python
from plugin_manager import package_plugin

package_plugin(
    source="my_plugin.py",
    output="my_plugin.deck",
    include_deps=True,
    sign=True
)
```

## Command Line Management

### List Plugins

```bash
control-deck plugins list
```

Output:
```
Installed plugins:
  ✓ docker_manager (2.0.1) - Enabled
  ✗ system_monitor (1.5.0) - Disabled
  ✓ network_tools (1.2.3) - Enabled
```

### Install Plugin

```bash
control-deck plugins install my_plugin.py
control-deck plugins install https://example.com/plugin.py
```

### Enable/Disable

```bash
control-deck plugins enable docker_manager
control-deck plugins disable system_monitor
```

### Remove Plugin

```bash
control-deck plugins remove system_monitor
```

## Plugin Collections

### Installing Collections

Install multiple related plugins:

```bash
control-deck plugins install-collection monitoring
```

Collections available:
- `monitoring` - System and service monitoring
- `containers` - Docker and Podman management
- `network` - Network services and tools
- `development` - Development environment services

### Creating Collections

Define a collection in `collection.yaml`:

```yaml
name: My Collection
description: Custom service plugins
version: 1.0.0
plugins:
  - name: plugin1
    url: https://example.com/plugin1.py
    version: ">=1.0.0"
  - name: plugin2
    url: https://example.com/plugin2.py
    version: ">=2.0.0"
```

## Troubleshooting

### Plugin Not Showing

1. Check file has `.py` extension
2. Verify file is in plugins directory
3. Ensure class extends `ServiceModule`
4. Check for Python syntax errors
5. Look for error messages in console

### Plugin Won't Enable

1. Check for missing dependencies
2. Verify Python version compatibility
3. Look for permission issues
4. Check plugin metadata

### Plugin Crashes

1. Run with debug mode:
```bash
DECK_DEBUG=1 control-deck
```

2. Check logs:
```bash
tail -f ~/.config/control-deck/plugin.log
```

3. Validate plugin:
```bash
control-deck plugins validate my_plugin.py
```

## Best Practices

1. **Regular Updates:** Keep plugins updated
2. **Verify Sources:** Only install from trusted sources
3. **Test First:** Test new plugins in development
4. **Backup:** Backup plugins before major changes
5. **Documentation:** Read plugin documentation
6. **Report Issues:** Report bugs to plugin authors

## Plugin Manager API

### For Deck Applications

```python
from plugin_manager import PluginManager

class MyDeck(ControlDeck):
    def __init__(self):
        super().__init__()
        self.plugin_manager = PluginManager(self)
    
    def on_plugin_enabled(self, plugin):
        """Called when plugin is enabled"""
        self.reload_modules()
    
    def on_plugin_disabled(self, plugin):
        """Called when plugin is disabled"""
        self.remove_module(plugin.get_id())
```

### For Plugin Developers

```python
class ManagedPlugin(ServiceModule):
    def on_install(self):
        """Called when plugin is installed"""
        pass
    
    def on_enable(self):
        """Called when plugin is enabled"""
        pass
    
    def on_disable(self):
        """Called when plugin is disabled"""
        pass
    
    def on_uninstall(self):
        """Called before plugin is removed"""
        pass
    
    def get_config_widget(self):
        """Return configuration widget"""
        return MyConfigWidget()
```

## See Also

- [Plugin Development](plugin-development.md)
- [Configuration](configuration.md)
- [Troubleshooting](troubleshooting.md)