# -*- mode: python -*-

block_cipher = None


a = Analysis(['__init__.py'],
             pathex=['gpa_analyser'],
             binaries=[],
             datas=None,
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=['FixTk', 'tcl', 'tk', '_tkinter', 'tkinter', 'Tkinter'],
             win_no_prefer_redirects=None,
             win_private_assemblies=None,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='gpa_analyser',
          debug=False,
          strip=None,
          upx=True,
          console=True )
