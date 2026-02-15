[app]
title = ORI SCION
package.name = scionsix
package.domain = org.svontz
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy

# (Host) High-Fidelity Target
android.api = 35
android.minapi = 21
android.sdk = 35
android.ndk = 27b
android.archs = arm64-v8a

# Sovereign Permissions
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, QUERY_ALL_PACKAGES

# Build Optimizations
android.release_artifact = apk
android.debug_artifact = apk
p4a.branch = master
