Dim location, p
location = WScript.ScriptFullName
p = Replace(location, "fixity-testing.vbs", "fixity-testing.bat")
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run("""" & p & """")
Set WinScriptHost = Nothing