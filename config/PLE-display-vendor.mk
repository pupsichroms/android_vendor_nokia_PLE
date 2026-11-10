# Exact PLE 619F SDM strategy + scalar dependency; source-built core/HWC stay unchanged.
# PLE-qualified Device composition, normal boot and blank/wake; explicit opt-out retained.
PLE_ENABLE_STOCK_SDM_EXTENSION ?= true
ifeq ($(PLE_ENABLE_STOCK_SDM_EXTENSION),true)
PRODUCT_COPY_FILES += \
    vendor/nokia/PLE/proprietary/vendor/lib64/libsdmextension.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libsdmextension.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libscalar.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libscalar.so
endif
