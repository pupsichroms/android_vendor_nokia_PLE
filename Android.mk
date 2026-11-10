# Prebuilt modules live in Android.bp; product copy selections in PLE-vendor.mk.
LOCAL_PATH := $(call my-dir)

# Exact619F data configs place the XML declaration after the copyright comment.
# Keep their accepted bytes through ETC prebuilts, not XML-normalizing copy rules.
include $(CLEAR_VARS)
LOCAL_MODULE := ple-netmgr-config
LOCAL_MODULE_CLASS := ETC
LOCAL_VENDOR_MODULE := true
LOCAL_MODULE_PATH := $(TARGET_OUT_VENDOR)/etc/data
LOCAL_MODULE_STEM := netmgr_config.xml
LOCAL_PREBUILT_MODULE_FILE := $(PLE_NETMGR_CONFIG)
include $(BUILD_PREBUILT)

ifeq ($(PLE_CELLULAR_BAM_RTM),true)
include $(CLEAR_VARS)
LOCAL_MODULE := ple-dsi-config
LOCAL_MODULE_CLASS := ETC
LOCAL_VENDOR_MODULE := true
LOCAL_MODULE_PATH := $(TARGET_OUT_VENDOR)/etc/data
LOCAL_MODULE_STEM := dsi_config.xml
LOCAL_PREBUILT_MODULE_FILE := vendor/nokia/PLE/proprietary/vendor/etc/data/dsi_config.xml
include $(BUILD_PREBUILT)
endif
