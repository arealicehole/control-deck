# Control Deck Documentation

Complete documentation for the Control Deck service control panel framework.

## Table of Contents

1. [Getting Started](getting-started.md) - Installation and first app
2. [Plugin Development](plugin-development.md) - Creating service modules
3. [API Reference](api-reference.md) - Complete API documentation
4. [Configuration](configuration.md) - Customizing your deck
5. [Plugin Manager](plugin-manager.md) - Managing plugins via UI
6. [Examples](examples.md) - Sample implementations
7. [Theming](theming.md) - Custom CSS and theming
8. [Troubleshooting](troubleshooting.md) - Common issues and solutions

## Quick Links

- [GitHub Repository](https://github.com/arealicehole/control-deck)
- [Example Plugins](../examples/plugins/)
- [Plugin Directory](../plugins/)

## What is Control Deck?

Control Deck is a lightweight, extensible framework for building service control panels with GTK4/Adwaita. It provides:

- A clean, modern UI with automatic layouts
- Plugin-based architecture for adding services
- Built-in refresh, theming, and state management
- Cross-platform support (Linux, Windows, macOS)

## Architecture

```
┌─────────────────────────────────────┐
│         Control Deck App            │
│  ┌─────────────────────────────┐    │
│  │     Header Bar              │    │
│  │  [↻] Refresh  [🧩] Plugins  │    │
│  └─────────────────────────────┘    │
│  ┌─────────────────────────────┐    │
│  │     Service Cards           │    │
│  │  ┌───────────────────┐      │    │
│  │  │ Service Module 1   │      │    │
│  │  │ [Status] [Toggle]  │      │    │
│  │  └───────────────────┘      │    │
│  │  ┌───────────────────┐      │    │
│  │  │ Service Module 2   │      │    │
│  │  │ [Status] [Toggle]  │      │    │
│  │  └───────────────────┘      │    │
│  └─────────────────────────────┘    │
│  Status: 2 running, 3 total         │
└─────────────────────────────────────┘
```

## License

MIT License - See [LICENSE](../LICENSE) file for details.