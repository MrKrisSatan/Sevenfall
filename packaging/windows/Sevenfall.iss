; Sevenfall per-user Windows candidate installer. GPL-3.0-or-later.
#ifndef SourceDir
  #error SourceDir must identify a verified portable candidate
#endif
#ifndef Version
  #error Version must match the candidate BUILD_INFO.json
#endif
#ifndef OutputDir
  #define OutputDir "."
#endif
[Setup]
AppId={{7C40D9CB-B042-4B9D-9AEA-754C8CDD25A6}
AppName=Sevenfall Skirmish Alpha
AppVersion={#Version}
AppPublisher=Sevenfall contributors
AppPublisherURL=https://github.com/MrKrisSatan/Sevenfall
AppSupportURL=https://github.com/MrKrisSatan/Sevenfall/issues
DefaultDirName={localappdata}\Programs\Sevenfall Alpha
DefaultGroupName=Sevenfall Alpha
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
OutputDir={#OutputDir}
OutputBaseFilename=Sevenfall-{#Version}-Setup-windows-x64
Compression=lzma2/normal
SolidCompression=yes
WizardStyle=modern
LicenseFile={#SourceDir}\COPYING
UninstallDisplayIcon={app}\Sevenfall.exe
CloseApplications=yes
RestartApplications=no
[Tasks]
Name: desktopicon; Description: "Create a desktop shortcut"; Flags: unchecked
[Dirs]
Name: "{app}\Support"; Flags: uninsneveruninstall
[Files]
Source: "{#SourceDir}\*"; DestDir: "{app}"; Excludes: "Support\*"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "{#SourceDir}\Support\settings.yaml"; DestDir: "{app}\Support"; Flags: onlyifdoesntexist uninsneveruninstall
[Icons]
Name: "{group}\Sevenfall"; Filename: "{app}\Sevenfall.exe"; WorkingDir: "{app}"
Name: "{autodesktop}\Sevenfall"; Filename: "{app}\Sevenfall.exe"; WorkingDir: "{app}"; Tasks: desktopicon
[Run]
Filename: "{app}\Sevenfall.exe"; Description: "Launch Sevenfall"; Flags: nowait postinstall skipifsilent
