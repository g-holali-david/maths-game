# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['jeu_math_app/main.py'],  # Chemin mis à jour vers 'main.py'
    pathex=['.'],
    binaries=[],
    datas=[('jeu_math_app/config.json', 'jeu_math_app'), ('jeu_math_app/main.py', 'jeu_math_app'), ('jeu_math_app/app_icon.ico', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='jeu_math',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    icon='jeu_math_app/app_icon.ico'  # Chemin vers votre fichier .ico
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='jeu_math',
)
