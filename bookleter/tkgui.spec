# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

data_files = [
				('tkgui.ui', '.'),
			]

hidden_imports=[
				'pygubu.builder.ttkstdwidgets',
			 ]


a = Analysis(['tkgui.py'],
             pathex=['C:\\Users\\ela\\Desktop\\bookleter\\bookleter\\bookleter'],
             binaries=[],
			 datas = data_files,
             hiddenimports=hidden_imports,
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
          name='tkgui',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False )

coll = COLLECT(exe,
               a.datas,
               strip=False,
               upx=True,
               name='tkgui')
