# Troubleshooting Guide

Solutions to common issues with Control Deck applications and plugins.

## Installation Issues

### "No module named 'gi'"

**Problem:** Python GObject bindings not installed.

**Solution:**

Linux (Fedora/RHEL):
```bash
sudo dnf install python3-gobject
```

Linux (Ubuntu/Debian):
```bash
sudo apt install python3-gi python3-gi-cairo
```

Windows (MSYS2):
```bash
pacman -S mingw-w64-x86_64-python-gobject
```

macOS:
```bash
brew install pygobject3
```

### "Namespace Gtk not available"

**Problem:** GTK4 not installed.

**Solution:**

Linux:
```bash
# Fedora/RHEL
sudo dnf install gtk4

# Ubuntu/Debian
sudo apt install libgtk-4-1
```

Windows (MSYS2):
```bash
pacman -S mingw-w64-x86_64-gtk4
```

macOS:
```bash
brew install gtk4
```

### "Namespace Adw not available"

**Problem:** libadwaita not installed.

**Solution:**

Linux:
```bash
# Fedora/RHEL
sudo dnf install libadwaita

# Ubuntu/Debian  
sudo apt install libadwaita-1-0
```

Windows (MSYS2):
```bash
pacman -S mingw-w64-x86_64-libadwaita
```

macOS:
```bash
brew install libadwaita
```

## Plugin Issues

### Plugin Not Loading

**Problem:** Plugin file exists but doesn't appear in the deck.

**Checklist:**

1. **File location correct?**
```python
# Plugin must be in one of these locations:
./plugins/
~/.config/control-deck/plugins/
/usr/share/control-deck/plugins/
```

2. **File has .py extension?**
```bash
ls -la plugins/
# Should show: my_plugin.py, not my_plugin.txt
```

3. **File doesn't start with underscore?**
```bash
# Bad: _my_plugin.py
# Good: my_plugin.py
```

4. **Class extends ServiceModule?**
```python
from control_deck import ServiceModule

class MyModule(ServiceModule):  # Must extend ServiceModule
    # ...
```

5. **All required methods implemented?**
```python
class MyModule(ServiceModule):
    def get_name(self) -> str:
        return "My Service"
    
    def get_id(self) -> str:
        return "my-service"
    
    def check_status(self) -> bool:
        return True
    
    def start(self) -> bool:
        return True
    
    def stop(self) -> bool:
        return True
```

6. **No syntax errors?**
```bash
python3 -m py_compile plugins/my_plugin.py
```

7. **Check console for errors:**
```bash
./my-deck.py
# Look for: "Error loading plugin: ..."
```

### Plugin Crashes on Load

**Problem:** Plugin causes application to crash.

**Debug steps:**

1. **Run with debugging:**
```bash
DECK_DEBUG=1 ./my-deck.py
```

2. **Test plugin standalone:**
```python
#!/usr/bin/env python3
from plugins.my_plugin import MyModule

module = MyModule()
print(f"Name: {module.get_name()}")
print(f"Status: {module.check_status()}")
```

3. **Check imports:**
```python
# At top of plugin file
try:
    import problematic_module
except ImportError as e:
    print(f"Missing dependency: {e}")
    # Provide fallback or skip plugin
```

4. **Add error handling:**
```python
class MyModule(ServiceModule):
    def __init__(self):
        try:
            self.initialize()
        except Exception as e:
            print(f"Init failed: {e}")
            # Set safe defaults
            self.initialized = False
```

### Multiple Plugins Not Working Together

**Problem:** Plugins work individually but fail when loaded together.

**Solutions:**

1. **Check for ID conflicts:**
```python
# Each plugin must have unique ID
def get_id(self):
    return "unique-id-here"  # Must be unique!
```

2. **Avoid global state:**
```python
# Bad: Global variable
running = False

class MyModule(ServiceModule):
    def check_status(self):
        return running  # Shared between instances!

# Good: Instance variable
class MyModule(ServiceModule):
    def __init__(self):
        self.running = False
    
    def check_status(self):
        return self.running  # Per-instance
```

