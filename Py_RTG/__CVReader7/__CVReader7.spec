# -*- mode: python -*-

block_cipher = None


a = Analysis(['стол\\__CVReader7', '-', 'Non', 'Gui\\icon.ico', 'mail.py'],
             pathex=['C:\\Users\\e_tas\\OneDrive\\Рабочий стол\\__CVReader7 - Non Gui'],
             binaries=[],
             datas=[],
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
          [],
          exclude_binaries=True,
          name='__CVReader7',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True , icon='C:\\Users\\e_tas\\OneDrive\\Рабочий')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='__CVReader7')
