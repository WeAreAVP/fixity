# -*- mode: python -*-
a = Analysis(['..\\..\\..\\mdqc\\MDQC MediaInfo\\Main.py'],
             pathex=['C:\\Users\\AVPS-Alex\\Desktop\\dev\\python libs\\pyinstaller-2.0'],
             hiddenimports=[],
             hookspath=None)
a.datas += [('images\\logo_sign_small.png', 'C:\\Users\\AVPS-Alex\\Desktop\\dev\\python libs\\pyinstaller-2.0\\logo_sign_small.png', 'DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'Main.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='logo_sign_small.ico')
app = BUNDLE(exe,
             name=os.path.join('dist', 'Main.exe.app'))
