#Fixity File Verification Logic
###Receives Single File information to be verified 

1. Check if given file exists at given path 
 1. Check if any file exists for given inode in last scanned file's list
 2. If file exists and inode exists in last scan ( means file is still present and was also have be scanned by Fixity in it's last scan)
 
    1. if  File Exists::YES  AND Hashes are Same of File in last scan and given file::YES  AND Have Same File Path of File in last scan and given file::YES AND Have Same I-Node of File in last scan and given file::YES
	   *  Result :: "Confirmed" File (FileExists::YES  || SameHashOfFile::YES  || SameFilePath::YES || Same I-Node::YES)
    2. if  File Exists::YES  AND Hashes are Same of File in last scan and given file::YES  AND Have Same File Path of File in last scan and given file::NO AND Have Same I-Node of File in last scan and given file::YES
	   *  Result :: Moved or Renamed File (FileExists::YES  ||SameHashOfFile::YES  || SameFilePath::NO || Same I-Node::YES)
    3. if  File Exists::YES  AND Hashes are Same of File in last scan and given file::NO  AND Have Same File Path of File in last scan and given file::YES AND Have Same I-Node of File in last scan and given file::YES
	   *  Result :: Changed File (FileExists::YES  || SameHashOfFile::NO  || SameFilePath::YES || Same I-Node::YES)
    4. if  File Exists::YES  AND Hashes are Same of File in last scan and given file::NO  AND Have Same File Path of File in last scan and given file::NO AND Have Same I-Node of File in last scan and given file::YES
	   *  Result :: Changed File (FileExists::YES  || SameHashOfFile::NO  || SameFilePath::NO || Same I-Node::YES)
   
 3. If file exists and file with same hash exists but inode dose not exists in last scan ( means file is still present and file with same hash exists but was not existing in directory , or was not scanned for some reason (could be because of filters))  
 
    1. if  File Exists::YES  AND Hashes are Same of File in last scan and given file::YES  AND Have Same File Path of File in last scan and given file::YES AND Have Same I-Node of File in last scan and given file::NO
	   * Result :: Confirmed File (FileExists::YES  || SameHashOfFile::YES  || SameFilePath::YES || Same I-Node::NO) 
				
    2. if  File Exists::YES  AND Hashes are Same of File in last scan and given file::NO  AND Have Same File Path of File in last scan and given file::YES AND Have Same I-Node of File in last scan and given file::NO  '''
	   * Result :: Moved or Renamed File (FileExists::YES  || SameHashOfFile::NO  || SameFilePath::YES || Same I-Node::NO) 
				
    3. if  File Exists::YES  AND Hashes are Same of File in last scan and given file::YES  AND Have Same File Path of File in last scan and given file::NO AND Have Same I-Node of File in last scan and given file::NO  '''
	   * Result :: Changed File (FileExists::YES  || SameHashOfFile::YES  || SameFilePath::NO || Same I-Node::NO) 
				
 4. If file exists but file with same hash dont exist and inode dose not exists in last scan ( means file is still present and file with same hash exists but was not existing in directory , or was not scanned for some reason (could be because of filters))   
	* Result :: New File (FileExists::YES   || SameHashOfFile::NO    || SameFilePath::NO     || Same I-Node::NO)
			
2) Check if given file do not exist at given path and didnot fall in any of above condition will be considerd as Removed
 * Result :: Removed File
