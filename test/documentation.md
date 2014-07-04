# Unit Tests For Fixity
######There are about 26 unit test writen for fixity 

### All unit test contains 
######Algorithum changes unit test for conditions mentioned below

#####Confirm

 1. Confirmed  FileExists::YES   ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::NO
 2. Confirmed   FileExists::YES  ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES

#####Changed

 1. Changed   FileExists::YES    ||SameHashOfFile::NO     ||SameFilePath::YES    ||SameI-Node::YES
 2. Changed  FileExists::YES     ||SameHashOfFile::NO     ||SameFilePath::NO     ||SameI-Node::YES
 3. Changed  FileExists::YES     ||SameHashOfFile::NO     ||SameFilePath::YES    ||SameI-Node::NO

#####Moved
 1. Moved   FileExists::YES      ||SameHashOfFile::YES    ||SameFilePath::NO     ||SameI-Node::YES

#####Removed
 1. Deleted   FileExists::NO     ||SameHashOfFile::YES    ||SameFilePath::YES    ||SameI-Node::YES

#####New
 1. New  FileExists::YES         ||SameHashOfFile::NO     ||SameFilePath::NO     ||SameI-Node::NO

###Project Operations

 1. Delete Run Unit test
 2. Project Run Unit test
 3. Change Project Name Unit test
 4. Save Project Unit test
 5. Change Algorithm Unit test
 6. Filter scanned files Unit test
 7. Import Project Unit test

