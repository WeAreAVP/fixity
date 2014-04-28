import FixityCore


'''
Checksum Generation Method.
Input: File Path, Algorithm.
Output: Hexadecimal Value Of Hashed File.

'''
def fixity(filePath, Algorithm , projectName= None):
    moreInformation= {}
    
    try:
        fixmd5 = FixityCore.hashlib.md5()
        fixsha256 = FixityCore.hashlib.sha256()
        
    except Exception as e:

        moreInformation = {"moreInfo":'null'}
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

        FixityCore.Debugging.tureDebugerOn()
        FixityCore.Debugging.logError('Error Reporting Line 36 - 40 While encrypting File into hashes using Algo:' + str(Algorithm)  +" File FixtyCore\n", moreInformation)

        pass
    try:
        if FixityCore.OS_Info == 'Windows':
            filePath = str(filePath).replace('\\\\','\\')
            filePath = str(filePath).replace('\\',str(FixityCore.os.sep)+str(FixityCore.os.sep))
       
        
        
        with open(filePath.decode('utf-8'), 'r') as target:
            for piece in iter(lambda: target.read(4096), b''):
                
                fixmd5.update(piece)
                fixsha256.update(piece)
                
            target.close()
            
            return {'md5':fixmd5.hexdigest() , 'sha256':fixsha256.hexdigest()}
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
        
        
        FixityCore.Debugging.tureDebugerOn()
        FixityCore.Debugging.logError('Error Reporting Line 59 - 63 While encrypting File into hashes using Algo:' + str(Algorithm)  +" File FixtyCore\n", moreInformation)
        pass
    




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