3. **Handle resource conflicts:**
```python
def start(self):
    try:
        # Try to acquire resource
        self.resource = acquire_resource()
        return True
    except ResourceInUse:
        print("Resource already in use")
        return False
```

## UI Issues

### Window Not Appearing

**Problem:** Application runs but no window shows.

**Solutions:**

1. **Check display server:**
```bash
echo $DISPLAY  # X11
echo $WAYLAND_DISPLAY  # Wayland
```

2. **Run with GTK debugging:**
```bash
GTK_DEBUG=all ./my-deck.py
```

3. **Verify main loop:**
```python
deck = ControlDeck()
deck.run()  # Must call run()!
```

### Buttons Not Working

**Problem:** Clicking buttons does nothing.

**Debug steps:**

1. **Check return values:**
```python
def start(self):
    print("Start called")  # Add debug print
    # Must return boolean!
    return True  # or False
```

2. **Verify permissions:**
```python
def start(self):
    try:
        subprocess.run(["systemctl", "start", "service"], check=True)
        return True
    except PermissionError:
        print("Need elevated permissions")
        return False
```

3. **Test commands manually:**
```bash
# Test the command your module runs
systemctl start myservice
# Check for errors
```

### Status Not Updating

**Problem:** Service status doesn't refresh.

**Solutions:**

1. **Check refresh enabled:**
```python
config = DeckConfig(
    auto_refresh=True,  # Must be True
    refresh_interval=5   # Seconds between refresh
)
```

2. **Verify check_status works:**
```python
def check_status(self):
    print(f"Checking status...")  # Debug
    result = self._do_check()
    print(f"Status: {result}")     # Debug
    return result
```

3. **Force manual refresh:**
```python
# Click refresh button in UI
# Or programmatically:
deck.refresh_all()
```

## Performance Issues

### Slow Startup

**Problem:** Application takes long to start.

**Solutions:**

1. **Profile startup:**
```bash
python3 -m cProfile -s cumtime ./my-deck.py
```

2. **Lazy load plugins:**
```python
class LazyModule(ServiceModule):
    def __init__(self):
        self._initialized = False
    
    def _lazy_init(self):
        if not self._initialized:
            # Do expensive initialization here
            self._initialized = True
    
    def check_status(self):
        self._lazy_init()
        return self._check()
```

3. **Cache expensive operations:**
```python
class CachedModule(ServiceModule):
    def __init__(self):
        self._cache = {}
        self._cache_time = 0
    
    def check_status(self):
        now = time.time()
        if now - self._cache_time > 5:  # Cache for 5 seconds
            self._cache['status'] = self._real_check()
            self._cache_time = now
        return self._cache['status']
```

### High CPU Usage

**Problem:** Application uses too much CPU.

**Solutions:**

1. **Increase refresh interval:**
```python
config = DeckConfig(
    refresh_interval=10  # Check less frequently
)
```

2. **Optimize check_status:**
```python
# Bad: Running expensive command
def check_status(self):
    result = subprocess.run(["docker", "ps", "-a"], capture_output=True)
    # Parse all output
    return parse_everything(result.stdout)

# Good: Quick check
def check_status(self):
    # Just check if process exists
    result = subprocess.run(["pgrep", "myservice"], capture_output=True)
    return result.returncode == 0
```

3. **Use threading for long operations:**
```python
import threading

class AsyncModule(ServiceModule):
    def check_status(self):
        # Return cached status immediately
        return self._cached_status
    
    def _update_status_async(self):
        # Do expensive check in background
        thread = threading.Thread(target=self._do_expensive_check)
        thread.daemon = True
        thread.start()
```

## System Integration Issues

### systemd Services Not Working

**Problem:** Can't control systemd services.

**Solutions:**

