# Unit Tests For Fixity
######There are about 26 unit test writen for fixity 

### All unit test contains 
######Algorithum changes unit test for conditions mentioned below

#####Confirm for Both Normal And Special Charachter

 1. Confirmed  FileExists::YES   ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::NO
 2. Confirmed   FileExists::YES  ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES

#####Changed for Both Normal And Special Charachter

 1. Changed   FileExists::YES    ||SameHashOfFile::NO     ||SameFilePath::YES    ||SameI-Node::YES
 2. Changed  FileExists::YES     ||SameHashOfFile::NO     ||SameFilePath::NO     ||SameI-Node::YES
 3. Changed  FileExists::YES     ||SameHashOfFile::NO     ||SameFilePath::YES    ||SameI-Node::NO

#####Moved for Both Normal And Special Charachter
 1. Moved   FileExists::YES      ||SameHashOfFile::YES    ||SameFilePath::NO     ||SameI-Node::YES

#####Removed for Both Normal And Special Charachter
 1. Deleted   FileExists::NO     ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES

#####New for Both Normal And Special Charachter
 1. New  FileExists::YES         ||SameHashOfFile::NO     ||SameFilePath::NO     ||SameI-Node::NO

#####Scenarios of Algorithm change 
 1. Move file with in a directory  
 2. Move file with in a directory and change content 
 3. Copy , Paste a File 
 4. Copy , Paste a File , Then Remove old File also change name of the new file as old one 
 5. Copy , Paste a File , Then Remove old File and change content of New file also change name of the new file as old one 
 6. Change Directories Path
 7. Intersection of folder at a new place
 
###Scenarios of Dir required
 1. Is Report Directory Exists
 2. Is Schedules Directory Exists
 3. Is Config File Exists
 4. Is Debug File Exists
 5. Is Database File Exists
 6. Is History Directory Exist 
 
###Project Operations

 1. Delete Run Unit test
 2. Project Run Unit test
 3. Change Project Name Unit test
 4. Save Project Unit test
 5. Change Algorithm Unit test
 6. Filter scanned files Unit test
 7. Import Project Unit test

###Email Unit Test 
 1. Testing Email
 2. Attchment Email
 3. Error Email

