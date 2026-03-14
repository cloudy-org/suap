DeleteRegKey HKCR "Applications\{suap-binary-name}.exe"

DeleteRegKey HKCR "Cloudy.{suap-project-name}.1"

# Removes application from "OpenWithProgIds" in supported and associate files
{suap-file-associations-and-types-macro}

# Deletes "Capabilities" as well as "Capabilities\FileAssociations" reg
DeleteRegKey HKLM "SOFTWARE\Cloudy\{suap-project-name}"

# Removes application from registered applications (e.g: default apps list)
DeleteRegValue HKLM "SOFTWARE\RegisteredApplications" "{suap-project-name}"