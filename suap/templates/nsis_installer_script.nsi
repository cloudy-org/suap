!include "MUI2.nsh"

# TODO: All "suap-project-name" keys except "InstallDir" and 
# "CreateShortcut" need to be changed to "suap-display-name" 
# when that is available.

Name "{suap-project-name}"
OutFile "{suap-binary-dist-path}"
InstallDir "$PROGRAMFILES64\cloudy-org\{suap-project-name}"

VIProductVersion "{suap-project-version}"
VIAddVersionKey "ProductName" "{suap-project-name}"
VIAddVersionKey "FileDescription" "{suap-project-description}"
VIAddVersionKey "FileVersion" "{suap-project-version}"

SetCompressor /SOLID Lzma

# The typical installer pages a windows user will expect before installing software.
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_LANGUAGE "English"

# Where the installing happens.
Section "MainSection"
    SetOutPath "$INSTDIR"
    File "{suap-binary-path}"

    CreateShortcut "$DESKTOP\{suap-project-name}.lnk" "$INSTDIR\{suap-binary-name}.exe"
SectionEnd

# TODO: add uninstaller