Created By Furqan Wasi furqan@avpreserve.com Create On 14/4/2014 Monday,April

#Directory Structure

./build (Stores file required to create stand alone application)

./dist (contains Stand Alone app after creating using py2app or pyinstaller)

./history (Contain Manifest files of the project as history)

./assets (images using in Fixity and templates for scheduler xml templates)

./reports (Contains generated Reports)

./schedules (contains files used in scheduling process)

#Code Structure

+---assets (Images and templates ) (Sub Directory ) +---template (templates of scheduler xml file creation)

+---Config (Files mentaion Fixity Setting up and Configuration )

+---Core   (Files Contains all business logic for Fixity )

+---GUI    (Files Contains all GUI for Fixity )

#Files information
./conf.xml (contain information is debugging on or off )
./Fixity.db (Database of Fixity contains all information except dubugging is on or off)
./debug.log (Exceptions and error Logging )



#MAC CONFIGURATION
1) Download and install latest Xcode compatible with your macOS version

2) Download and install QT 4.8 (witout debug-libraries) http://qt-project.org/downloads

3) Download and install PySide (http://qt-project.org/wiki/PySide_Binaries_MacOSX)

4) Download and install favorite IDE (PyCharm,Textmate,eclipse)

5) install from mac port or brew

install cmake install qmake

6) Install PySide using easyinstall:: sudo easy_install-2.7 PySide

7) Upgrade PySide sudo easy_install-2.7 -U PySide

#For App Creation
py2applet --make-setup MyApplication.py

rm -rf build dist

python setup.py py2app

new app will be create in "dist" folder

For More Information Visist:https://pythonhosted.org/py2app/tutorial.html

#scheduling Process
Fixity is using launchd for scheduling , it save's plist for scheduling at "cd ~/Library/LaunchAgents/" , in this .plist file stores all scheduling information , for each project one .plist will be created.

#Windows Configuration
1) Download and install Python2.7

2) Download and install pyside1.2

2) Download and install QT4.8

3) Download and install PyInstaller 2.1 for .exe file create as stand alone application

4) Download and install favorite IDE (PyCharm,Textmate,eclipse)

For eclipse from install new update , install pydev from python.org/updates and set interpreter as python from preferences

5) if having problem of missing library download and install them from python.org using python setup.py install (setup.py file will be provided in the given library package )

#App/Executable File Creation
python /path/to/pyinstaller/pyinstaller.py --onefile --noconsole --icon="assets\icon.ico" FileName.py

In Fixity two Files are created

python /path/to/pyinstaller/pyinstaller.py --onefile --noconsole --icon="assets\icon.ico" Fixity.py

python /path/to/pyinstaller/pyinstaller.py --onefile --noconsole --icon="assets\icon.ico" AutoFixity.py

These files are placed in "dist" directory after complilation of above commands

Note: to turn on the debugging for app using --console

when placing the file for the build

Fixity.exe will be placed at the same level of all other directories for example (bin,schedules,history,etc)

AutoFxity.py will be placed into schedules directory where from task scheduler will access it to run scanner

#Scheduling Process
For Scheduling process Fixity is using windows task scheduler , it triggers the scanning process on given time when saving the project , for each project one scheduler will be created in Task scheduler
