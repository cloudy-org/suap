!include "MUI2.nsh"

Name "{suap-display-name}"
OutFile "{suap-binary-dist-path}"
InstallDir "$PROGRAMFILES64\cloudy-org\{suap-project-name}"

VIProductVersion "{suap-project-version}"
VIAddVersionKey "ProductName" "{suap-display-name}"
VIAddVersionKey "FileDescription" "{suap-project-description}"
VIAddVersionKey "FileVersion" "{suap-project-version}"

SetCompressor /SOLID Lzma

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
    # Where we place our application binary file and other files.
    SetOutPath "$INSTDIR"
    File "{suap-binary-path}"

    WriteUninstaller "$INSTDIR\uninstall.exe"

    # Windows needs to know our application can be uninstalled via it's uninstall apps settings.
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}" "DisplayName" "{suap-display-name}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}" "UninstallString" "$INSTDIR\uninstall.exe"

    CreateShortcut "$DESKTOP\{suap-project-name}.lnk" "$INSTDIR\{suap-binary-name}.exe"
SectionEnd

Section "Uninstall"
    # Where we remove our application binary file and other files.
    Delete "$INSTDIR\{suap-binary-name}.exe"
    Delete "$INSTDIR\uninstall.exe"
    RMDir "$INSTDIR"

    Delete "$DESKTOP\{suap-project-name}.lnk"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}"
SectionEnd