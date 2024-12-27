[app]

# (str) Title of your application
title = CPL_CalculatorApp

# (str) Package name
package.name = CPLApk

# (str) Package domain (needed for android/ios packaging)
package.domain = org.telecom_meknes

# (str) Source code directory where the main.py file resides
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (list) Include specific patterns of files
source.include_patterns = images/*.png

# (str) Application version
version = 0.1

# (list) Application requirements
# Include all necessary libraries here
requirements = python3,kivy,kivymd,pillow

# (str) Presplash screen image
presplash.filename = %(source.dir)s/images/presplash.png

# (str) Application icon
icon.filename = %(source.dir)s/images/favicon.png

# (list) Supported orientations
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 1

# (list) Android architecture to build for
android.archs = arm64-v8a,armeabi-v7a

# (bool) Allow Android auto-backup feature
android.allow_backup = True

# (str) Package format for debug mode
android.debug_artifact = apk

# (str) Package format for release mode
android.release_artifact = apk

# (str) Python-for-android branch to use
p4a.branch = master

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
