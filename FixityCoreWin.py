# -*- coding: utf-8 -*-
# Fixity Core module Helper for Windows
# Version 0.3, 2013-10-28
# Copyright (c) 2013 AudioVisual Preservation Solutions
# All rights reserved.
# Released under the Apache license, v. 2.0




import win32file
from Debuger import Debuger
Debugging = Debuger()
'''
File ID for NTFS
Returns the complete file ID as a single long string
(volume number, high index, low index)
'''
def ntfsIDForWindows(filePath):
    print('ntfsIDForWindows')
    idNode = '';
    try:
        
        
        target = open(filePath.decode('utf-8'), 'rb')
    except Exception as Excep:
        moreInformation = {"moreInfo":'none'}
        try:
            if not Excep[0] == None:
                moreInformation['LogsMore'] =str(Excep[0])
        except:
            pass
        try:
            if not Excep[1] == None:
                moreInformation['LogsMore1'] =str(Excep[1])
        except:
            pass
        
        
        
        
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 106 - 108 While reading file to Creating INode for File :' + str(filePath)  +" File FixtyCore\n", moreInformation)
        pass
    
    try:
        idNode = str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[4]) + \
            str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[8]) + \
            str(win32file.GetFileInformationByHandle(win32file._get_osfhandle(target.fileno()))[9])
        return idNode
    except Exception as Excep:


            moreInformation = {"moreInfo":'none'}
            try:
                if not Excep[0] == None:
                    moreInformation['LogsMore'] =str(Excep[0])
            except:
                pass
            try:
                if not Excep[1] == None:
                    moreInformation['LogsMore1'] =str(Excep[1])
            except:
                pass
          
            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting Line 89 - 95 While Creating INode for File :' + str(filePath)  +" File FixtyCore\n", moreInformation)
            pass
    return idNode
