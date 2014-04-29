import FixityCore



'''
File ID for NTFS
Returns the complete file ID as a single long string
(volume number, high index, low index)
'''

def ntfsIDForMac(f):
    id=''
    try:
        target = FixityCore.os.open(f , FixityCore.os.O_RDWR|FixityCore.os.O_CREAT )
        # Now get  the touple
        info = FixityCore.os.fstat(target)
        id = str(info.st_ino)

        FixityCore.os.close(target)
        
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

        try:
            target.close()
        except:
            pass
        
        
        FixityCore.Debugging.tureDebugerOn()
        FixityCore.Debugging.logError('Error Reporting Line 89 - 95 While Creating INode for File :' + str(f)  +" File FixtyCore\n", moreInformation)

        pass
    return id