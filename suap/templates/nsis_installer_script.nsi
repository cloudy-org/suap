!include "MUI2.nsh"

Name "{suap-display-name}"
BrandingText "{suap-display-name}"
OutFile "{suap-binary-dist-path}"
InstallDir "$PROGRAMFILES64\Cloudy\{suap-project-name}"

VIProductVersion "{suap-project-version}"
VIAddVersionKey "ProductName" "{suap-display-name}"
VIAddVersionKey "FileDescription" "{suap-project-description}"
VIAddVersionKey "FileVersion" "{suap-project-version}"
VIAddVersionKey "CompanyName" "Cloudy Org"
VIAddVersionKey "LegalCopyright" "© 2026 Goldy"

SetCompressor /SOLID Lzma

# Admin is required for some registries to apply, like "HKEY_LOCAL_MACHINE\Software\Cloudy".
RequestExecutionLevel admin

# Defining some MUI specific features, like icons for the installer executables
!define MUI_ICON "{suap-icon-path}"
!define MUI_UNICON "{suap-icon-path}"

!define MUI_ABORTWARNING # good UX
!define MUI_UNABORTWARNING

# The typical installer pages a windows user will expect before installing software.
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

# This is like the entry point of the 
# installer, it's where the installation 
# of the application and uninstaller happens.
Section "MainSection"
    SetRegView 64
    SetShellVarContext all

    # Where we place our application binary file and other files.
    SetOutPath "$INSTDIR"

    # Where we add files from our environment, such as the application binary to the windows install directory.
    File "{suap-binary-path}"
    File "{suap-icon-path}"

    # Placing shortcut in "C:\ProgramData\Microsoft\Windows\Start Menu\Programs"
    CreateDirectory "$SMPROGRAMS\Cloudy"
    CreateShortcut "$SMPROGRAMS\Cloudy\{suap-project-name}.lnk" "$INSTDIR\{suap-binary-name}.exe" "" "$INSTDIR\{suap-icon-file-name}" 0

    WriteUninstaller "$INSTDIR\uninstall.exe"

    # Windows needs to know our application can be uninstalled via it's uninstall apps settings.
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}" "Publisher" "Cloudy Org"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}" "DisplayName" "{suap-display-name}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}" "DisplayVersion" "{suap-project-version}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}" "UninstallString" "$INSTDIR\uninstall.exe"

    # Allows the application to be called from the Windows Run Dialog or Command Prompt (CMD).
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\App Paths\{suap-binary-name}.exe" "" "$INSTDIR\{suap-binary-name}.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\App Paths\{suap-binary-name}.exe" "Path" "$INSTDIR"

    # Add application to "Open With" dialog if the application has mime types it supports
    {suap-app-capabilities-macro}

    System::Call "shell32.dll::SHChangeNotify(i 0x08000000, i 0, i 0, i 0)"
SectionEnd

Section "Uninstall"
    SetRegView 64
    SetShellVarContext all

    # Where we remove our application binary file and other files.
    Delete "$INSTDIR\{suap-binary-name}.exe"
    Delete "$INSTDIR\{suap-icon-file-name}"
    Delete "$INSTDIR\uninstall.exe"
    RMDir "$INSTDIR"

    Delete "$SMPROGRAMS\Cloudy\{suap-project-name}.lnk"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\App Paths\{suap-binary-name}.exe"

    {suap-app-capabilities-uni-macro}

    System::Call "shell32.dll::SHChangeNotify(i 0x08000000, i 0, i 0, i 0)"
SectionEnd