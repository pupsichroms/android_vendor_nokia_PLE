# Exact619F data transport; Binder/HIDL/netutils/netd interfaces remain maintained platform modules.
PLE_NETMGR_CONFIG := vendor/nokia/PLE/proprietary/variants/radio-data/vendor/etc/data/netmgr_config.xml
PLE_NETMGR_DAEMON := vendor/nokia/PLE/proprietary/variants/radio-data/vendor/bin/netmgrd
# Device default selects the installed/packet-tested v5; false retains v1 fallback.
ifeq ($(PLE_CELLULAR_BAM_RTM),true)
PLE_NETMGR_CONFIG := vendor/nokia/PLE/proprietary/vendor/etc/data/netmgr_config.xml
PLE_NETMGR_DAEMON := vendor/nokia/PLE/proprietary/vendor/bin/netmgrd
PRODUCT_PACKAGES += ple-dsi-config
endif
PRODUCT_PACKAGES += ple-netmgr-config
PRODUCT_COPY_FILES += \
    $(PLE_NETMGR_DAEMON):$(TARGET_COPY_OUT_VENDOR)/bin/netmgrd \
    vendor/nokia/PLE/proprietary/vendor/lib64/com.quicinc.cne.api@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/com.quicinc.cne.api@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/com.quicinc.cne.api@1.1.so:$(TARGET_COPY_OUT_VENDOR)/lib64/com.quicinc.cne.api@1.1.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/com.quicinc.cne.constants@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/com.quicinc.cne.constants@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/com.quicinc.cne.constants@2.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/com.quicinc.cne.constants@2.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/com.quicinc.cne.constants@2.1.so:$(TARGET_COPY_OUT_VENDOR)/lib64/com.quicinc.cne.constants@2.1.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/com.quicinc.cne.server@2.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/com.quicinc.cne.server@2.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/com.quicinc.cne.server@2.1.so:$(TARGET_COPY_OUT_VENDOR)/lib64/com.quicinc.cne.server@2.1.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/com.quicinc.cne.server@2.2.so:$(TARGET_COPY_OUT_VENDOR)/lib64/com.quicinc.cne.server@2.2.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libcneapiclient.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libcneapiclient.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libnetmgr_common.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libnetmgr_common.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libnlnetmgr.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libnlnetmgr.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/librmnetctl.so:$(TARGET_COPY_OUT_VENDOR)/lib64/librmnetctl.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.data.factory@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.data.factory@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.data.dynamicdds@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.data.dynamicdds@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.data.qmi@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.data.qmi@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.ims.rcsconfig@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.ims.rcsconfig@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.latency@2.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.latency@2.0.so
