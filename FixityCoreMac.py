import FixityCore



'''
File ID for NTFS
Returns the complete file ID as a single long string
(volume number, high index, low index)
'''

def ntfsIDForMac(f):
    idNode = ''
    try:
        target = FixityCore.os.open(f , FixityCore.os.O_RDWR|FixityCore.os.O_CREAT )
        # Now get  the touple
        info = FixityCore.os.fstat(target)
        idNode = str(info.st_ino)

        FixityCore.os.close(target)
        
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

        try:
            target.close()
        except:
            pass
        
        
        FixityCore.Debugging.tureDebugerOn()
        FixityCore.Debugging.logError('Error Reporting Line 89 - 95 While Creating INode for File :' + str(f)  +" File FixtyCore\n", moreInformation)

        pass
    return idNode