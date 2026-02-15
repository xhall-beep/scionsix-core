[app]
title = ORI SCION AI
package.name = oriscion
package.domain = com.sovereign
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,md,txt,sh
version = 1.1
requirements = python3,kivy,requests,beautifulsoup4,gitpython,playwright
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 34
android.minapi = 21
android.ndk = 25b
android.arch = arm64-v8a
p4a.bootstrap = sdl2
p4a.python_version = 3.11
[buildozer]
log_level = 2