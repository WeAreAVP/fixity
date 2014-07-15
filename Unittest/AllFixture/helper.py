import os

def setImportBaseBath():
    base_path = os.getcwd()
    base_path = base_path.replace(r'\Unittest', '')
    base_path = base_path.replace(r'\AllFixture', '')
    base_path = base_path.replace(r'/Unittest', '')
    base_path = base_path.replace(r'/AllFixture', '')
    return os.path.join(base_path,'')