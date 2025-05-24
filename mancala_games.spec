# -*- mode: python ; coding: utf-8 -*-

options = [('O', None, "OPTION")]

block_cipher = None

##  plays 

play_a = Analysis(
    ['src/play.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter.simpledialog'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=1,
)
play_pyz = PYZ(play_a.pure, play_a.zipped_data, cipher=block_cipher)

play_exe = EXE(
    play_pyz,
    play_a.scripts,
    [],
    exclude_binaries=True,
    name='play',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


## play_mancala

play_man_a = Analysis(
    ['src/play_mancala.pyw'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter.simpledialog'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=1,
)
play_man_pyz = PYZ(play_man_a.pure, play_man_a.zipped_data, cipher=block_cipher)

play_man_exe = EXE(
    play_man_pyz,
    play_man_a.scripts,
    [],
    exclude_binaries=True,
    name='play_mancala',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)


## mancala_games

man_games_a = Analysis(
    ['src/mancala_games.pyw'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter.simpledialog'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
    optimize=1,
)
man_games_pyz = PYZ(man_games_a.pure, man_games_a.zipped_data, cipher=block_cipher)

man_games_exe = EXE(
    man_games_pyz,
    man_games_a.scripts,
    [],
    exclude_binaries=True,
    name='mancala_games',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    play_exe,
    play_a.binaries,
    play_a.zipfiles,
    play_a.datas,
    
    play_man_exe,
    play_man_a.binaries,
    play_man_a.zipfiles,
    play_man_a.datas,
    
    man_games_exe,
    man_games_a.binaries,
    man_games_a.zipfiles,
    man_games_a.datas,
    
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MancalaGames',
)

