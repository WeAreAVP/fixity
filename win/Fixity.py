# Fixity GUI
# Version 0.1, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0

from PySide.QtCore import *
from PySide.QtGui import *
from os import path, listdir, remove, walk
import re
import datetime
import shutil
import FixityCore
import FixitySchtask
from EmailPref import EmailPref
import sys
from os import getcwd


class ProjectWin(QMainWindow):
        def __init__(self,EmailPref):
                QMainWindow.__init__(self)
                EP = EmailPref()
                self.EP = EmailPref()
                #self.setWindowIcon(QIcon(path.join(sys._MEIPASS, 'images\\logo_sign_small.png')))
                self.setWindowIcon(QIcon(path.join(getcwd(), 'images\\logo_sign_small.png')))
                if not path.isfile(getcwd()+'\\bin\conf.txt'):
                    fileConf = open(getcwd()+'\\bin\conf.txt', 'w+')
                    fileConf.close()
                self.unsaved = False
                menubar = self.menuBar()
                self.f = menubar.addMenu('&File')
                newp = QAction('&New Project', self)
                save = QAction('&Save and Run', self)
                usch = QAction('&Save Email/Time', self)
                dlte = QAction('&Delete Project', self)
                configemail = QAction('&Configure Email', self)
                quit = QAction('&Quit Fixity', self)
                
                
                self.f.addAction(newp)
                self.f.addAction(save)
                self.f.addAction(usch)
                self.f.addAction(dlte)
                self.f.addAction(configemail)
                self.f.addAction(quit)
                 
                
                dlte.triggered.connect(self.deleteproject)
                newp.triggered.connect(self.new)
                configemail.triggered.connect(self.ConfigEmailView)
                save.triggered.connect(self.run)
                usch.triggered.connect(self.updateschedule)
                quit.triggered.connect(self.close)
                
                self.widget = QWidget(self)
                
                self.pgroup = QGroupBox("Projects")
                self.play = QVBoxLayout()
                self.projects = QListWidget(self)
                self.projects.setFixedSize(115,190)

                for p in listdir('projects\\'):
                        if not '.tmp.' in p:
                                QListWidgetItem(p.replace('.fxy', ''), self.projects)
                self.play.addWidget(self.projects)
                self.pgroup.setLayout(self.play)
                
                self.sch = QGroupBox("Scheduling")
                self.monthly = QRadioButton("Monthly")
                self.weekly = QRadioButton("Weekly")
                self.daily = QRadioButton("Daily")
                self.runOnlyOnACPower =QCheckBox("Run Even on Battery")
                self.StartWhenAvailable  =QCheckBox("Start When Available ")
                self.EmailOnlyWhenSomethingChanged  =QCheckBox("Email Only When Something Changed ")
                self.runOnlyOnACPower.setChecked(True)
                self.StartWhenAvailable.setChecked(True)
                self.EmailOnlyWhenSomethingChanged.setChecked(True)
                self.monthly.clicked.connect(self.monthclick)
                self.weekly.clicked.connect(self.weekclick)
                self.daily.clicked.connect(self.dayclick)
                
                #self.runOnlyOnACPower.clicked.connect(self.runOnlyOnACPowerclick)
                
                slay = QVBoxLayout()
                slay.addWidget(self.monthly)
                slay.addWidget(self.weekly)
                slay.addWidget(self.daily)
                slay.addWidget(self.runOnlyOnACPower)
                slay.addWidget(self.StartWhenAvailable)
                slay.addWidget(self.EmailOnlyWhenSomethingChanged)
                
                
                self.timer = QTimeEdit(QTime())
                self.timer.setDisplayFormat("HH:mm")
                slay.addWidget(self.timer)
                
                self.dow = QComboBox()
                self.dow.addItems(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                self.dow.activated.connect(self.changed)
                slay.addWidget(self.dow)
                self.dow.hide()
                
                self.dom = QSpinBox()
                self.dom.setMaximum(31)
                self.dom.setMinimum(1)
                self.dom.valueChanged.connect(self.changed)
                slay.addWidget(self.dom)
                self.dom.hide()
                
                self.spacer = QSpacerItem(125,30)
                slay.addItem(self.spacer)
                
                self.lastrun = QLabel("Last checked: ")
                slay.addWidget(self.lastrun)
                self.sch.setLayout(slay)
                self.sch.setFixedSize(220, 255)
                
                self.mlay = QVBoxLayout()
                self.mlay.setSpacing(0)
                self.mtx = []
                for n in xrange(0, 7):
                        self.mtx.append(QLineEdit())
                        self.mlay.addWidget(self.mtx[n])
                        self.mtx[n].textChanged.connect(self.changed)
                
                self.dlay = QVBoxLayout()
                self.dlay.setSpacing(0)
                self.dtx, self.but = [], []
                for n in xrange(0, 7):
                        hbox = QHBoxLayout()
                        hbox.setContentsMargins(0,0,0,0)
                        hbox.setSpacing(0)
                        self.dtx.append(QLineEdit())
                        self.but.append(QPushButton('...'))
                        self.but[n].setFixedSize(30, 20)
                        self.but[n].clicked.connect(self.pickdir)
                        self.dtx[n].textChanged.connect(self.changed)
                        hbox.addWidget(self.dtx[n])
                        hbox.addWidget(self.but[n])
                        self.dlay.addLayout(hbox)
                
                self.dirs = QGroupBox("Directories")
                self.mail = QGroupBox("Email Addresses")
                self.dirs.setLayout(self.dlay)
                self.mail.setLayout(self.mlay)
                
                self.main = QHBoxLayout()
                
                self.main.addWidget(self.pgroup)
                self.main.addWidget(self.sch)
                self.main.addWidget(self.dirs)
                self.main.addWidget(self.mail) 
                self.widget.setLayout(self.main)
                self.setCentralWidget(self.widget)
                self.projects.itemClicked.connect(self.update)
                
                try:
                        self.old = self.projects.itemAt(0,0)
                        self.update(self.old)
                        self.old.setSelected(True)
                except:
                        pass
                self.unsaved = False
                self.toggler((self.projects.count() == 0))
                self.show()


                            
        # Configure Email Address for the Tools
        def ConfigEmailView(self):
            self.EP.CloseClick()
            self.EP=None
            self.EP = EmailPref()
            self.EP.SetDesgin()
            self.EP.ShowDialog()
            
        def newWindow(self):
            self = ProjectWin()
            self.show()
            sys.exit(app.exec_())
        # updates fields when project is selected in list
        @Slot(str)
        def update(self, new):
                if self.unsaved:
                        sbox = QMessageBox()
                        sbox.setText("There are unsaved changes to this project.")
                        sbox.setInformativeText("These will be discarded when opening a new project.\nWould you like to stay on this project?")
                        sbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Discard)
                        sbox.setDefaultButton(QMessageBox.Ok)
                        sval = sbox.exec_()
                        if sval == QMessageBox.Ok:
                                self.projects.setCurrentRow(self.projects.indexFromItem(self.old).row())
                                return
                if not path.isfile('projects\\' + self.old.text() + '.fxy'):
                        self.projects.takeItem(self.projects.row(self.old))
                try:
                        f = open('projects\\' + new.text() + '.fxy', 'rb')
                except:
                        for n in xrange(0,7):
                                self.dtx[n].setText("")
                                self.mtx[n].setText("")
                        self.timer.setTime(QTime(0,0))
                        self.monthclick()
                        self.monthly.setChecked(True)
                        self.dom.setValue(1)
                        return
                dlabel = f.readline()
                elabel = f.readline()
                slabel = f.readline()
                rlabel = f.readline()
                f.close()
                ds = dlabel.split(';')
                ms = elabel.split(';')
                n, p = 0, 0
                for n in xrange(0,7):
                        try:
                                self.dtx[n].setText(ds[n].strip())
                        except:
                                self.dtx[n].setText("")
                        try:
                                self.mtx[n].setText(ms[n].strip())
                        except:
                                self.mtx[n].setText("")
                sc = slabel.rstrip().split(' ')
                if sc[0] == '1':
                        self.monthly.setChecked(True)
                        self.monthclick()
                        self.dom.setValue(int(sc[2]))
                elif sc[0] == '2':
                        self.weekly.setChecked(True)
                        self.weekclick()
                        self.dow.setCurrentIndex(int(sc[3]))
                elif sc[0] == '3':
                        self.daily.setChecked(True)
                        self.dayclick()
                try:
                        t = sc[1].split(':')
                except:
                        t = ['00','00']
                self.timer.setTime(QTime(int(t[0]),int(t[1])))
                self.lastrun.setText("Last checked:\n" + rlabel)
                self.unsaved = False
                self.old = new
                
        # new project creation
        def new(self):
                name = QInputDialog.getText(self, "Project Name", "Name for new Fixity project:", text="New_Project")
                if name[0] == "" or path.isfile("projects\\" + name[0] + ".fxy") or any(c in '\ <>:\"\/\\\|?*' for c in name[0]) or name[0][-1] == '.':
                        QMessageBox.warning(self, "Fixity", "Invalid project name:\n*Project names must be unique\n*Project names cannot be blank\n*Project names cannot contain spaces\n*Project names must be legal filenames")
                        return
                newitem = QListWidgetItem(name[0], self.projects)
                self.projects.setCurrentItem(newitem)
                self.monthly.setChecked(True)
                self.monthclick()
                self.dom.setValue(1)
                self.timer.setTime(QTime(0,0))
                for x in xrange(0, 4):
                        self.dtx[x].setText("")
                        self.mtx[x].setText("")
                self.old = newitem
                self.toggler(False)

        # creates and saves projects
        def process(self):
                if all(d.text() == "" for d in self.dtx):
                        QMessageBox.warning(self, "Fixity", "No directories selected!\nPlease set directories to scan")
                        return
                dmonth, dweek = 99, 99
                if self.monthly.isChecked():
                        interval = 1
                        dmonth = int(self.dom.value())
                elif self.weekly.isChecked():
                        interval = 2
                        dweek = int(self.dow.currentIndex())
                elif self.daily.isChecked():
                        interval = 3
                else:
                        QMessageBox.warning(self, "Fixity", "Project schedule not set - please select an interval for scans")
                        return
                projfile = open('projects\\' + self.projects.currentItem().text() + '.fxy', 'wb')
                total = 0
                for ds in self.dtx:
                        if ds.text().strip() != "":
                                projfile.write(ds.text() + ";")
                projfile.write("\n")
                for ms in self.mtx:
                        if ms.text().strip() != "":
                                projfile.write(ms.text() + ";")
                projfile.write("\n")
                projfile.write(str(interval) + " " + self.timer.time().toString() + " " + str(dmonth) + " " + str(dweek) + "\n")
                projfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
            
                
                FixitySchtask.schedule(interval, dweek, dmonth, self.timer.time().toString(), self.projects.currentItem().text(),self.runOnlyOnACPower.isChecked() , self.StartWhenAvailable.isChecked(),self.EmailOnlyWhenSomethingChanged.isChecked())
                
                for dx in self.dtx:
                        src = dx.text()
                        l = self.buildTable(src, 'sha256')
                        for n in xrange(len(l)):
                                projfile.write(l[n][0] + "\t" + l[n][1] + "\t" + l[n][2] + "\n")
                                total += 1
                projfile.close()
                QMessageBox.information(self, "Fixity", str(total) + " files processed in project: " + self.projects.currentItem().text())
                self.unsaved = False
                
        # toggles fields on/off
        def toggler(self, switch):
                for n in xrange(len(self.mtx)):
                        self.mtx[n].setDisabled(switch)
                        self.dtx[n].setDisabled(switch)
                        self.but[n].setDisabled(switch)
                self.timer.setDisabled(switch)
                self.monthly.setDisabled(switch)
                self.weekly.setDisabled(switch)
                self.daily.setDisabled(switch)
                self.timer.setDisabled(switch)
                self.dom.setDisabled(switch)
                self.dow.setDisabled(switch)
        
        def changed(self):
                self.unsaved = True
        
        def dayclick(self):
                self.dom.hide()
                self.dow.hide()
                self.spacer.changeSize(30,25)
                
        def weekclick(self):
                self.spacer.changeSize(0,0)
                self.dom.hide()
                self.dow.show()
                
        def monthclick(self):
                self.spacer.changeSize(0,0)
                self.dow.hide()
                self.dom.show()

        def pickdir(self):
                n = self.but.index(self.sender())
                self.dtx[n].setText(QFileDialog.getExistingDirectory(dir=path.expanduser('~') + '\\Desktop\\'))
                
        # saves and runs 
        def run(self):
                try:
                        if path.getsize("projects\\" + self.projects.currentItem().text() + ".fxy") < 1024:
                                self.process()
                                self.unsaved = False
                                return
                except:
                        self.process()
                        self.unsaved = False
                        return
                self.updateschedule()
                results = FixityCore.run("projects\\" + self.projects.currentItem().text() + ".fxy")
                QMessageBox.information(self, "Fixity Results", self.projects.currentItem().text() + " scanned\n* " + str(results[0]) + " files passed\n* " + str(results[1]) + " files moved\n* " + str(results[2]) + " new files\n* " + str(results[4]) + " files missing\n* " + str(results[3]) + " files damaged")
                
        def deleteproject(self):
                sbox = QMessageBox()
                try:
                        sbox.setText("Are you certain that you want to delete " + self.projects.currentItem().text() + "?")
                except:
                        QMessageBox.information(self, "Fixity", "No project selected for deletion!")
                        return
                sbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                sbox.setDefaultButton(QMessageBox.Cancel)
                sval = sbox.exec_()
                if sval == QMessageBox.Cancel:
                                return
                try:
                        remove("projects\\" + self.projects.currentItem().text() + ".fxy")
                        remove("schedules\\fixity-" + self.projects.currentItem().text().replace(' ','_') + ".bat")
                        remove("schedules\\fixity-" + self.projects.currentItem().text().replace(' ','_') + ".vbs")
                except:
                        pass
                FixitySchtask.deltask(self.projects.currentItem().text())
                self.projects.takeItem(self.projects.row(self.projects.currentItem()))
                self.unsaved = False
                try:
                        self.update(self.projects.selectedItems()[0])
                except:
                        for x in xrange(0,7):
                                self.dtx[x].setText("")
                                self.mtx[x].setText("")
                        self.monthly.setChecked(True)
                        self.monthclick()
                        self.timer.setTime(QTime(0,0))
                        self.lastrun.setText("Last checked:")
                self.toggler((self.projects.count() == 0))
                self.unsaved = False
        def buildTable(self, r, a):
                list = []
                fls = []
                cur = QLabel("")
                progress = QProgressDialog()
                progress.setMaximum(100)
                progress.setMinimumDuration(0)
                for root, subFolders, files in walk(r):
                        for file in files:
                                fls.append(path.join(root, file))
                for f in xrange(len(fls)):
                        txt = path.abspath(fls[f])
                        if len(txt) > 43:
                                txt = txt[:20] + '...' + txt[-20:]
                        progress.setLabelText(txt.ljust(43))
                        p = path.abspath(fls[f])
                        h = FixityCore.fixity(p, a)
                        i = FixityCore.ntfsID(p)
                        list.append((h, p, i))
                        progress.setValue(100 * float(f) / len(fls))
                        qApp.processEvents()
                progress.close()
                return list
                
        def updateschedule(self):
                dmonth, dweek = 99, 99
                if self.monthly.isChecked():
                        interval = 1
                        dmonth = int(self.dom.value())
                elif self.weekly.isChecked():
                        interval = 2
                        dweek = int(self.dow.currentIndex())
                elif self.daily.isChecked():
                        interval = 3
                try:
                        new = open('projects\\' + self.projects.currentItem().text() + '.tmp.fxy', 'wb')
                        old = open('projects\\' + self.projects.currentItem().text() + '.fxy', 'rb')
                except:
                        QMessageBox.information(self, "Fixity", "No project selected to reschedule!")
                        return
                        
                new.write(old.readline())
                
                for ms in self.mtx:
                        if ms.text().strip() != "":
                                new.write(ms.text() + ";")
                new.write("\n")
                old.readline()
                old.readline()
                new.write(str(interval) + " " + self.timer.time().toString() + " " + str(dmonth) + " " + str(dweek) + "\n")
                while True:
                        x = old.readline()
                        if not x:
                                break
                        new.write(x)
                new.close()
                old.close()
                shutil.copy('projects\\' + self.projects.currentItem().text() + '.tmp.fxy', 'projects\\' + self.projects.currentItem().text() + '.fxy')
                remove('projects\\' + self.projects.currentItem().text() + '.tmp.fxy')
                
                FixitySchtask.schedule(interval, dweek, dmonth, self.timer.time().toString(), self.projects.currentItem().text() , self.runOnlyOnACPower.isChecked(), self.StartWhenAvailable.isChecked(),self.EmailOnlyWhenSomethingChanged.isChecked())
                self.unsaved = False
                
        def closeEvent(self, event):
                if self.unsaved:
                        sbox = QMessageBox()
                        sbox.setText("There are unsaved changes to this project.")
                        sbox.setInformativeText("These will be discarded when opening a new project.\nWould you like to stay on this project?")
                        sbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Discard)
                        sbox.setDefaultButton(QMessageBox.Ok)
                        sval = sbox.exec_()
                        if sval == QMessageBox.Ok:
                                event.ignore()
                        else:
                                event.accept()
        
if __name__ == '__main__':
        app = QApplication(sys.argv)
        w = ProjectWin(EmailPref)
        w.show()
        sys.exit(app.exec_())