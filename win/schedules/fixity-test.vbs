Dim location, p
location = WScript.ScriptFullName
p = Replace(location, "fixity-test.vbs", "fixity-test.bat")
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run("""" & p & """")
Set WinScriptHost = Nothing