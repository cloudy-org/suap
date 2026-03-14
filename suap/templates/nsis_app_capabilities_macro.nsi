# https://learn.microsoft.com/en-us/windows/win32/shell/app-registration
WriteRegStr HKCR "Applications\{suap-binary-name}.exe" "DefaultIcon" "$INSTDIR\{suap-icon-file-name},0"
WriteRegStr HKCR "Applications\{suap-binary-name}.exe\shell\open" "FriendlyAppName" "{suap-display-name}"
WriteRegStr HKCR "Applications\{suap-binary-name}.exe\shell\open\command" "" '"$INSTDIR\{suap-binary-name}.exe" "%1"'

WriteRegStr HKCR "Cloudy.{suap-project-name}.1" "" "{suap-display-name} File Associations"
WriteRegStr HKCR "Cloudy.{suap-project-name}.1\DefaultIcon" "" "$INSTDIR\{suap-icon-file-name},0"
WriteRegStr HKCR "Cloudy.{suap-project-name}.1\shell\open\command" "" '"$INSTDIR\{suap-binary-name}.exe" "%1"'

# Adds supported and associate files for "OpenWithProgIds" 
# and also adds "Capabilities\FileAssociations" for application
{suap-file-associations-and-types-macro}

# Adds application to registered applications so it can show in Windows default apps list:
# https://learn.microsoft.com/en-us/windows/apps/develop/launch/launch-default-apps-settings
WriteRegStr HKLM "SOFTWARE\Cloudy\{suap-project-name}\Capabilities" "ApplicationName" "{suap-display-name}"
WriteRegStr HKLM "SOFTWARE\Cloudy\{suap-project-name}\Capabilities" "ApplicationDescription" "{suap-project-description}"

# This is where it actually registers by pointing to the "Capabilities" reg
WriteRegStr HKLM "SOFTWARE\RegisteredApplications" "{suap-project-name}" "SOFTWARE\Cloudy\{suap-project-name}\Capabilities"