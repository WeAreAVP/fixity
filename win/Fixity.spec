# -*- mode: python -*-
a = Analysis(['Fixity.py'],
             pathex=['d:\\python\\Fixity\\win'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Fixity.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='images\\logo_sign_small.ico')
