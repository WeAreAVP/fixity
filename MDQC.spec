# -*- mode: python -*-
a = Analysis(['MDQC.py'],
             pathex=['C:\\PyInstaller\\pyinstaller.py'],
             hiddenimports=[],
             hookspath=None)
a.datas += [('images\\logo_sign_small.png', 'images\\logo_sign_small.png', 'DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'MDQC.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='icon.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'MDQC.exe.app'))