1. **Check if running as user service:**
```python
# System service
subprocess.run(["systemctl", "start", "nginx"])

# User service  
subprocess.run(["systemctl", "--user", "start", "myservice"])
```

2. **Verify service exists:**
```bash
systemctl list-unit-files | grep myservice
systemctl --user list-unit-files | grep myservice
```

3. **Check permissions:**
```bash
# May need sudo for system services
sudo systemctl start nginx

# Or use polkit for GUI apps
pkexec systemctl start nginx
```

### Docker Commands Failing

**Problem:** Docker operations don't work.

**Solutions:**

1. **Check Docker running:**
```bash
docker info
systemctl status docker
```

2. **Verify user in docker group:**
```bash
groups | grep docker
# If not, add user:
sudo usermod -aG docker $USER
# Log out and back in
```

3. **Use sudo if needed:**
```python
def start(self):
    try:
        # Try without sudo first
        subprocess.run(["docker", "start", "container"], check=True)
        return True
    except PermissionError:
        # Fall back to sudo
        subprocess.run(["sudo", "docker", "start", "container"], check=True)
        return True
```

## Platform-Specific Issues

### Windows Issues

**Problem:** Application doesn't work on Windows.

**Solutions:**

1. **Use MSYS2 terminal:**
```bash
# Must run from MSYS2 MinGW terminal
# Not CMD or PowerShell
```

2. **Set environment:**
```bash
export PATH="/mingw64/bin:$PATH"
export PKG_CONFIG_PATH="/mingw64/lib/pkgconfig"
```

3. **Adapt commands:**
```python
import platform

class CrossPlatformModule(ServiceModule):
    def start(self):
        if platform.system() == "Windows":
            # Windows command
            subprocess.run(["net", "start", "service"])
        else:
            # Linux command
            subprocess.run(["systemctl", "start", "service"])
```

### macOS Issues

**Problem:** GTK4 not working properly on macOS.

**Solutions:**

1. **Install XQuartz if needed:**
```bash
brew install --cask xquartz
```

2. **Set display:**
```bash
export DISPLAY=:0
```

3. **Use native alternatives:**
```python
if platform.system() == "Darwin":
    # Use launchctl instead of systemctl
    subprocess.run(["launchctl", "start", "com.example.service"])
```

## Debugging Tools

### Enable Debug Logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class DebugModule(ServiceModule):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Module initialized")
```

### GTK Inspector

```bash
GTK_DEBUG=interactive ./my-deck.py
```

Press Ctrl+Shift+I to open inspector.

### Python Debugger

```python
import pdb

class MyModule(ServiceModule):
    def start(self):
        pdb.set_trace()  # Breakpoint here
        # Step through code
        return True
```

### Strace for System Calls

```bash
strace -e trace=process ./my-deck.py
```

## Getting Help

### Collect Debug Information

```bash
# System info
uname -a
python3 --version
gtk4-launch --version

# Dependencies
pip list | grep -E "(gi|gtk|adwaita)"

# Error messages
./my-deck.py 2>&1 | tee debug.log
```

### Report Issues

Include:
1. Error messages
2. Debug output
3. System information
4. Steps to reproduce
5. Expected vs actual behavior

### Community Resources

- GitHub Issues: Report bugs
- Discussions: Ask questions
- Wiki: Community solutions
- Discord: Real-time help

## Common Error Messages

### "Permission denied"
- Need elevated privileges
- User not in required group
- File permissions incorrect

### "Command not found"
- Package not installed
- PATH not set correctly
- Wrong platform command

### "No such file or directory"
- Path doesn't exist
- Relative vs absolute path issue
- Working directory incorrect

### "Connection refused"
- Service not running
- Wrong port number
- Firewall blocking

### "Resource temporarily unavailable"
- Resource locked
- Too many open files
- System limits reached

## See Also

- [Getting Started](getting-started.md)
- [Plugin Development](plugin-development.md)
- [Configuration](configuration.md)