# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['harmoniMIDI.py'],
             pathex=['/home/gabriel/Desktop/poc/poc'],
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
          a.binaries + [('libfluidsynth.so.1', '/usr/lib/x86_64-linux-gnu/libfluidsynth.so.1', 'BINARY')],
          a.zipfiles,
          a.datas,
          [],
          name='harmoniMIDI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
