# Theming Guide

Learn how to customize the appearance of Control Deck applications with CSS and theming.

## Built-in Themes

### Dark Mode (Default)

```python
config = DeckConfig(dark_mode=True)
```

Dark mode with Adwaita dark theme:
- Dark backgrounds
- Light text
- Blue accents
- High contrast borders

### Light Mode

```python
config = DeckConfig(dark_mode=False)
```

Light mode with standard Adwaita:
- Light backgrounds
- Dark text
- Blue accents
- Subtle borders

## Custom CSS

### Applying Custom Styles

```python
config = DeckConfig(
    custom_css="styles/custom.css"
)
```

Or inline CSS:

```python
deck = ControlDeck(config)
deck.apply_css("""
    .service-card {
        background: #1e3a5f;
        border-radius: 12px;
    }
""")
```

### CSS Class Reference

#### Container Classes

```css
/* Main window */
.control-deck-window {
    background: #0d1117;
}

/* Header bar */
.header-bar {
    background: #161b22;
    padding: 8px;
}

/* Main content area */
.content-area {
    padding: 12px;
}

/* Status bar */
.status-bar {
    background: #161b22;
    padding: 6px 12px;
    font-size: 0.9em;
}
```

#### Service Card Classes

```css
/* Service card container */
.service-card {
    background: #0d1117;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
    margin: 6px;
}

/* Card when service is running */
.service-card.running {
    border-left: 3px solid #3fb950;
}

/* Card when service is stopped */
.service-card.stopped {
    border-left: 3px solid #f85149;
}

/* Service name label */
.service-name {
    font-weight: bold;
    font-size: 1.1em;
}

/* Service status text */
.service-status {
    color: #8b949e;
    font-size: 0.9em;
}

/* Service details text */
.service-details {
    color: #8b949e;
    font-size: 0.85em;
    opacity: 0.8;
}
```

#### Button Classes

```css
/* All control buttons */
.service-button {
    min-width: 80px;
    padding: 4px 12px;
}

/* Start button */
.start-button {
    background: #238636;
    color: white;
}

.start-button:hover {
    background: #2ea043;
}

/* Stop button */
.stop-button {
    background: #da3633;
    color: white;
}

.stop-button:hover {
    background: #f85149;
}

/* Remove button */
.remove-button {
    background: #6e7681;
    color: white;
}

/* Refresh button in header */
.refresh-button {
    background: transparent;
}

.refresh-button:hover {
    background: rgba(255, 255, 255, 0.1);
}
```

## Docker-Themed Example

### Docker Blue Theme

```css
/* docker-theme.css */

/* Use Docker colors */
:root {
    --docker-blue: #2496ed;
    --docker-dark: #0d1117;
    --docker-gray: #161b22;
    --docker-light-gray: #30363d;
}

/* Window background */
.control-deck-window {
    background: var(--docker-dark);
}

/* Header with Docker blue */
.header-bar {
    background: linear-gradient(90deg, var(--docker-blue), #1a73e8);
    color: white;
}

/* Service cards */
.service-card {
    background: var(--docker-gray);
    border: 1px solid var(--docker-light-gray);
    border-radius: 12px;
    padding: 16px;
    margin: 8px;
    transition: all 0.3s ease;
}

.service-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(36, 150, 237, 0.2);
    border-color: var(--docker-blue);
}

/* Running services with blue glow */
.service-card.running {
    border-left: 4px solid var(--docker-blue);
    background: linear-gradient(90deg, 
        rgba(36, 150, 237, 0.1) 0%, 
        var(--docker-gray) 10%);
}

/* Buttons with Docker styling */
.service-button {
    background: var(--docker-blue);
    color: white;
    border: none;
    border-radius: 6px;
    padding: 6px 16px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.service-button:hover {
    background: #1a73e8;
    transform: scale(1.05);
}

.service-button:active {
    transform: scale(0.95);
}

/* Status bar */
.status-bar {
    background: var(--docker-gray);
    border-top: 1px solid var(--docker-light-gray);
    color: #8b949e;
    font-family: 'SF Mono', 'Monaco', 'Inconsolata', monospace;
}

/* Icons with Docker blue */
.service-icon {
    color: var(--docker-blue);
}
```

Apply the theme:

```python
config = DeckConfig(
    title="Docker Control",
    dark_mode=True,
    custom_css="styles/docker-theme.css"
)
```

## Material Design Theme

```css
/* material-theme.css */

/* Material Design colors */
:root {
    --md-primary: #6200ea;
    --md-primary-variant: #3700b3;
    --md-secondary: #03dac6;
    --md-background: #121212;
    --md-surface: #1e1e1e;
    --md-error: #cf6679;
    --md-on-primary: #ffffff;
    --md-on-surface: #e1e1e1;
}

/* Elevated cards with shadows */
.service-card {
    background: var(--md-surface);
    border: none;
    border-radius: 8px;
    padding: 16px;
    margin: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.service-card:hover {
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.6);
    transform: translateY(-4px);
}

/* Material buttons */
.service-button {
    background: var(--md-primary);
    color: var(--md-on-primary);
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    text-transform: uppercase;
    font-weight: 500;
    letter-spacing: 0.5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.service-button:hover {
    background: var(--md-primary-variant);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}

.service-button:active {
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
}

/* Floating Action Button style */
.refresh-button {
    background: var(--md-secondary);
    color: var(--md-background);
    border-radius: 50%;
    width: 48px;
    height: 48px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
}

/* Status indicators */
.service-card.running::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
    background: var(--md-secondary);
    border-radius: 4px 0 0 4px;
}
```

## Glassmorphism Theme

