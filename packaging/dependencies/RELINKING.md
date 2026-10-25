# Library and font source / replacement instructions

The release's `dependencies-source.zip` contains the source, build scripts and
licences for bundled OpenRA wrappers, native libraries, LGPL audio libraries and
the exact GNU FreeFont 20090104 fonts. Source URLs, revisions and download SHA-256
hashes are pinned in SOURCE_MANIFEST.json. Unrelated test/sample trees and compiled
outputs are omitted; library source/build scripts and licence files are retained.
Fetch the pinned original archive if you want the upstream test suites and fixtures.

The separate project source archive contains Sevenfall, the base OpenRA and SDK
trees, and the reviewed engine overlay. Build instructions are in BUILDING.md.
Sevenfall's original squad inference implementation is included in that source.

## Native libraries

- Eluant's wrapper source includes `.github/workflows/build-natives.yml` and the
  Lua platform patches. Build against the included Lua 5.1.5 source.
- FreeType's wrapper workflow and `win64.patch` describe the Windows build of
  FreeType 2.13.0. The FTL licence and copyright notices are included.
- OpenAL-CS uses OpenAL Soft 1.23.1. Its workflow records the CMake configuration;
  rebuild the included source and replace `soft_oal.dll` in the game directory.
- SDL2-CS includes its managed build and native packaging workflow. SDL 2.32.0
  source and ANGLE at the version reported by the bundled renderer are supplied.
  ANGLE has additional third-party notices retained under its source component.

## Managed LGPL libraries

- MP3Sharp 1.0.5: build `MP3Sharp/MP3Sharp.csproj` from its source component using
  a compatible .NET SDK. Replace `MP3Sharp.dll` in the game directory.
- TagLibSharp 2.3.0: follow the included project README and build its library
  project. Replace `TagLibSharp.dll` in the game directory.

These libraries are dynamically loaded. The package applies no signature check,
encryption or licence restriction preventing replacement with compatible modified
versions. Copy the portable distribution to a writable folder before rebuilding
or replacing files, and retain its other runtime files. The GPL engine and its
corresponding source permit rebuilding the application if an interface changes.

## Fonts

`mods/common/FreeSans.ttf` and `FreeSansBold.ttf` match the GNU FreeFont 20090104
TrueType distribution byte for byte. Its corresponding SFD font source, AUTHORS,
README and GPL COPYING are included in `gnu-freefont-20090104`.

Microsoft .NET 10 runtime and managed package notices are copied from the exact
restored packages into `Notices`. Their source repository/commit is recorded in
the corresponding NuGet metadata; permissive runtime sources are also available
from https://github.com/dotnet/runtime. The runtime is self-contained and may be
replaced/rebuilt subject to compatibility and the included licence terms.
