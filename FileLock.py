import os
import time
import errno

class FileLockException(Exception):
    pass

class FileLock(object):
    """ A file locking mechanism that has context-manager support so
        you can use it in a with statement. This should be relatively cross
        compatible as it doesn't rely on msvcrt or fcntl for the locking.
    """

    def __init__(self, file_name, processID , timeout=10, delay=30):
        """ Prepare the file locker. Specify the file to lock and optionally
            the maximum timeout and the delay between each attempt to lock.
        """
        self.is_locked = False
        self.lockfile = os.path.join(os.getcwd(), "%s.lock" % file_name)
        self.file_name = file_name
        self.timeout = timeout
        self.delay = delay
        self.processID = processID
        


    def acquire(self):
        """ Acquire the lock, if possible. If the lock is in use, it check again
            every `wait` seconds. It does this until it either gets the lock or
            exceeds `timeout` number of seconds, in which case it throws
            an exception.
        """
        start_time = time.time()
        while True:
            try:
                self.fd = os.open(self.lockfile, os.O_CREAT|os.O_EXCL|os.O_RDWR)
                if self.processID:
                    os.write(self.fd, str(self.processID))
                else:
                    os.write(self.fd, str(''))
                
                break;
            except OSError as e:
                if e.errno != errno.EEXIST:
                    print('process slept for 20 sec')
                    time.sleep(self.delay)

                if (time.time() - start_time) >= self.timeout:
                    print('process slept for 20 sec')
                    time.sleep(self.delay)

        self.is_locked = True

    def release(self):
        """ Get rid of the lock by deleting the lockfile.
            When working in a `with` statement, this gets automatically
            called at the end.
        """
        if self.is_locked:
            try:
                os.close(self.fd)
            except:
                pass
            
            print(str(self.lockfile)+' process released')
            os.unlink(self.lockfile)
            self.is_locked = False
            
    #Check is process alive or dead
    def isProcessLockFileIsDead(self):
            if(os.path.isfile(self.lockfile)):
                lockFile = open(self.lockfile,'r+')
                oldProcessId = lockFile.readline()
                lockFile.close()
                
                # If process Exists then returns False else True
                if(oldProcessId !='' and oldProcessId != None ):
                    return self.check_pid(oldProcessId)
                else:
                    os.remove(self.lockfile)
                    return False
            else:
                return False
            
    # Check For the existence of a unix pid.     
    def check_pid(self,pid):
        try:
            print(pid)
            os.kill(int(pid), 0)
        except OSError:
            return True
        else:
            return False
        