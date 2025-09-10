#!/usr/bin/env python3
"""
Plugin Manager for Control Deck - Add/remove plugins from the UI
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio
import json
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List
import shutil

class PluginInfo:
    """Information about a plugin"""
    def __init__(self, path: Path):
        self.path = path
        self.name = path.stem
        self.enabled = True
        self.error = None
        
        # Try to load metadata
        try:
            spec = importlib.util.spec_from_file_location(self.name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Look for metadata
            self.display_name = getattr(module, '__plugin_name__', self.name)
            self.description = getattr(module, '__description__', 'No description')
            self.author = getattr(module, '__author__', 'Unknown')
            self.version = getattr(module, '__version__', '1.0')
            
            # Count ServiceModule classes
            self.module_count = 0
            for item_name in dir(module):
                item = getattr(module, item_name)
                if isinstance(item, type) and item_name.endswith('Module'):
                    self.module_count += 1
                    
        except Exception as e:
            self.error = str(e)
            self.display_name = self.name
            self.description = f"Error: {e}"
            self.author = "Unknown"
            self.version = "?"
            self.module_count = 0

class PluginCard(Gtk.Box):
    """Card showing plugin info with enable/disable"""
    
    def __init__(self, plugin_info: PluginInfo, on_toggle_callback):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.plugin_info = plugin_info
        self.on_toggle_callback = on_toggle_callback
        
        self.set_margin_top(8)
        self.set_margin_bottom(8)
        self.set_margin_start(12)
        self.set_margin_end(12)
        
        # Left side - plugin info
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        left_box.set_hexpand(True)
        
        # Plugin name
        name_label = Gtk.Label(label=plugin_info.display_name)
        name_label.set_halign(Gtk.Align.START)
        name_label.add_css_class("title-4")
        left_box.append(name_label)
        
        # Description
        desc_label = Gtk.Label(label=plugin_info.description)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.add_css_class("dim-label")
        desc_label.set_wrap(True)
        left_box.append(desc_label)
        
        # Metadata
        meta_text = f"v{plugin_info.version} by {plugin_info.author} • {plugin_info.module_count} modules"
        meta_label = Gtk.Label(label=meta_text)
        meta_label.set_halign(Gtk.Align.START)
        meta_label.add_css_class("caption")
        left_box.append(meta_label)
        
        self.append(left_box)
        
        # Right side - controls
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # Status icon
        if plugin_info.error:
            icon = Gtk.Image()
            icon.set_from_icon_name("dialog-error-symbolic")
            icon.add_css_class("error")
            icon.set_tooltip_text(plugin_info.error)
            controls_box.append(icon)
        
        # Enable/disable switch
        self.switch = Gtk.Switch()
        self.switch.set_active(plugin_info.enabled and not plugin_info.error)
        self.switch.set_sensitive(not plugin_info.error)
        self.switch.set_valign(Gtk.Align.CENTER)
        self.switch.connect("state-set", self.on_toggle)
        controls_box.append(self.switch)
        
        # Delete button
        delete_btn = Gtk.Button()
        delete_btn.set_icon_name("user-trash-symbolic")
        delete_btn.set_tooltip_text("Remove plugin")
        delete_btn.add_css_class("circular")
        delete_btn.add_css_class("flat")
        delete_btn.connect("clicked", self.on_delete)
        controls_box.append(delete_btn)
        
        self.append(controls_box)
    
    def on_toggle(self, switch, state):
        """Handle enable/disable"""
        self.plugin_info.enabled = state
        self.on_toggle_callback(self.plugin_info)
        return False
    
    def on_delete(self, button):
        """Handle delete request"""
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            f"Remove '{self.plugin_info.display_name}'?",
            "This will delete the plugin file."
        )
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("delete", "Delete")
        dialog.set_response_appearance("delete", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.connect("response", self.on_delete_response)
        dialog.present()
    
    def on_delete_response(self, dialog, response):
        """Handle delete confirmation"""
        if response == "delete":
            try:
                self.plugin_info.path.unlink()
                self.on_toggle_callback(None)  # Trigger refresh
            except Exception as e:
                print(f"Failed to delete plugin: {e}")

class PluginManager(Adw.ApplicationWindow):
    """Plugin manager window"""
    
    def __init__(self, app, plugin_dir: Path):
        super().__init__(application=app)
        self.plugin_dir = plugin_dir
        self.plugins = {}
        
        self.set_title("Plugin Manager")
        self.set_default_size(600, 500)
        
        # Main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Header bar
        header = Adw.HeaderBar()
        
        # Add plugin button
        add_btn = Gtk.Button()
        add_btn.set_icon_name("list-add-symbolic")
        add_btn.set_tooltip_text("Add plugin from file")
        add_btn.connect("clicked", self.on_add_plugin)
        header.pack_start(add_btn)
        
        # Refresh button
        refresh_btn = Gtk.Button()
        refresh_btn.set_icon_name("view-refresh-symbolic")
        refresh_btn.set_tooltip_text("Refresh")
        refresh_btn.connect("clicked", lambda x: self.refresh_plugins())
        header.pack_end(refresh_btn)
        
        main_box.append(header)
        
        # Plugin list
        self.list_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.list_box.set_margin_top(12)
        self.list_box.set_margin_bottom(12)
        self.list_box.set_margin_start(12)
        self.list_box.set_margin_end(12)
        
        # Scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.list_box)
        scrolled.set_vexpand(True)
        main_box.append(scrolled)
        
        # Info bar
        info_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        info_box.set_margin_top(6)
        info_box.set_margin_bottom(6)
        info_box.set_margin_start(12)
        info_box.set_margin_end(12)
        
        info_label = Gtk.Label(label=f"Plugin directory: {self.plugin_dir}")
        info_label.add_css_class("dim-label")
        info_box.append(info_label)
        
        main_box.append(info_box)
        
        self.set_content(main_box)
        
        # Load plugins
        self.refresh_plugins()
    
    def refresh_plugins(self):
        """Scan and display plugins"""
        # Clear current list
        while child := self.list_box.get_first_child():
            self.list_box.remove(child)
        
        # Ensure plugin dir exists
        self.plugin_dir.mkdir(exist_ok=True)
        
        # Scan for plugins
        self.plugins.clear()
        
        plugin_files = list(self.plugin_dir.glob("*.py"))
        plugin_files = [f for f in plugin_files if not f.name.startswith("_")]
        
        if not plugin_files:
            # Empty state
            empty_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            
            empty_icon = Gtk.Image()
            empty_icon.set_from_icon_name("folder-open-symbolic")
            empty_icon.set_pixel_size(64)
            empty_icon.add_css_class("dim-label")
            empty_box.append(empty_icon)
            
            empty_label = Gtk.Label(label="No plugins installed")
            empty_label.add_css_class("title-2")
            empty_label.add_css_class("dim-label")
            empty_box.append(empty_label)
            
            help_label = Gtk.Label(label="Click + to add a plugin file")
            help_label.add_css_class("dim-label")
            empty_box.append(help_label)
            
            empty_box.set_vexpand(True)
            empty_box.set_valign(Gtk.Align.CENTER)
            empty_box.set_halign(Gtk.Align.CENTER)
            self.list_box.append(empty_box)
        else:
            # Create cards for each plugin
            for plugin_file in sorted(plugin_files):
                plugin_info = PluginInfo(plugin_file)
                self.plugins[plugin_file.name] = plugin_info
                
                card = PluginCard(plugin_info, self.on_plugin_toggle)
                
                # Wrap in frame
                frame = Gtk.Frame()
                frame.set_child(card)
                self.list_box.append(frame)
    
    def on_plugin_toggle(self, plugin_info):
        """Handle plugin enable/disable or refresh"""
        if plugin_info is None:
            # Refresh request
            self.refresh_plugins()
        else:
            # Save enabled state (could persist to config file)
            print(f"Plugin {plugin_info.name} enabled: {plugin_info.enabled}")
    
    def on_add_plugin(self, button):
        """Handle add plugin button"""
        dialog = Gtk.FileChooserNative.new(
            "Select Plugin File",
            self,
            Gtk.FileChooserAction.OPEN,
            "_Add",
            "_Cancel"
        )
        
        # Add filter for Python files
        filter_py = Gtk.FileFilter()
        filter_py.set_name("Python files")
        filter_py.add_pattern("*.py")
        dialog.add_filter(filter_py)
        
        dialog.connect("response", self.on_file_selected)
        dialog.show()
    
    def on_file_selected(self, dialog, response):
        """Handle file selection"""
        if response == Gtk.ResponseType.ACCEPT:
            source_file = Path(dialog.get_file().get_path())
            dest_file = self.plugin_dir / source_file.name
            
            try:
                # Copy file to plugins directory
                shutil.copy2(source_file, dest_file)
                self.refresh_plugins()
            except Exception as e:
                error_dialog = Adw.MessageDialog.new(
                    self,
                    "Failed to add plugin",
                    str(e)
                )
                error_dialog.add_response("ok", "OK")
                error_dialog.present()

class PluginManagerApp(Adw.Application):
    """Standalone plugin manager app"""
    
    def __init__(self):
        super().__init__(application_id='com.control.deck.plugins')
        
    def do_activate(self):
        plugin_dir = Path(__file__).parent / "plugins"
        window = PluginManager(self, plugin_dir)
        window.present()

if __name__ == "__main__":
    app = PluginManagerApp()
    app.run()