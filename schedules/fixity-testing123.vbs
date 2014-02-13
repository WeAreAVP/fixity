Dim location, p
location = WScript.ScriptFullName
p = Replace(location, "fixity-testing123.vbs", "fixity-testing123.bat")
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run("""" & p & """")
Set WinScriptHost = Nothing