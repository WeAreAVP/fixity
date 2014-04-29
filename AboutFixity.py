# ===============================================================================
#  -- coding: utf-8 --
#  Details about fixity
#  Version 0.4, Apr 1, 2014
#  Copyright (c) 2013 AudioVisual Preservation Solutions
#  All rights reserved.
#  Released under the Apache license, v. 2.0
# ===============================================================================

'''
Created on Dec 5, 2013
@author: Furqan Wasi <furqan@avpreserve.com>
'''
import os
OS_Info = ''
if os.name == 'posix':
    OS_Info = 'linux'
elif os.name == 'nt':
    OS_Info = 'Windows'
elif os.name == 'os2':
    OS_Info = 'check'

from PySide.QtCore import *
from PySide.QtGui import *
from os import getcwd , path, listdir, remove, walk
import sys
import time
import re
import hashlib


class AboutFixity(QDialog):
    
    
    ''' Class to manage the Filter to be implemented for the files with specific extensions '''
    
    '''Contstructor'''
    def __init__(self):
        QDialog.__init__(self)
        
        self.setWindowTitle('About Fixity')
        self.setWindowIcon(QIcon(path.join(getcwd(), 'images' + str(os.sep) + 'logo_sign_small.png')))
        self.AboutFixityLayout = QVBoxLayout()

        self.widget = QWidget(self)
        self.pgroup = QGroupBox()
        self.play = QVBoxLayout()

        self.DescriptionBtn = QPushButton('Description')
        self.AuthorandLicenseBtn = QPushButton('Author and License')
        self.ContactBtn = QPushButton('Contact')
        self.CloseBtn = QPushButton('Close')
        
        self.sch = QGroupBox()
        self.monthly = QTextEdit()
        self.weekly = QTextEdit()
        self.main = QHBoxLayout()

    ''' Distructor'''
    def destroyAboutFixity(self):
        del self
        
        
    ''' Create Window'''
    def CreateWindow(self):
        self = QDialog()
        
        
    ''' Get Window'''
    def GetWindow(self):
        return self
    
    
    ''' Show Dialog'''
    def ShowDialog(self):
        self.show()
        self.exec_()


    ''' Set Layout'''
    def SetLayout(self, layout):
        self.AboutFixityLayout = layout


    ''' Get Layout'''
    def GetLayout(self):
        return self.AboutFixityLayout
    
    
    ''' Show Description'''
    def showDescription(self):
        
        self.monthly.setText('<h1>DESCRIPTION</h1>')
        decriptionText = '<p>AVPreserve Fixity 0.4</p>'
        decriptionText += '<p>Fixity was developed by AVPreserve and can be found at www.avpreserve.com/tools</p></br>'
        decriptionText += '<p>The GitHub repository for Fixity can be found at https://github.com/avpreserve/fixity</p>'
        decriptionText += '<p>Fixity is a utility for the documentation and regular review of stored files. Fixity scans a folder or directory, creating a manifest of the files including their file paths and their checksums, against which a regular comparative analysis can be run. Fixity monitors file integrity through generation and validation of checksums, and file attendance through monitoring and reporting on new, missing, moved and renamed files. Fixity emails a report to the user documenting flagged items along with the reason for a flag, such as that a file has been moved to a new location in the directory, has been edited, or has failed a checksum comparison for other reasons. Supplementing tools like BagIt that review files at points of exchange, when run regularly Fixity becomes a powerful tool for monitoring digital files in repositories, servers, and other long-term storage locations.</p>'
        
        self.weekly.setText(decriptionText)
        self.DescriptionBtn.setDisabled(True)
        self.AuthorandLicenseBtn.setDisabled(False)
        self.ContactBtn.setDisabled(False)


    ''' Show License Information On About Us Page(Trigger in  button press)'''
    def showLicense(self):
        
        '''header'''
        self.monthly.setText('<h1>Author and License </h1>')
        
        
        '''header Detail'''
        LicenseText = '<p>Fixity Copyright and License</p>'
        LicenseText += '<p>Copyright (C) 2013-2014 www.avpreserve.com, info@avpreserve.com</p></br>'
        LicenseText += '<p>Fixity is licensed under an Apache License, Version 2.0</p>'
        LicenseText += '<p>Fixity is a utility for the documentation and regular review of stored files. Fixity scans a folder or directory, creating a manifest of the files including their file paths and their checksums, against which a regular comparative analysis can be run. Fixity monitors file integrity through generation and validation of checksums, and file attendance through monitoring and reporting on new, missing, moved and renamed files. Fixity emails a report to the user documenting flagged items along with the reason for a flag, such as that a file has been moved to a new location in the directory, has been edited, or has failed a checksum comparison for other reasons. Supplementing tools like BagIt that review files at points of exchange, when run regularly Fixity becomes a powerful tool for monitoring digital files in repositories, servers, and other long-term storage locations.</p>'
        LicenseText += '<h1>Fixity License</h1></br>'
        LicenseText += '<center>Apache License</center></br>'
        LicenseText += '<center>Version 2.0, January 2004</center></br>'
        LicenseText += '<center>http://www.apache.org/licenses/</center></br>'
        LicenseText += '<p>TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION</p></br>'
        
        
        '''Definitions'''
        LicenseText += '<ol>'
        LicenseText += '    <li>'
        LicenseText += '        <p> "License" shall mean the terms and conditions for use, reproduction, and distribution as defined by Sections 1 through 9 of this document.</p>'
        LicenseText += '        <p> "Licensor" shall mean the copyright owner or entity authorized by the copyright owner that is granting the License.</p>'
        LicenseText += '        <p> "Legal Entity" shall mean the union of the acting entity and all other entities that control, are controlled by, or are under common control with that entity. For the purposes of this definition, "control" means (i) the power, direct or indirect, to cause the direction or management of such entity, whether by contract or otherwise, or (ii) ownership of fifty percent (50%) or more of the outstanding shares, or (iii) beneficial ownership of such entity.</p>'
        LicenseText += '        <p> "You" (or "Your") shall mean an individual or Legal Entity exercising permissions granted by this License.</p>'
        LicenseText += '        <p> "Source" form shall mean the preferred form for making modifications, including but not limited to software source code, documentation source, and configuration files.</p>'
        LicenseText += '        <p> "Object" form shall mean any form resulting from mechanical transformation or translation of a Source form, including but not limited to compiled object code, generated documentation, and conversions to other media types.</p>'
        LicenseText += '        <p> "Derivative Works" shall mean any work, whether in Source or Object form, that is based on (or derived from) the Work and for which the editorial revisions, annotations, elaborations, or other modifications represent, as a whole, an original work of authorship. For the purposes of this License, Derivative Works shall not include works that remain separable from, or merely link (or bind by name) to the interfaces of, the Work and Derivative Works thereof.</p>'
        LicenseText += '        <p> "Contribution" shall mean any work of authorship, including the original version of the Work and any modifications or additions to that Work or Derivative Works thereof, that is intentionally submitted to Licensor for inclusion in the Work by the copyright owner or by an individual or Legal Entity authorized to submit on behalf of the copyright owner. For the purposes of this definition, "submitted" means any form of electronic, verbal, or written communication sent to the Licensor or its representatives, including but not limited to communication on electronic mailing lists, source code control systems, and issue tracking systems that are managed by, or on behalf of, the Licensor for the purpose of discussing and improving the Work, but excluding communication that is conspicuously marked or otherwise designated in writing by the copyright owner as "Not a Contribution."</p>'
        LicenseText += '        <p> "Contributor" shall mean Licensor and any individual or Legal Entity on behalf of whom a Contribution has been received by Licensor and subsequently incorporated within the Work.</p>'
        LicenseText += '    </li>'
        
        '''1'''
        LicenseText += '    <li>'
        LicenseText += '        <p> Grant of Copyright License. Subject to the terms and conditions of this License, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable copyright license to reproduce, prepare Derivative Works of, publicly display, publicly perform, sublicense, and distribute the Work and such Derivative Works in Source or Object form.</p>'
        LicenseText += '    </li>'
        '''2'''
        LicenseText += '    <li>'
        LicenseText += '        <p> Grant of Patent License. Subject to the terms and conditions of this License, each Contributor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable (except as stated in this section) patent license to make, have made, use, offer to sell, sell, import, and otherwise transfer the Work, where such license applies only to those patent claims licensable by such Contributor that are necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with the Work to which such Contribution(s) was submitted. If You institute patent litigation against any entity (including a cross-claim or counterclaim in a lawsuit) alleging that the Work or a Contribution incorporated within the Work constitutes direct or contributory patent infringement, then any patent licenses granted to You under this License for that Work shall terminate as of the date such litigation is filed.</p>'
        LicenseText += '    </li>'
        
        '''3'''
        LicenseText += '    <li>'
        LicenseText += '        <p> Redistribution. You may reproduce and distribute copies of the Work or Derivative Works thereof in any medium, with or without modifications, and in Source or Object form, provided that You meet the following conditions:</p>'
        LicenseText += '        <ol type="a">'
        
        '''3-a'''
        LicenseText += '            <li>'
        LicenseText += '                <p> You must give any other recipients of the Work or Derivative Works a copy of this License; and</p>'
        LicenseText += '            </li>'
        
        '''3-b'''
        LicenseText += '            <li>'
        LicenseText += '                <p> You must cause any modified files to carry prominent notices stating that You changed the files; and</p>'
        LicenseText += '            </li>'
        
        '''3-c'''
        LicenseText += '            <li>'
        LicenseText += '                <p> You must retain, in the Source form of any Derivative Works that You distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work, excluding those notices that do not pertain to any part of the Derivative Works; and</p>'
        LicenseText += '            </li>'
        
        '''3-d'''
        LicenseText += '            <li>'
        LicenseText += '                <p> If the Work includes a "NOTICE" text file as part of its distribution, then any Derivative Works that You distribute must include a readable copy of the attribution notices contained within such NOTICE file, excluding those notices that do not pertain to any part of the Derivative Works, in at least one of the following places: within a NOTICE text file distributed as part of the Derivative Works; within the Source form or documentation, if provided along with the Derivative Works; or, within a display generated by the Derivative Works, if and wherever such third-party notices normally appear. The contents of the NOTICE file are for informational purposes only and do not modify the License. You may add Your own attribution notices within Derivative Works that You distribute, alongside or as an addendum to the NOTICE text from the Work, provided that such additional attribution notices cannot be construed as modifying the License.</p>'
        LicenseText += '            </li>'
        LicenseText += '        </ol>'
        
        LicenseText += '        <p> You may add Your own copyright statement to Your modifications and may provide additional or different license terms and conditions for use, reproduction, or distribution of Your modifications, or for any such Derivative Works as a whole, provided Your use, reproduction, and distribution of the Work otherwise complies with the conditions stated in this License. </p>'
        
        LicenseText += '    </li>'
        
        '''4'''
        LicenseText += '    <li>'
        LicenseText += '        <p> Submission of Contributions. Unless You explicitly state otherwise, any Contribution intentionally submitted for inclusion in the Work by You to the Licensor shall be under the terms and conditions of this License, without any additional terms or conditions. Notwithstanding the above, nothing herein shall supersede or modify the terms of any separate license agreement you may have executed with Licensor regarding such Contributions.</p>'
        LicenseText += '    </li>'
        
        '''5'''
        LicenseText += '    <li>'
        LicenseText += '        <p> Trademarks. This License does not grant permission to use the trade names, trademarks, service marks, or product names of the Licensor, except as required for reasonable and customary use in describing the origin of the Work and reproducing the content of the NOTICE file.</p>'
        LicenseText += '    </li>'
        '''6'''
        LicenseText += '    <li>'
        LicenseText += '        <p> Disclaimer of Warranty. Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.</p>'
        LicenseText += '    </li>'
        
        '''7'''
        LicenseText += '    <li>'
        LicenseText += '        <p> Limitation of Liability. In no event and under no legal theory, whether in tort (including negligence), contract, or otherwise, unless required by applicable law (such as deliberate and grossly negligent acts) or agreed to in writing, shall any Contributor be liable to You for damages, including any direct, indirect, special, incidental, or consequential damages of any character arising as a result of this License or out of the use or inability to use the Work (including but not limited to damages for loss of goodwill, work stoppage, computer failure or malfunction, or any and all other commercial damages or losses), even if such Contributor has been advised of the possibility of such damages.</p>'
        LicenseText += '    </li>'
        
        '''8'''
        LicenseText += '    <li>'
        LicenseText += '        <p> Accepting Warranty or Additional Liability. While redistributing the Work or Derivative Works thereof, You may choose to offer, and charge a fee for, acceptance of support, warranty, indemnity, or other liability obligations and/or rights consistent with this License. However, in accepting such obligations, You may act only on Your own behalf and on Your sole responsibility, not on behalf of any other Contributor, and only if You agree to indemnify, defend, and hold each Contributor harmless for any liability incurred by, or claims asserted against, such Contributor by reason of your accepting any such warranty or additional liability.</p>'
        LicenseText += '    </li>'
        LicenseText += '</ol>'
        
        LicenseText += '<p>END OF TERMS AND CONDITIONS</p></br>'
        
        '''PySide License'''
        LicenseText += '<h1>PySide License</h1></br>'
        LicenseText += '<p>Copyright (C) 2013 Digia Plc</p>'
        LicenseText += '<span>Contact: PySide team</span>'
        LicenseText += '<p>This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License version 2.1 as published by the Free Software Foundation. This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.</p>'
        LicenseText += '<p>You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA</p>'
        
        LicenseText += '<h1>SQLite License</h1></br>'
        LicenseText += '<p>All of the code and documentation in SQLite has been dedicated to the public domain by the authors. All code authors, and representatives of the companies they work for, have signed affidavits dedicating their contributions to the public domain and originals of those signed affidavits are stored in a firesafe at the main offices of Hwaci. Anyone is free to copy, modify, publish, use, compile, sell, or distribute the original SQLite code, either in source code form or as a compiled binary, for any purpose, commercial or non-commercial, and by any means.</p><br/>'
        
        self.weekly.setText(LicenseText)
        self.DescriptionBtn.setDisabled(False)
        self.AuthorandLicenseBtn.setDisabled(True)
        self.ContactBtn.setDisabled(False)
        
        
    '''Trigger The Show Contact'''
    def showContact(self):
        self.monthly.setText('<h1>Contact</h1>')

        ContactText = '<p>Please post issues and feature requests at https://github.com/avpreserve/fixity/issues</p>'
        ContactText += '<p>Please send questions, comments or feedback to info@avpreserve.com</p></br>'

        self.weekly.setText(ContactText)
        self.DescriptionBtn.setDisabled(False)
        self.AuthorandLicenseBtn.setDisabled(False)
        self.ContactBtn.setDisabled(True)


    ''' All design Management Done in Here'''
    def SetDesgin(self):
        try:
            self.DescriptionBtn.setFixedSize(210, 30)
            self.AuthorandLicenseBtn.setFixedSize(210, 30)
            self.ContactBtn.setFixedSize(210, 30)
        except:
            self.DescriptionBtn = QPushButton('Description')
            self.AuthorandLicenseBtn = QPushButton('Author and License')
            self.ContactBtn = QPushButton('Contact')
            self.CloseBtn = QPushButton('Close')
            
    

        pic = QLabel(self)
        pic.setGeometry(30, 30, 500, 600)
        pic.setFixedSize(400,400)
        '''use full ABSOLUTE path to the image, not relative'''
        pic.setPixmap(QPixmap(path.join(getcwd(), 'images'+str(os.sep)+'avpreserve.png')))

        self.DescriptionBtn.clicked.connect(self.showDescription)
        self.AuthorandLicenseBtn.clicked.connect(self.showLicense)
        self.ContactBtn.clicked.connect(self.showContact)
        self.CloseBtn.clicked.connect(self.Cancel)

        self.play.addWidget(self.DescriptionBtn)
        self.play.addWidget(self.AuthorandLicenseBtn)
        self.play.addWidget(self.ContactBtn)
        self.play.addWidget(pic)
        self.pgroup.setLayout(self.play)

        slay = QVBoxLayout()
        self.monthly.setFixedSize(570,40)
        self.weekly.setFixedSize(570,500)
        slay.addWidget(self.monthly)
        slay.addWidget(self.weekly)
        self.CloseBtn.setFixedSize(200,30)
        slay.addWidget(self.CloseBtn)

        self.sch.setFixedSize(600, 600)
        self.pgroup.setFixedSize(255, 600)
        self.main.addWidget(self.pgroup)
        self.main.addWidget(self.sch)

        self.sch.setLayout(slay)
        self.setLayout(self.main)
        self.showDescription()


    ''' 
    close the dailog box
    '''
    def Cancel(self):
        self.destroyAboutFixity()
        self.close()
