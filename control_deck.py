#!/usr/bin/env python3
"""
Control Deck - Universal service control panel framework
Extensible through plugins
"""

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, Gio, Gdk
import importlib
import importlib.util
from pathlib import Path
from typing import List, Optional, Dict, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass

class ServiceModule(ABC):
    """Base class for all service modules"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return display name"""
        pass
    
    @abstractmethod
    def get_id(self) -> str:
        """Return unique identifier"""
        pass
    
    @abstractmethod
    def check_status(self) -> bool:
        """Check if service is running"""
        pass
    
    @abstractmethod
    def start(self) -> bool:
        """Start the service"""
        pass
    
    @abstractmethod
    def stop(self) -> bool:
        """Stop the service"""
        pass
    
    def restart(self) -> bool:
        """Restart the service (default: stop then start)"""
        return self.stop() and self.start()
    
    def get_details(self) -> str:
        """Optional: Return status details"""
        return ""
    
    def get_icon(self) -> Optional[str]:
        """Optional: Return icon name"""
        return None
    
    def can_remove(self) -> bool:
        """Optional: Whether this service can be removed"""
        return False
    
    def remove(self) -> bool:
        """Optional: Remove the service"""
        return False

class ServiceCard(Gtk.Box):
    """Universal UI card for any service module"""
    
    def __init__(self, module: ServiceModule, on_refresh_callback):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.module = module
        self.on_refresh_callback = on_refresh_callback
        self.set_margin_top(8)
        self.set_margin_bottom(8)
        self.set_margin_start(12)
        self.set_margin_end(12)
        
        # Left side - name and details
        left_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        left_box.set_hexpand(True)
        
        # Service icon and name
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        if icon_name := module.get_icon():
            icon = Gtk.Image()
            icon.set_from_icon_name(icon_name)
            icon.set_pixel_size(20)
            name_box.append(icon)
        
        self.name_label = Gtk.Label(label=module.get_name())
        self.name_label.set_halign(Gtk.Align.START)
        self.name_label.add_css_class("title-4")
        name_box.append(self.name_label)
        
        left_box.append(name_box)
        
        # Status/details
        self.status_label = Gtk.Label()
        self.status_label.set_halign(Gtk.Align.START)
        self.status_label.add_css_class("dim-label")
        left_box.append(self.status_label)
        
        self.append(left_box)
        
        # Status indicator
        self.status_icon = Gtk.Image()
        self.status_icon.set_pixel_size(16)
        self.append(self.status_icon)
        
        # Control buttons
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        
        # Toggle switch for simple services
        self.switch = Gtk.Switch()
        self.switch.set_valign(Gtk.Align.CENTER)
        self.switch.connect("state-set", self.on_toggle)
        controls_box.append(self.switch)
        
        # Restart button
        restart_btn = Gtk.Button()
        restart_btn.set_icon_name("view-refresh-symbolic")
        restart_btn.set_tooltip_text("Restart")
        restart_btn.add_css_class("circular")
        restart_btn.add_css_class("flat")
        restart_btn.connect("clicked", self.on_restart)
        controls_box.append(restart_btn)
        
        # Remove button if applicable
        if module.can_remove():
            remove_btn = Gtk.Button()
            remove_btn.set_icon_name("user-trash-symbolic")
            remove_btn.set_tooltip_text("Remove")
            remove_btn.add_css_class("circular")
            remove_btn.add_css_class("flat")
            remove_btn.add_css_class("destructive-action")
            remove_btn.connect("clicked", self.on_remove)
            controls_box.append(remove_btn)
        
        self.append(controls_box)
        
        # Initial update
        self.update_status()
    
    def update_status(self):
        """Update the UI based on service status"""
        is_running = self.module.check_status()
        
        # Update switch without triggering signal
        self.switch.set_active(is_running)
        
        # Update status icon
        if is_running:
            self.status_icon.set_from_icon_name("emblem-default-symbolic")
            self.status_icon.add_css_class("success")
            self.status_icon.remove_css_class("error")
        else:
            self.status_icon.set_from_icon_name("process-stop-symbolic")
            self.status_icon.add_css_class("error")
            self.status_icon.remove_css_class("success")
        
        # Update details
        details = self.module.get_details()
        status = "Running" if is_running else "Stopped"
        self.status_label.set_text(f"{status} • {details}" if details else status)
    
    def on_toggle(self, switch, state):
        """Handle toggle switch"""
        if state:
            success = self.module.start()
        else:
            success = self.module.stop()
        
        GLib.timeout_add(1000, self.update_status)
        return True
    
    def on_restart(self, button):
        """Handle restart button"""
        self.module.restart()
        GLib.timeout_add(1000, self.update_status)
    
    def on_remove(self, button):
        """Handle remove button"""
        dialog = Adw.MessageDialog.new(
            self.get_root(),
            f"Remove '{self.module.get_name()}'?",
            "This action cannot be undone."
        )
        dialog.add_response("cancel", "Cancel")
        dialog.add_response("remove", "Remove")
        dialog.set_response_appearance("remove", Adw.ResponseAppearance.DESTRUCTIVE)
        dialog.connect("response", self.on_remove_response)
        dialog.present()
    
    def on_remove_response(self, dialog, response):
        """Handle remove confirmation"""
        if response == "remove":
            if self.module.remove():
                GLib.timeout_add(500, self.on_refresh_callback)

