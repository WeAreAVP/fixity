# -*- mode: python -*-
a = Analysis(['Main.py'],
             pathex=['c:\\Users\\Xohotech\\Desktop\\projects\\fixity'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Main.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False )
