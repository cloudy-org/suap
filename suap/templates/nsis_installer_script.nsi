!include "MUI2.nsh"

Name "{suap-display-name}"
BrandingText "{suap-display-name}"
OutFile "{suap-binary-dist-path}"
InstallDir "$PROGRAMFILES64\Cloudy\{suap-project-name}"

VIProductVersion "{suap-project-version}"
VIAddVersionKey "ProductName" "{suap-display-name}"
VIAddVersionKey "FileDescription" "{suap-project-description}"
VIAddVersionKey "FileVersion" "{suap-project-version}"

SetCompressor /SOLID Lzma

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
    # Where we place our application binary file and other files.
    SetOutPath "$INSTDIR"

    # Where we add files from our environment, such as the application binary to the windows install directory.
    File "{suap-binary-path}"
    File "{suap-icon-path}"

    WriteUninstaller "$INSTDIR\uninstall.exe"

    # Windows needs to know our application can be uninstalled via it's uninstall apps settings.
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}" "DisplayName" "{suap-display-name}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}" "UninstallString" "$INSTDIR\uninstall.exe"

    CreateShortcut "$DESKTOP\{suap-project-name}.lnk" "$INSTDIR\{suap-binary-name}.exe" "" "$INSTDIR\{suap-icon-file-name}" 0
SectionEnd

Section "Uninstall"
    # Where we remove our application binary file and other files.
    Delete "$INSTDIR\{suap-binary-name}.exe"
    Delete "$INSTDIR\{suap-icon-file-name}"
    Delete "$INSTDIR\uninstall.exe"
    RMDir "$INSTDIR"

    Delete "$DESKTOP\{suap-project-name}.lnk"

    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\{suap-project-name}"
SectionEnd