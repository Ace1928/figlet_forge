# **figlet_forge**

```ascii
  _____ _       _      _     _____
   |  ___(_) __ _| | ___| |_  |  ___|__  _ __ __ _  ___
   | |_  | |/ _` | |/ _ \ __| | |_ / _ \| '__/ _` |/ _ \
   |  _| | | (_| | |  __/ |_  |  _| (_) | | | (_| |  __/
   |_|   |_|\__, |_|\___|\__| |_|  \___/|_|  \__, |\___|
      |___/                            |___/
```

## **Synopsis**

Figlet Forge is an Eidosian reimplementation and extension of pyfiglet (which itself is a port of [FIGlet](http://www.figlet.org/) into pure Python). It renders text as ASCII art typography with significant enhancements and optimizations.

Building upon pyfiglet's foundation, Figlet Forge adds robust support for colorized ANSI codes, full Unicode character rendering, an expanded font ecosystem, and intelligent fallback mechanisms that ensure backward compatibility with older systems.

## **Key Improvements**

- **Colorized Output**: Full ANSI color support for vibrant text art
- **Unicode Compatibility**: Render any Unicode character with appropriate mappings
- **Enhanced Font Ecosystem**: Expanded library with careful attention to licensing
- **Intelligent Fallbacks**: Automatic degradation for compatibility with legacy systems
- **Performance Optimization**: Significantly faster rendering without sacrificing quality
- **API Extensions**: New capabilities while maintaining full backward compatibility
- **Comprehensive Documentation**: Clear guides for all usage scenarios

## **FAQ**

- **Q**: How is this different from the original pyfiglet?

  **A**: Figlet Forge extends pyfiglet with colorized text, Unicode support, enhanced performance, and intelligent fallbacks while maintaining 100% backward compatibility.

- **Q**: Will my existing pyfiglet code work with Figlet Forge?

  **A**: Yes! We've ensured complete API compatibility. Simply replace import statements and enjoy the enhancements.

- **Q**: Does it support kerning/smushing like the original?

  **A**: Yes, all original functionality is preserved and optimized, including kerning and smushing. Output quality matches or exceeds the original.

- **Q**: Can I use/modify/redistribute this code?

  **A**: Yes, under the terms of the MIT license (see LICENSE below).

- **Q**: I've improved the code, what should I do with it?

  **A**: Please submit changes via pull request. For kerning/mushing/rendering changes, include thorough testing as this code is both powerful and complex.

- **Q**: Why are some fonts missing in my distribution?

  **A**: Some Linux distributions have strict legal requirements. We've organized fonts into standard (clear licensing) and contrib (other licenses) directories.

- **Q**: How do I use the new color features?

  **A**: The color API is detailed in our documentation. Basic usage: `figlet_forge.colored_format("text", font="slant", fg="red", bg="black")`.

- **Q**: What about Unicode support limitations?

  **A**: While we support full Unicode, rendering quality depends on font completeness. Our intelligent fallbacks will substitute approximations when needed.

## **Usage**

You can use Figlet Forge in two ways:

### Command line interface

```bash
figlet_forge 'text to render'
```

Run with `--help` to see all options, including color controls, Unicode options, and font selection.

### As a Python library

```py
from figlet_forge import Figlet
f = Figlet(font='slant')
print(f.renderText('text to render'))
```

Or with the simplified interface:

```py
import figlet_forge
f = figlet_forge.figlet_format("text to render", font="slant")
print(f)
```

Using the new color features:

```py
import figlet_forge
colored_text = figlet_forge.colored_format("Rainbow Text", font="slant",
                       color_mode="rainbow")
print(colored_text)
```

To install custom fonts:

```bash
figlet_forge --load-font <font_file>
```

The font file can be a ZIP of multiple fonts or a single font file. Administrative privileges may be needed depending on your installation.

## **Author & Contributors**

Figlet Forge is an Eidosian reimplementation developed by Lloyd Handyside, building upon:

- Original pyfiglet by Christopher Jones (<cjones@insub.org>)
- Packaging by Peter Waller (<p@pwaller.net>)
- Enhancements by Stefano Rivera (<stefano@rivera.za.net>)
- And many other contributors to the original project

Figlet Forge maintains the spirit of the original code while significantly enhancing its capabilities, performance, and future-proofness.

The original FIGlet authors are listed on their website at <http://www.figlet.org/>.

## **Integration with Eidosian Forge**

Figlet Forge serves as a central component of the Eidosian Forge ecosystem, providing typography services, text crystallization, and visual communication tools for other Forge components. It exemplifies the Eidosian principles of extending and enhancing existing tools while maintaining strict backwards compatibility.

## **License**

The MIT License (MIT)
Copyright © 2007-2023 Original pyfiglet authors
Copyright © 2023-2024 Lloyd Handyside and Eidosian Forge contributors

```markdown
Christopher Jones <cjones@insub.org>
Stefano Rivera <stefano@rivera.za.net>
Peter Waller <p@pwaller.net>
Lloyd Handyside <ace1928@gmail.com>
And various contributors (see git history).
```

(see LICENSE for full details)

## Packaging status

[![Packaging status](https://repology.org/badge/vertical-allrepos/python:figlet-forge.svg)](https://repology.org/project/python:figlet-forge/versions)