@dataclass
class DeckConfig:
    """Configuration for a deck instance"""
    title: str = "Control Deck"
    app_id: str = "com.control.deck"
    width: int = 500
    height: int = 400
    refresh_interval: int = 10
    theme: Optional[str] = None
    dark_mode: bool = True
    css: Optional[str] = None

class ControlDeck(Adw.Application):
    """Main application framework"""
    
    def __init__(self, config: DeckConfig = None, modules: List[ServiceModule] = None):
        self.config = config or DeckConfig()
        super().__init__(application_id=self.config.app_id)
        self.modules = modules or []
        self.cards = []
        
    def add_module(self, module: ServiceModule):
        """Add a service module"""
        self.modules.append(module)
    
    def load_plugin(self, plugin_path: Path):
        """Load a plugin module from file"""
        spec = importlib.util.spec_from_file_location("plugin", plugin_path)
        plugin = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(plugin)
        
        # Look for ServiceModule subclasses
        for item_name in dir(plugin):
            item = getattr(plugin, item_name)
            if isinstance(item, type) and issubclass(item, ServiceModule) and item != ServiceModule:
                self.add_module(item())
    
    def load_plugins_from_directory(self, directory: Path):
        """Load all plugins from a directory"""
        if directory.exists():
            for plugin_file in directory.glob("*.py"):
                if not plugin_file.name.startswith("_"):
                    try:
                        self.load_plugin(plugin_file)
                    except Exception as e:
                        print(f"Failed to load plugin {plugin_file}: {e}")
    
    def do_activate(self):
        """Build and show the window"""
        # Create window
        self.window = Adw.ApplicationWindow(application=self)
        self.window.set_title(self.config.title)
        self.window.set_default_size(self.config.width, self.config.height)
        
        # Apply theme settings
        if self.config.dark_mode:
            style_manager = Adw.StyleManager.get_default()
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        
        # Load custom CSS if provided
        if self.config.css:
            self.load_custom_css(self.config.css)
        
        # Main box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        # Header bar
        header = Adw.HeaderBar()
        
        # Refresh button
        refresh_btn = Gtk.Button()
        refresh_btn.set_icon_name("view-refresh-symbolic")
        refresh_btn.set_tooltip_text("Refresh")
        refresh_btn.add_css_class("flat")
        refresh_btn.connect("clicked", lambda x: self.refresh_all())
        header.pack_start(refresh_btn)
        
        main_box.append(header)
        
        # Content box with cards
        self.content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.content.set_margin_top(12)
        self.content.set_margin_bottom(12)
        self.content.set_margin_start(12)
        self.content.set_margin_end(12)
        
        # Scrolled window for content
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_child(self.content)
        scrolled.set_vexpand(True)
        main_box.append(scrolled)
        
        # Status bar
        self.status_label = Gtk.Label()
        self.status_label.set_margin_top(6)
        self.status_label.set_margin_bottom(6)
        self.status_label.add_css_class("dim-label")
        main_box.append(self.status_label)
        
        self.window.set_content(main_box)
        self.window.present()
        
        # Initial load
        self.refresh_all()
        
        # Auto-refresh timer
        if self.config.refresh_interval > 0:
            GLib.timeout_add_seconds(self.config.refresh_interval, self.auto_refresh)
    
    def load_custom_css(self, css: str):
        """Load custom CSS"""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def refresh_all(self):
        """Refresh all service cards"""
        # Clear current cards
        while child := self.content.get_first_child():
            self.content.remove(child)
        self.cards.clear()
        
        if not self.modules:
            # Empty state
            empty_label = Gtk.Label(label="No services configured")
            empty_label.add_css_class("title-2")
            empty_label.add_css_class("dim-label")
            empty_label.set_vexpand(True)
            empty_label.set_valign(Gtk.Align.CENTER)
            self.content.append(empty_label)
        else:
            # Create cards for each module
            for module in self.modules:
                card = ServiceCard(module, self.refresh_all)
                self.cards.append(card)
                
                # Wrap in a frame
                frame = Gtk.Frame()
                frame.set_child(card)
                self.content.append(frame)
        
        # Update status
        if self.modules:
            running = sum(1 for m in self.modules if m.check_status())
            total = len(self.modules)
            self.status_label.set_text(f"{running} running, {total} total services")
    
    def auto_refresh(self):
        """Auto refresh timer"""
        for card in self.cards:
            card.update_status()
        return True  # Continue timer