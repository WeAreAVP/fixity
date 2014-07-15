import subprocess

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

command_html_report = 'coverage html --omit=../GUI/*,../UnitTest/*,../Config/Validation.py,../Core/CustomException.py,../Core/Debugger.py'
process_response = subprocess.call(command_html_report, startupinfo=startupinfo)
