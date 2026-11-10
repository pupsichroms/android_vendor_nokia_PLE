# Exact619F modem-storage prerequisite. No foreign modem/NV image is selected.
# User20261104 authorizes only normal daemon management of this phone's own NV.
PRODUCT_COPY_FILES += \
    vendor/nokia/PLE/proprietary/vendor/bin/rmt_storage:$(TARGET_COPY_OUT_VENDOR)/bin/rmt_storage \
    vendor/nokia/PLE/proprietary/vendor/bin/pm-service:$(TARGET_COPY_OUT_VENDOR)/bin/pm-service \
    vendor/nokia/PLE/proprietary/vendor/bin/pm-proxy:$(TARGET_COPY_OUT_VENDOR)/bin/pm-proxy \
    vendor/nokia/PLE/proprietary/vendor/lib64/libperipheral_client.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libperipheral_client.so

# libmdmdetect/current QMI are already selected by the accepted sensor layer;
# reuse the identical provider, never duplicate or replace that stack.
