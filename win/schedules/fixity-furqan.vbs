Dim location, p
location = WScript.ScriptFullName
p = Replace(location, "fixity-furqan.vbs", "fixity-furqan.bat")
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run("""" & p & """")
Set WinScriptHost = Nothing