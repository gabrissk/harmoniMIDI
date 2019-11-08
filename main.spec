# -*- mode: python ; coding: utf-8 -*-

import os.path

block_cipher = None


a = Analysis(['main.py'],
             pathex=['/home/gabriel.morais/Documentos/Projetos/poc'],
             binaries=[('/usr/lib/x86_64-linux-gnu/libfluidsynth.so.1', '.'), ('/usr/lib/x86_64-linux-gnu/libfluidsynth.so.1.5.2', '.')],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)


ICON = 'icon.svg'

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
