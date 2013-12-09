Dim location, p
location = WScript.ScriptFullName
p = Replace(location, "fixity-hello.vbs", "fixity-hello.bat")
Set WinScriptHost = CreateObject("WScript.Shell")
WinScriptHost.Run("""" & p & """")
Set WinScriptHost = Nothing