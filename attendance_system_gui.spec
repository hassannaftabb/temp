# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['attendance_system_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('venv310/Lib/site-packages/face_recognition_models/models/dlib_face_recognition_resnet_model_v1.dat', 'face_recognition_models/models'),
        ('venv310/Lib/site-packages/face_recognition_models/models/mmod_human_face_detector.dat', 'face_recognition_models/models'),
        ('venv310/Lib/site-packages/face_recognition_models/models/shape_predictor_5_face_landmarks.dat', 'face_recognition_models/models'),
        ('venv310/Lib/site-packages/face_recognition_models/models/shape_predictor_68_face_landmarks.dat', 'face_recognition_models/models'),
        ('venv310/Lib/site-packages/cv2/opencv_videoio_ffmpeg4110_64.dll', 'cv2'),
        ('venv310/Lib/site-packages/cv2/cv2.pyd', '.'),
        ('venv310/Lib/site-packages/cv2', 'cv2'),    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='attendance_system_gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
