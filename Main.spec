# -*- mode: python -*-
a = Analysis(['Main.py'],
             pathex=['d:\\python\\Fixity Project'],
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
          console=False , icon='assets\\icon.ico')




# -*- mode: python -*-
a = Analysis(['Main.py'],
             pathex=['C:\\PyInstaller\\pyinstaller.py'],
             hiddenimports=[],
             hookspath=None)
a.datas += [('assets\\logo_sign_small.png', 'assets\\logo_sign_small.png','DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'Fixity.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True , icon='assets\\icon.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'Fixity.exe.app'))



