Dim location, p
location = WScript.ScriptFullName
p = Replace(location, "fixity-New_Project1.vbs", "fixity-New_Project1.bat")
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run("""" & p & """")
Set WinScriptHost = Nothing