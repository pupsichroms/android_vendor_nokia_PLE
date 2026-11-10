# Exact PLE619F plugins. Reproduce with extract-camera.py --manifest
# media/stock.sha256 --output media/proprietary --stock-system STOCK_SYSTEM.
# AVC only is registered until other hardware formats have been device-tested.
PRODUCT_COPY_FILES += \
    vendor/nokia/PLE/proprietary/vendor/lib/libstagefrighthw.so:$(TARGET_COPY_OUT_VENDOR)/lib/libstagefrighthw.so \
    vendor/nokia/PLE/proprietary/vendor/lib/libmm-omxcore.so:$(TARGET_COPY_OUT_VENDOR)/lib/libmm-omxcore.so \
    vendor/nokia/PLE/proprietary/vendor/lib/libOmxCore.so:$(TARGET_COPY_OUT_VENDOR)/lib/libOmxCore.so \
    vendor/nokia/PLE/proprietary/vendor/lib/libOmxVenc.so:$(TARGET_COPY_OUT_VENDOR)/lib/libOmxVenc.so \
    vendor/nokia/PLE/proprietary/vendor/lib/libOmxVdec.so:$(TARGET_COPY_OUT_VENDOR)/lib/libOmxVdec.so \
    vendor/nokia/PLE/proprietary/vendor/lib/libc2dcolorconvert.so:$(TARGET_COPY_OUT_VENDOR)/lib/libc2dcolorconvert.so \
    vendor/nokia/PLE/proprietary/vendor/lib/libhypv_intercept.so:$(TARGET_COPY_OUT_VENDOR)/lib/libhypv_intercept.so
