import shlex, subprocess, os
# Constructor

if os.name == 'posix':
    OsType = 'linux'

elif os.name == 'nt':
    OsType = 'Windows'

elif os.name == 'os2':
    OsType = 'check'

command_html_report = 'coverage html --omit=../GUI/*,../UnitTest/*,../Config/Validation.py,../Core/CustomException.py,../Core/Debugger.py'
if OsType == 'Windows':
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    process_response = subprocess.call(command_html_report, startupinfo=startupinfo)
else:

    args = shlex.split(command_html_report)
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
