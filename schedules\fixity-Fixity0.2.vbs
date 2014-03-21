Dim location, p
location = WScript.ScriptFullName
p = Replace(location, "fixity-Fixity0.2.vbs", "fixity-Fixity0.2.bat")
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run("""" & p & """")
Set WinScriptHost = Nothing