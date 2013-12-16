# -*- mode: python -*-
a = Analysis(['AutoFix'],
             pathex=['d:\\python\\Fixity'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='AutoFix.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='images\\logo_sign_small.ico')
