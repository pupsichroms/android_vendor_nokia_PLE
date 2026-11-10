# Exact619F selection/extraction/provenance remains local; no common tree.
PRODUCT_PACKAGES += \
    audio.primary.ple lib_FIH_SmartAmp libtinycompress_vendor \
    libaudio_log_utils libacdbloader libaudcal libacdbrtac libadiertac \
    libacdb-fts libdiag.pleaudio libadm

PLE_AUDIO_STOCK := vendor/nokia/PLE/proprietary/vendor
PRODUCT_COPY_FILES += \
    $(PLE_AUDIO_STOCK)/etc/mixer_paths_ple.xml:$(TARGET_COPY_OUT_VENDOR)/etc/mixer_paths_ple.xml \
    $(PLE_AUDIO_STOCK)/etc/audio_platform_info_ple.xml:$(TARGET_COPY_OUT_VENDOR)/etc/audio_platform_info_ple.xml
PRODUCT_COPY_FILES += $(foreach name,Bluetooth General Global Handset Hdmi Headset Speaker, \
    $(PLE_AUDIO_STOCK)/etc/acdbdata/PLE/$(name)_cal.acdb:$(TARGET_COPY_OUT_VENDOR)/etc/acdbdata/PLE/$(name)_cal.acdb)
PRODUCT_COPY_FILES += \
    $(PLE_AUDIO_STOCK)/etc/acdbdata/PLE/WorkspaceFile.qwsp:$(TARGET_COPY_OUT_VENDOR)/etc/acdbdata/PLE/WorkspaceFile.qwsp
PRODUCT_COPY_FILES += $(foreach name,Tfa9891_PLE_top.cnt Tfa9891_PLE_bot.cnt, \
    $(PLE_AUDIO_STOCK)/etc/NXPsmartamp/settings/$(name):$(TARGET_COPY_OUT_VENDOR)/etc/NXPsmartamp/settings/$(name))
