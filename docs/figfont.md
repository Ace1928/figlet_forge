╔═══════════════════════════════════════════════════════════════════════════╗
║ ███████╗██╗ ██████╗ ███████╗ ██████╗ ███╗ ██╗████████╗ ║
║ ██╔════╝██║██╔════╝ ██╔════╝██╔═══██╗████╗ ██║╚══██╔══╝ ║
║ █████╗ ██║██║ ███╗█████╗ ██║ ██║██╔██╗ ██║ ██║ ║
║ ██╔══╝ ██║██║ ██║██╔══╝ ██║ ██║██║╚██╗██║ ██║ ║
║ ██║ ██║╚██████╔╝██║ ╚██████╔╝██║ ╚████║ ██║ ║
║ ╚═╝ ╚═╝ ╚═════╝ ╚═╝ ╚═════╝ ╚═╝ ╚═══╝ ╚═╝ ║
╚═══════════════════════════════════════════════════════════════════════════╝

           ⚜️ The FIGfont Version 2 FIGfont and FIGdriver Standard ⚜️
           ═══ ═══════ ═══════ ═ ═══════ ═══ ═════════ ════════
              Draft 2.0 Copyright 1996, 1997
              by John Cowan and Paul Burton
              Portions Copyright 1991, 1993, 1994
              by Glenn Chappell and Ian Chai
              May be freely copied and distributed.

              ⟡ Eidosian Edition 2025 ⟡
              Figlet Forge: The Eidosian Typography Engine

             📍 Original Figlet: http://www.figlet.org/

      ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
      ┃  _____          __           __                            ┃
      ┃ / ___/__  ___  / /____ ___  / /____                        ┃
      ┃/ /__/ _ \/ _ \/ __/ -_) _ \/ __(_-<                        ┃
      ┃\___/\___/_//_/\__/\__/_//_/\__/___/                        ┃
      ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

        ╭─────────────────────────────────────────────────────╮
        │ ◈ INTRODUCTION                                      │
        │ ◈ BASIC DEFINITIONS AND CONCEPTS                    │
        │   • "FIGfont"                                       │
        │   • "FIGcharacters" and "Sub-characters"            │
        │   • "FIGdriver"                                     │
        │   • "FIGure"                                        │
        │   • "FIG"                                           │
        │   • "Layout Modes"                                  │
        │   • "Smushing Rules"                                │
        │   • "Hardblanks"                                    │
        │ ◈ CREATING FIGFONTS                                 │
        │   • The Header Line                                 │
        │   • Interpretation of Layout Parameters             │
        │   • Setting Layout Parameters Step-by-Step          │
        │   • FIGfont Comments                                │
        │   • FIGcharacter Data                               │
        │     - Basic Data Structure                          │
        │     - Character Codes                               │
        │     - Required FIGcharacters                        │
        │     - Code Tagged FIGcharacters                     │
        │ ◈ NOTES - AVOIDING ERRORS AND GENERAL ADVICE        │
        │ ◈ CONTROL FILES                                     │
        │   • Standard Format                                 │
        │   • Extended Commands                               │
        │ ◈ STANDARDIZED CAPABILITIES OF CURRENT AND FUTURE   │
        │   FIGDRIVERS                                        │
        │ ◈ CHART OF CAPABILITIES OF FIGLET 2.2.1 AND         │
        │   FIGWIN 1.0                                        │
        ╰─────────────────────────────────────────────────────╯

# 🔍 INTRODUCTION

This document specifies the format of font files and associated control files used by
FIGlet and FIGWin programs (collectively known as FIGdrivers). It serves as a
comprehensive reference for designers creating fonts (FIGfonts) compatible with these
systems and establishes standards for future FIGdriver development.

┌─────────────────────────────────────────────────────────────────────┐
│ 📝 PURPOSE: │
│ • Define standard font file format specifications │
│ • Document control file structures and behaviors │
│ • Establish compatibility guidelines across implementations │
│ • Serve as canonical reference for font designers │
└─────────────────────────────────────────────────────────────────────┘

Note that some features described in this document may not be supported by all
FIGdriver implementations. Consult program-specific documentation for details on
using FIGlet or FIGWin directly.

> ⚠️ **IMPLEMENTATION NOTE**: FIGWin 1.0 includes a program called FIGfont Editor
> for Windows 1.0 that simplifies font creation without requiring complete
> understanding of this specification. However, familiarity with the "BASIC
> DEFINITIONS AND CONCEPTS" section is still recommended for effective use.

## 📤 CONTRIBUTING FONTS

If you design a FIGfont, please share it with the community:

1. Send an announcement email to the FIGlet fonts mailing list:
   <figletfonts@figlet.org>

2. Submit a copy to <info@figlet.org> for potential inclusion in the
   official repository at ftp://ftp.figlet.org/

🔄 Contributing your work helps maintain a vibrant ecosystem of ASCII typography
resources for all users.

# 🧩 BASIC DEFINITIONS AND CONCEPTS

This section introduces the fundamental terminology and concepts needed to understand FIGlet typography. Each concept builds on the previous, creating a scaffolding of knowledge that enables both usage and extension of the FIGlet system.

## "FIGfont" 🔤

A FIGfont is a file which represents the graphical arrangement of characters representing larger characters. Since a FIGfont file is a text file, it can be created with any text editing program on any platform. The filename of a FIGfont file must end with ".flf", which stands for "<F>IG<L>ettering <F>ont".

```ascii
┌───────────────────────────────────────────────────────────┐
│ 📂 FIGfont = Typography patterns crystallized into text  │
└───────────────────────────────────────────────────────────┘
```

## "FIGcharacters" and "Sub-characters" 📝

Because FIGfonts describe large characters which consist of smaller characters, confusion can result when discussing one or the other. Therefore, the terms "FIGcharacter" and "sub-character" are used, respectively.

```ascii
╭───────────────────────────────────────────────────────────╮
│ ╭───╮  ← This entire structure is a FIGcharacter         │
│ │ A │  ← These individual characters are sub-characters  │
│ ╰───╯                                                    │
╰───────────────────────────────────────────────────────────╯
```

## "FIGdriver" ⚙️

The term FIGdriver is used in this document to encompass FIGlet, FIGWin, and any future programs which use FIGfonts.

## "FIGure" 🖼️

A FIGure (thusly capitalized) is an image created by a FIGdriver.

## "FIG" 📜 Evolution History

> _"Understanding where we've been illuminates the path ahead."_ — Eidosian Principle 4.7

A bit of history:

In Spring 1991, inspired by the Email signature of a friend named Frank, and goaded on by Ian Chai, Glenn Chappell wrote a nifty little 170-line "C" program called "newban", which would create large letters out of ordinary text characters. At the time, it was only compiled for UNIX. In hindsight, we now call it "FIGlet 1.0". FIGlet stands for <F>rank, <I>an, and <G>lenn's <let>ters. In various incarnations, newban circulated around the net for a couple of years. It had one font, which included only lowercase letters.

```ascii
┌──────────────────────────────────────────────────────────┐
│ 🌱 EVOLUTIONARY TIMELINE                                │
│                                                        │
│ ┌────────────┐  ┌─────────┐  ┌──────────┐  ┌────────┐  │
│ │ newban 1.0 │→ │FIGlet 2.0│→│FIGlet 2.1│→│FIGlet 2.2│  │
│ │ 170 lines  │  │ 888 lines│  │1314 lines│  │4800 lines│  │
│ └────────────┘  └─────────┘  └──────────┘  └────────┘  │
│      1991         1993         1994-1995      1996      │
└──────────────────────────────────────────────────────────┘
```

In early 1993, Ian decided newban was due for a few changes, so together Ian and Glenn added the full ASCII character set, to start with. First, though, Ian had to find a copy of the source, since Glenn had tossed it away as not worth the disk space. Ian and Glenn discussed what could be done with it, decided on a general re-write, and, 7 months later, ended up with 888 lines of code, 13 FIGfonts and documentation. This was FIGlet 2.0, the first real release.

To their great surprise, FIGlet took the net by storm. They received floods of "FIGlet is great!" messages and a new contributed FIGfont about once a week. To handle all the traffic, Ian quickly set up a mailing list, Daniel Simmons kindly offered space for an FTP site, several people volunteered to port FIGlet to non-Unix operating systems, ...and bug reports poured in.

Because of these, and the need to make FIGlet more "international", Ian and Glenn released a new version of FIGlet which could handle non-ASCII character sets and right-to-left printing. This was FIGlet 2.1, which, in a couple of weeks, became figlet 2.1.1. This weighed in at 1314 lines, and there were over 60 FIGfonts.

By late 1996, FIGlet had quite a following of fans subscribing to its mailing list. It had been ported to MS-DOS, Macintosh, Amiga, Apple II GS, Atari ST, Acorn and OS/2. FIGlet had been further updated, and there were nearly 200 FIGfonts.

John Cowan and Paul Burton are two FIGlet fans who decided to create new versions. While John wrote FIGlet version 2.2 using C, Paul wrote FIGWin 1.0, the first true GUI (Windows) implementation of FIGlet, using Visual Basic. John and Paul worked together to add new features to FIGfont files which could be read by both programs, and together wrote this document, which we hope helps to establish consistency in FIGfonts and help with the creation of future FIGdrivers. FIGlet 2.2 has about 4800 lines of code, of which over half is a support library for reading compressed files.

FIGlet 2.2 and FIGWin 1.0 both allow greater flexibility by use of new information which can be contained in FIGfont files without interfering with the function of older FIGdrivers.

> ⚠️ **HISTORICAL NOTE**: The Macintosh version of FIGlet (as of 1997) was still command-line driven, and a GUI version was in demand. The FIGlet C code was written to be easily plugged into a GUI shell.

## "Layout Modes" 📐

A FIGdriver may arrange FIGcharacters using one of three "layout modes", which define the spacing between FIGcharacters. The layout mode for the horizontal axis may differ from the layout mode for the vertical axis. A default choice is defined for each axis by every FIGfont.

```ascii
┌────────────────────────────────────────────────────────────┐
│ LAYOUT MODES VISUALIZED:                                   │
│                                                            │
│ ┌─────┐ ┌─────┐  │  ┌─────┐┌─────┐  │  ┌─────┐─────┐       │
│ │  A  │ │  B  │  │  │  A  ││  B  │  │  │  A  │  B  │       │
│ └─────┘ └─────┘  │  └─────┘└─────┘  │  └─────┘─────┘       │
│ Full Size        │  Fitting Only    │  Smushing            │
└────────────────────────────────────────────────────────────┘
```

The three layout modes are:

### Full Size (Separately called "Full Width" or "Full Height")

Represents each FIGcharacter occupying the full width or height of its arrangement of sub-characters as designed.

### Fitting Only (Separately called "Kerning" or "Vertical Fitting")

Moves FIGcharacters closer together until they touch. Typographers use the term "kerning" for this phenomenon when applied to the horizontal axis, but fitting also includes this as a vertical behavior, for which there is apparently no established typographical term.

### Smushing (Same term for both axes)

Moves FIGcharacters one step closer after they touch, so that they partially occupy the same space. A FIGdriver must decide what sub-character to display at each junction. There are two ways of making these decisions: by controlled smushing or by universal smushing.

- **Controlled smushing** uses a set of "smushing rules" selected by the designer of a FIGfont. (See "Smushing Rules" below.) Each rule is a comparison of the two sub-characters which must be joined to yield what to display at the junction. Controlled smushing will not always allow smushing to occur, because the compared sub-characters may not correspond to any active rule. Wherever smushing cannot occur, fitting occurs instead.

- **Universal smushing** simply overrides the sub-character from the earlier FIGcharacter with the sub-character from the later FIGcharacter. This produces an "overlapping" effect with some FIGfonts, wherein the latter FIGcharacter may appear to be "in front".

A FIGfont which does not specify any smushing rules for a particular axis indicates that universal smushing is to occur when smushing is requested. Therefore, it is not possible for a FIGfont designer to "forbid" smushing. However, there are ways to ensure that smushing does not cause a FIGfont to be illegible when smushed. This is especially important for smaller FIGfonts. (See "Hardblanks" for details.)

> 🔍 **TECHNICAL NOTE**: For vertical fitting or smushing, entire lines of output FIGcharacters are "moved" as a unit.

Not all FIGdrivers do vertical fitting or smushing. At present, FIGWin 1.0 does, but FIGlet 2.2 does not. Further, while FIGlet 2.2 allows the user to override the FIGfont designer's set of smushing rules, FIGWin 1.0 does not.

> ⚙️ **IMPLEMENTATION NOTE**: In FIGlet versions prior to 2.2, the term "smushmode" was used to mean the layout mode, and this term further included the smushing rules (if any) to be applied. However, since the layout mode may or may not involve smushing, more recent documentation uses more precise terminology.

## "Smushing Rules" 🧩

> _"Precise character interaction creates typographic elegance."_ — Eidosian Typography Principle 2.3

Again, smushing rules are for controlled smushing. If none are defined to be active in a FIGfont, universal smushing occurs instead.

Generally, if a FIGfont is "drawn at the borders" using sub-characters "-\_|/\[]{}()<>", you will want to use controlled smushing by selecting from the rules below. Otherwise, if your FIGfont uses a lot of other sub-characters, do not select any rules and universal smushing will occur instead. (See "Hardblanks" below if your FIGfont is very small and would become illegible if smushed.) Experimentation is the best way to make these decisions.

```ascii
┌───────────────────────────────────────────────────────────────────────────┐
│ 🔍 RULE SELECTION GUIDANCE:                                              │
│                                                                           │
│ Border-drawn fonts (using "-_|/\[]{}()<>") → Use controlled smushing      │
│ Complex character fonts                    → Universal smushing preferred │
│ Small/compact fonts                        → Consider hardblanks          │
│                                                                           │
│ 🧪 Always experiment with different combinations to find optimal results! │
└───────────────────────────────────────────────────────────────────────────┘
```

There are six possible horizontal smushing rules and five possible vertical smushing rules. Below is a description of all of the rules.

> ⚠️ **NOTE**: Ignore the "code values" for now. They are explained later in the document.

### The Six Horizontal Smushing Rules

#### Rule 1: EQUAL CHARACTER SMUSHING (code value 1)

Two sub-characters are smushed into a single sub-character if they are the same. This rule does not smush hardblanks. (See "Hardblanks" below.)

#### Rule 2: UNDERSCORE SMUSHING (code value 2)

An underscore ("\_") will be replaced by any of: "|", "/", "\\", "[", "]", "{", "}", "(", ")", "<" or ">".

#### Rule 3: HIERARCHY SMUSHING (code value 4)

A hierarchy of six classes is used: "|", "/\\", "[]", "{}", "()", and "<>". When two smushing sub-characters are from different classes, the one from the latter class will be used.

#### Rule 4: OPPOSITE PAIR SMUSHING (code value 8)

Smushes opposing brackets ("[]" or "]["), braces ("{}" or "}{") and parentheses ("()" or ")(") together, replacing any such pair with a vertical bar ("|").

#### Rule 5: BIG X SMUSHING (code value 16)

Smushes "/\\" into "|", "\\/" into "Y", and "><" into "X". Note that "<>" is not smushed in any way by this rule. The name "BIG X" is historical; originally all three pairs were smushed into "X".

#### Rule 6: HARDBLANK SMUSHING (code value 32)

Smushes two hardblanks together, replacing them with a single hardblank. (See "Hardblanks" below.)

### The Five Vertical Smushing Rules

#### Rule 1: EQUAL CHARACTER SMUSHING (code value 256)

Same as horizontal smushing rule 1.

#### Rule 2: UNDERSCORE SMUSHING (code value 512)

Same as horizontal smushing rule 2.

#### Rule 3: HIERARCHY SMUSHING (code value 1024)

Same as horizontal smushing rule 3.

#### Rule 4: HORIZONTAL LINE SMUSHING (code value 2048)

Smushes stacked pairs of "-" and "\_", replacing them with a single "=" sub-character. It does not matter which is found above the other. Note that vertical smushing rule 1 will smush IDENTICAL pairs of horizontal lines, while this rule smushes horizontal lines consisting of DIFFERENT sub-characters.

#### Rule 5: VERTICAL LINE SUPERSMUSHING (code value 4096)

This one rule is different from all others, in that it "supersmushes" vertical lines consisting of several vertical bars ("|"). This creates the illusion that FIGcharacters have slid vertically against each other. Supersmushing continues until any sub-characters other than "|" would have to be smushed. Supersmushing can produce impressive results, but it is seldom possible, since other sub-characters would usually have to be considered for smushing as soon as any such stacked vertical lines are encountered.

```ascii
┌────────────────────────────────────────────────────────────────────┐
│ VERTICAL LINE SUPERSMUSHING VISUALIZATION:                         │
│                                                                    │
│ Original:                │ After Supersmushing:                    │
│  ┌─────┐                 │  ┌─────┐                                │
│  │  A  │                 │  │  A  │                                │
│  └─────┘                 │  └─────┘                                │
│    │                     │    │                                    │
│    │                     │  ┌─┴───┐                                │
│  ┌─┴───┐                 │  │  B  │                                │
│  │  B  │                 │  └─────┘                                │
│  └─────┘                 │                                         │
└────────────────────────────────────────────────────────────────────┘
```

## "Hardblanks" 🔲

A hardblank is a special sub-character which is displayed as a blank (space) in rendered FIGures, but is treated more like a "visible" sub-character when fitting or smushing horizontally. Therefore, hardblanks keep adjacent FIGcharacters a certain distance apart.

> 🔍 **TECHNICAL NOTE**: Hardblanks act the same as blanks for vertical operations.

### Hardblanks have three purposes

#### 1️⃣ Hardblanks are used to create the blank (space) FIGcharacter

Usually the space FIGcharacter is simply one or two vertical columns of hardblanks. Some slanted FIGfonts have a diagonal arrangement of hardblanks instead.

#### 2️⃣ Hardblanks can prevent "unreasonable" fitting or smushing

Normally when fitting or smushing, the blank (space) sub-character is considered "vacant space". In the following example, a capital "C" FIGcharacter is smushed with a "minus" FIGcharacter.

```
        ______                        ______
       / ____/                       / ____/
      / /      ____  >>-Becomes->   / /  ____
     / /___   /___/                / /__/___/
     \____/                        \____/
```

The FIGure above looks like a capital G. To prevent this, a FIGfont designer might place a hardblank in the center of the capital C. In the following example, the hardblank is represented as a "$":

```
        ______                        ______
       / ____/                       / ____/
      / /  $   ____  >>-Becomes->   / /   ____
     / /___   /___/                / /___/___/
     \____/                        \____/
```

Using hardblanks in this manner ensures that FIGcharacters with a lot of empty space will not be unreasonably "invaded" by adjacent FIGcharacters. Generally, FIGcharacters such as capital C, L or T, or small punctuation marks such as commas, may contain hardblanks, since they may contain a lot of vacant space which is "accessible" from either side.

#### 3️⃣ Hardblanks can prevent smushing from making FIGfonts illegible

This legitimate purpose of hardblanks is often overused. If a FIGfont designer is absolutely sure that smushing "visible" sub-characters would make their FIGfont illegible, hardblanks may be positioned at the end of each row of sub-characters, against the visible sub-characters, creating a barrier.

With older FIGdrivers, using hardblanks for this purpose meant that FIGcharacters would have to be separated by at least one blank in output FIGures, since only a hardblank could smush with another hardblank. However with the advent of universal smushing, this is no longer necessary. Hardblanks ARE overriden by any visible sub-character when performing universal smushing. Hardblanks still represent a "stopping point", but only AFTER their locations are occupied.

> ⚠️ **IMPORTANT**: Earlier it was stated that universal smushing overrides the sub-character from the former FIGcharacter with the sub-character from the latter FIGcharacter. Hardblanks (and blanks or spaces) are the exception to this rule; they will always be overriden by visible sub-characters, regardless of which FIGcharacter contains the hardblank. This ensures that no visible sub-characters "disappear".

Therefore, one can design a FIGfont with a default behavior of universal smushing, while the output FIGure would LOOK like the effect of fitting, or even full size if additional hardblanks are used. If a user "scales down" the layout mode to fitting, the result would look like "extra spacing" between FIGcharacters.

Taking this concept further, a FIGcharacter may also include extra blanks (spaces) on the left side of each FIGcharacter, which would define the FIGcharacter's width as slightly larger than required for the visible sub-characters and hardblanks. With such a FIGfont, a user who further "scales down" the layout mode to full size would see even greater spacing.

These techniques prevent horizontal smushing from causing a FIGfont to become illegible, while offering greater flexibility of output to users.

> 🔄 **DESIGN PHILOSOPHY NOTE**: These techniques cannot be used to prevent vertical smushing of visible sub-characters, since hardblanks are not respected in the vertical axis. Although it is possible to select only one vertical smushing rule which involves only sub-characters which are not used in your FIGfont, it is recommended that you do NOT do so. In our opinion, most users would prefer to get what they ask for, rather than being told, in effect: "I, the FIGfont designer, have decided that you wouldn't like the results of vertical smushing, so I have prevented you from trying it." Instead, we recommend setting the default behavior to either fitting or full height, and either allowing universal smushing, or selecting vertical smushing rules which seem most appropriate. A user of your FIGfont will quickly see why you did not choose smushing as the default vertical layout mode, and will agree with you.

```ascii
┌────────────────────────────────────────────────────────────────────────┐
│ 💡 TYPOGRAPHY TIP:                                                     │
│                                                                        │
│ When designing FIGfonts, think of hardblanks as the "personal space"   │
│ of your characters—they establish boundaries that respect the integrity │
│ of each glyph while still allowing for dynamic layout options.         │
└────────────────────────────────────────────────────────────────────────┘
```

                 ___________           __               _
                 \_   _____/ ____     |__| ____ ___ __ | |
                  |    __)_ /    \    |  |/  _ <   |  || |
                  |        \   |  \   |  (  <_> )___  | \|
                 /_______  /___|  /\__|  |\____// ____| __
                         \/     \/\______|      \/      \/
