import os

def setImportBaseBath():
    base_path = os.getcwd()
    base_path = base_path.replace(r'\test', '')
    base_path = base_path.replace(r'\AllFixture', '')
    base_path = base_path.replace(r'/test', '')
    base_path = base_path.replace(r'/AllFixture', '')
    return base_path+os.sep