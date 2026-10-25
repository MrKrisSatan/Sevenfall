# Sevenfall distribution notices

Sevenfall uses OpenRA release-20250330, commit
`b4f3d8ae02b6bd6f4a3a5441e6d0daf7c5073787`, and the Mod SDK at
`0059e22e0e3bfc862500aaaa9fe1aed4ea4e994a`.

OpenRA engine code and adapted rules, layouts, scripts and text definitions are
copyright the OpenRA Developers and Contributors, GPL-3.0-or-later. The packaged
COPYING and AUTHORS retain the upstream licence and contributor/dependency notices.
Adapted mod definitions reside in `mods/sevenfall/upstream`; this directory holds
text source only. It does not contain Red Alert game archives or audiovisual assets.

Sevenfall C# extensions and code-native vector graphics carry GPL-3.0-or-later
headers. Generated Sevenfall artwork has source images, packing scripts and
provenance manifests in the source repository. No exclusivity or trademark rights
in AI-generated images are asserted. No EA/Westwood game sprites, palettes,
cinematics, music, speech or game archives are part of the standalone package.

The common OpenRA module includes GNU FreeFont; upstream AUTHORS identifies it
as GPL. Exact font notices/source must be verified before publication.
The packaging script collects available NuGet licence texts and metadata in
`Notices`, including Microsoft .NET runtime licences and notices. Entries without
licence texts remain review items, not implied clearance.
OpenRA's dependencies include SDL2, FreeType, OpenAL, Eluant/Lua, Mono.NAT,
SharpZipLib, Linguini, NVorbis, TagLib#, MP3Sharp and other packages identified in
the upstream AUTHORS and the published dependency metadata. Preserve their
included licences when redistributing the candidate.

Corresponding source: https://github.com/MrKrisSatan/Sevenfall (the release tag),
https://github.com/OpenRA/OpenRA (the pinned commit above), and
https://github.com/OpenRA/OpenRAModSDK (the pinned commit above). A release must
include a source bundle alongside binaries; a candidate without that bundle is
not approved for publication.
