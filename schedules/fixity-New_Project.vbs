Dim location, p
location = WScript.ScriptFullName
p = Replace(location, "fixity-New_Project.vbs", "fixity-New_Project.bat")
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run("""" & p & """")
Set WinScriptHost = Nothing