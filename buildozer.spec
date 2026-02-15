[app]
android.sdk_path = /usr/local/lib/android/sdk
android.ndk_path = /usr/local/lib/android/sdk/ndk/27.3.13750724
title = ORI SCION AI
package.name = oriscion
package.domain = com.sovereign
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,md,txt,sh
version = 1.1
requirements = python3,kivy,kivymd,sdl2_ttf,pillow,requests,beautifulsoup4,gitpython,playwright
android.permissions = CAMERA,VIBRATE,INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 35
android.minapi = 24
android.ndk = 27.3.13750724
android.arch = arm64-v8a
p4a.bootstrap = sdl2
p4a.python_version = 3.11
[buildozer]
log_level = 2