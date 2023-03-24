# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['ORTHO_STATUS.py'],
             pathex=[],
             binaries=[],
             datas=[('back_clear.bmp', '.'), ('body.bmp', '.'), ('foot_movements.bmp', '.'), ('front_clear.bmp', '.'), ('Ped_d.bmp', '.'), ('Ped_s.bmp', '.'), ('sagit_vertebra_fit.bmp', '.'), ('vertebra.bmp', '.'), ('wrists_l.bmp', '.'), ('wrists_r.bmp', '.'), ('samples_diagnosis.pickle', '.'), ('samples_manipulation.pickle', '.'), ('samples_appointment.pickle', '.'), ('samples_recomendation.pickle', '.'), ('icon.ico', '.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
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
          name='ORTHO_STATUS',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='icon.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='ORTHO_STATUS')