```css
/* glass-theme.css */

/* Modern glassmorphism effect */
.control-deck-window {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.content-area {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
}

.service-card {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    padding: 20px;
    margin: 10px;
    box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
}

.service-card:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
}

.service-button {
    background: rgba(255, 255, 255, 0.2);
    backdrop-filter: blur(5px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
}

.service-button:hover {
    background: rgba(255, 255, 255, 0.3);
    border-color: rgba(255, 255, 255, 0.4);
}
```

## Dynamic Theming

### Theme Switching

```python
class ThemedDeck(ControlDeck):
    def __init__(self, config):
        super().__init__(config)
        self.themes = {
            "default": "styles/default.css",
            "docker": "styles/docker.css",
            "material": "styles/material.css",
            "glass": "styles/glass.css"
        }
        self.current_theme = "default"
    
    def switch_theme(self, theme_name: str):
        """Switch to a different theme"""
        if theme_name in self.themes:
            css_file = self.themes[theme_name]
            with open(css_file) as f:
                css = f.read()
            self.apply_css(css)
            self.current_theme = theme_name
    
    def create_theme_menu(self):
        """Create theme selection menu"""
        menu = Gtk.PopoverMenu()
        
        for theme_name in self.themes:
            item = Gtk.Button(label=theme_name.title())
            item.connect("clicked", 
                        lambda w, t=theme_name: self.switch_theme(t))
            menu.add(item)
        
        return menu
```

### Color Scheme Detection

```python
def get_system_color_scheme():
    """Detect system color scheme preference"""
    settings = Gtk.Settings.get_default()
    return settings.get_property("gtk-application-prefer-dark-theme")

def apply_system_theme(deck: ControlDeck):
    """Apply theme based on system preference"""
    if get_system_color_scheme():
        deck.apply_css(load_dark_theme())
    else:
        deck.apply_css(load_light_theme())
```

## Animated Effects

### CSS Animations

```css
/* Pulse animation for running services */
@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(36, 150, 237, 0.7);
    }
    70% {
        box-shadow: 0 0 0 10px rgba(36, 150, 237, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(36, 150, 237, 0);
    }
}

.service-card.running {
    animation: pulse 2s infinite;
}

/* Slide in animation for cards */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.service-card {
    animation: slideIn 0.3s ease-out;
}

/* Loading spinner */
@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.loading {
    animation: spin 1s linear infinite;
}
```

## Responsive Design

### Adaptive Layouts

```css
/* Compact mode for small windows */
@media (max-width: 600px) {
    .service-card {
        padding: 8px;
        margin: 4px;
    }
    
    .service-button {
        min-width: 60px;
        padding: 4px 8px;
        font-size: 0.9em;
    }
    
    .service-details {
        display: none;
    }
}

/* Wide layout for large screens */
@media (min-width: 1200px) {
    .content-area {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 16px;
    }
    
    .service-card {
        margin: 0;
    }
}
```

## Icon Theming

### Custom Icon Sets

```python
config = DeckConfig(
    icon_theme="Papirus-Dark"  # Or "Adwaita", "Breeze", etc.
)
```

### Icon Overrides

```python
class ThemedModule(ServiceModule):
    def get_icon(self):
        if self.check_status():
            return "custom-running-icon"
        return "custom-stopped-icon"
```

### SVG Icons

```python
def create_custom_icon():
    """Create custom SVG icon"""
    svg = """
    <svg width="24" height="24" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="10" fill="#2496ed"/>
        <path d="M9 12l2 2 4-4" stroke="white" stroke-width="2"/>
    </svg>
    """
    return Gtk.Picture.new_for_filename("data:image/svg+xml," + svg)
```

## Font Customization

```css
/* Custom fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.control-deck-window {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
}

.service-name {
    font-weight: 600;
    font-size: 14px;
    letter-spacing: -0.01em;
}

.service-status {
    font-weight: 500;
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.service-details {
    font-family: 'SF Mono', 'Consolas', monospace;
    font-size: 11px;
}
```

## Accessibility

### High Contrast Theme

```css
/* high-contrast.css */

.control-deck-window {
    background: #000000;
    color: #ffffff;
}

.service-card {
    background: #000000;
    border: 2px solid #ffffff;
}

.service-card:focus {
    outline: 3px solid #ffff00;
    outline-offset: 2px;
}

.service-button {
    background: #ffffff;
    color: #000000;
    border: 2px solid #ffffff;
    font-weight: bold;
}

.service-button:hover {
    background: #000000;
    color: #ffffff;
}

/* Ensure sufficient color contrast */
.service-status {
    color: #00ff00;  /* Green for running */
}

.service-card.stopped .service-status {
    color: #ff0000;  /* Red for stopped */
}
```

## Best Practices

1. **Test in both light and dark modes**
2. **Ensure sufficient color contrast (WCAG 2.1)**
3. **Use CSS variables for maintainability**
4. **Provide smooth transitions**
5. **Test on different screen sizes**
6. **Keep animations subtle and optional**
7. **Support system theme preferences**

## Debugging Styles

### GTK Inspector

```bash
GTK_DEBUG=interactive ./my-deck.py
```

Use GTK Inspector to:
- Inspect element hierarchy
- View applied CSS
- Test CSS changes live
- Check computed styles

### CSS Logging

```python
def debug_css(deck: ControlDeck):
    """Print CSS debugging info"""
    css_provider = deck.css_provider
    print(f"CSS loaded: {css_provider is not None}")
    
    # List all style contexts
    for widget in deck.window.get_children():
        context = widget.get_style_context()
        classes = context.list_classes()
        print(f"Widget: {widget}, Classes: {classes}")
```

## See Also

- [Configuration](configuration.md)
- [Getting Started](getting-started.md)
- [Examples](examples.md)