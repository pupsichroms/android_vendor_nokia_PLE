# Exact619F legacy-RIL private inputs; current platform Binder/HIDL/SQLite stay source-built.
PRODUCT_COPY_FILES += \
    vendor/nokia/PLE/proprietary/vendor/lib64/libconfigdb.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libconfigdb.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libdsi_netctrl.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libdsi_netctrl.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/liblqe.so:$(TARGET_COPY_OUT_VENDOR)/lib64/liblqe.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libnetmgr.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libnetmgr.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqdi.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqdi.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqdp.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqdp.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqmi.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqmi.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqmi_client_helper.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqmi_client_helper.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libril-qc-ltedirectdisc.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libril-qc-ltedirectdisc.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libril-qc-qmi-1.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libril-qc-qmi-1.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libril-qc-radioconfig.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libril-qc-radioconfig.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libril-qcril-hook-oem.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libril-qcril-hook-oem.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/librilqmiservices.so:$(TARGET_COPY_OUT_VENDOR)/lib64/librilqmiservices.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libsettings.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libsettings.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libsystem_health_mon.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libsystem_health_mon.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libxml.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libxml.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.radio.am@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.radio.am@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.radio.ims@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.radio.ims@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.radio.lpa@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.radio.lpa@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.radio.qcrilhook@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.radio.qcrilhook@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.radio.qtiradio@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.radio.qtiradio@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.radio.uim@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.radio.uim@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.radio.uim@1.1.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.radio.uim@1.1.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.radio.uim_remote_client@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.radio.uim_remote_client@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/vendor.qti.hardware.radio.uim_remote_server@1.0.so:$(TARGET_COPY_OUT_VENDOR)/lib64/vendor.qti.hardware.radio.uim_remote_server@1.0.so \
    vendor/nokia/PLE/proprietary/vendor/radio/qcril_database/qcril.db:$(TARGET_COPY_OUT_VENDOR)/radio/qcril_database/qcril.db \
    vendor/nokia/PLE/proprietary/vendor/radio/qcril_database/upgrade/0_initial.sql:$(TARGET_COPY_OUT_VENDOR)/radio/qcril_database/upgrade/0_initial.sql \
    vendor/nokia/PLE/proprietary/vendor/radio/qcril_database/upgrade/1_version_intro.sql:$(TARGET_COPY_OUT_VENDOR)/radio/qcril_database/upgrade/1_version_intro.sql \
    vendor/nokia/PLE/proprietary/vendor/radio/qcril_database/upgrade/2_version_add_wps_config.sql:$(TARGET_COPY_OUT_VENDOR)/radio/qcril_database/upgrade/2_version_add_wps_config.sql \
    vendor/nokia/PLE/proprietary/vendor/radio/qcril_database/upgrade/3_version_update_wps_config.sql:$(TARGET_COPY_OUT_VENDOR)/radio/qcril_database/upgrade/3_version_update_wps_config.sql
