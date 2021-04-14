# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['Encoder_Control_GUI.py'],
             pathex=['/home/pi/Documents/GUIPythonEncodeur/GUI'],
             binaries=[],
             datas=[('/home/pi/.local/lib/python3.7/site-packages/matplotlib/mpl-data/matplotlibrc','/matplotlib/mpl-data/')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Encoder_Control_GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
