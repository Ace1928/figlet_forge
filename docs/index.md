# docs/index.rst
=============
Figlet Forge
=============

**Figlet Forge** is an Eidosian reimplementation extending the original pyfiglet
package with colorized ANSI support, Unicode rendering, and intelligent fallbacks.

.. image:: https://img.shields.io/badge/Forge-System-8A2BE2

Features
=========

- Full colorized ANSI code support for vibrant text art
- Unicode character rendering with comprehensive mapping
- Expanded font ecosystem with careful attention to licensing
- Intelligent fallbacks for compatibility with older systems
- Significant performance optimizations without sacrificing quality
- Enhanced maintainability through modern Python practices
- Comprehensive documentation for all use cases
- Full backward compatibility with pyfiglet

Getting Started
===============

Installation
-----------

.. code-block:: bash

   pip install figlet-forge

Basic Usage
-----------

.. code-block:: python

   from figlet_forge import print_figlet

   # Basic usage
   print_figlet("Hello World")

   # With a specific font
   print_figlet("Hello World", font="slant")

   # With colors
   from figlet_forge import colored_format
   print(colored_format("Hello World", font="big", fg="blue", bg="white"))

Table of Contents
=================

.. toctree::
   :maxdepth: 2

   api/index
   examples/index
   fonts/index
