import FixityCore



'''
File ID for NTFS
Returns the complete file ID as a single long string
(volume number, high index, low index)
'''
def ntfsIDForWindows(filePath):
    id = '';
    try:
        
        
        target = open(filePath.decode('utf-8'), 'rb')
    except Exception as e:
        moreInformation = {"moreInfo":'none'}
        try:
            if not e[0] == None:
                moreInformation['LogsMore'] =str(e[0])
        except:
            pass
        try:
            if not e[1] == None:
                moreInformation['LogsMore1'] =str(e[1])
        except:
            pass
        
        
        
        Debugging = FixityCore.Debuger()
        Debugging.tureDebugerOn()
        Debugging.logError('Error Reporting Line 106 - 108 While reading file to Creating INode for File :' + str(filePath)  +" File FixtyCore\n", moreInformation)
        pass
    
    try:
        id = str(FixityCore.win32file.GetFileInformationByHandle(FixityCore.win32file._get_osfhandle(target.fileno()))[4]) + \
            str(FixityCore.win32file.GetFileInformationByHandle(FixityCore.win32file._get_osfhandle(target.fileno()))[8]) + \
            str(FixityCore.win32file.GetFileInformationByHandle(FixityCore.win32file._get_osfhandle(target.fileno()))[9])
        return id
    except Exception as e:


            moreInformation = {"moreInfo":'none'}
            try:
                if not e[0] == None:
                    moreInformation['LogsMore'] =str(e[0])
            except:
                pass
            try:
                if not e[1] == None:
                    moreInformation['LogsMore1'] =str(e[1])
            except:
                pass
            
            Debugging = FixityCore.Debuger()
            Debugging.tureDebugerOn()
            Debugging.logError('Error Reporting Line 89 - 95 While Creating INode for File :' + str(filePath)  +" File FixtyCore\n", moreInformation)
            pass
    return id
