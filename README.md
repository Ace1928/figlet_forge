# 🔠 Figlet Forge

> _"Typography crystallized into ASCII art perfection"_

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with Eidosian Principles](https://img.shields.io/badge/Made%20with-Eidosian_Principles-8A2BE2)](https://github.com/Ace1928)

[![Version](https://img.shields.io/badge/Version-1.0.2-blue)](https://github.com/Ace1928/figlet_forge)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Forge System](https://img.shields.io/badge/Forge-System-8A2BE2)](https://github.com/Ace1928)

```ascii
   _______ _       __     __  ______
  / ____(_) /____ / /__  / /_/ ____/___  _________  ____
 / /_  / / __/ _ \/ / _ \/ __/ /_  / __ \/ ___/ __ \/ __ \
/ __/ / / /_/  __/ /  __/ /_/ __/ / /_/ / /  / /_/ / /_/ /
/_/   /_/\__/\___/_/\___/\__/_/    \____/_/   \____/ .___/
                                                  /_/
```

**Figlet Forge** is an Eidosian reimplementation extending the original pyfiglet package with enhanced features, while maintaining complete backward compatibility.

## ✨ Features

- **📊 Full colorized ANSI code support** for vibrant text art with foreground and background colors
- **🌍 Unicode character rendering** with comprehensive mapping for global language support
- **🗃️ Expanded font ecosystem** with careful attention to licensing and compatibility
- **🔄 Intelligent fallbacks** for complete backward compatibility with older systems
- **🚀 Significant performance optimizations** without sacrificing quality
- **🧩 Enhanced maintainability** through modern Python practices and typing
- **📚 Comprehensive documentation** for all use cases
- **♻️ Full backward compatibility** with pyfiglet

## 🚀 Quick Start

### Installation

```bash
pip install figlet-forge
```

### Basic Usage

```python
from figlet_forge import Figlet
from figlet_forge import print_figlet

# Simple rendering
fig = Figlet(font="slant")
result = fig.renderText("Hello, world!")
print(result)

# Colorized output
print_figlet("Colorful Text", font="big", colors="RED:BLUE")
```

## 🔮 Advanced Features

### Color Support

```python
# Syntax: foreground:background
print_figlet("Warning!", font="standard", colors="RED:YELLOW")

# RGB support
print_figlet("Custom", font="slant", colors="255;128;0:0;0;128")
```

### Unicode Support

```python
# Enable Unicode rendering
fig = Figlet(font="standard", unicode_aware=True)
print(fig.renderText("こんにちは世界"))

# Right-to-left languages
fig = Figlet(font="standard", direction="right-to-left")
print(fig.renderText("مرحبا بالعالم"))
```

## 📋 Command Line Interface

```bash
# Basic usage
figlet_forge "Hello world"

# Select a font with colors
figlet_forge -f slant -c "RED:BLUE" "Cool Text"

# Unicode support with centered justification
figlet_forge -u -w 60 -j center "こんにちは世界"
```

## 📚 Documentation

Full documentation is available at [figlet-forge.readthedocs.io](https://figlet-forge.readthedocs.io/)

## 🤝 Contributing

Contributions are welcome! Check out our [contribution guidelines](CONTRIBUTING.md) to get started.

## 📜 License

Figlet Forge is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Original pyfiglet copyright © 2007-2023 belongs to the original pyfiglet authors.
Figlet Forge extensions copyright © 2023-2025 Lloyd Handyside and Eidosian Forge contributors.
