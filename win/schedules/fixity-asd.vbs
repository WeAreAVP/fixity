Dim location, p
location = WScript.ScriptFullName
p = Replace(location, "fixity-asd.vbs", "fixity-asd.bat")
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run("""" & p & """")
Set WinScriptHost = Nothing