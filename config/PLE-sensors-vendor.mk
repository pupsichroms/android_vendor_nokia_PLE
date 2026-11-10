# Exact PLE619F inputs; pins in sensors/stock.sha256. No factory calibration.
PRODUCT_COPY_FILES += \
    vendor/nokia/PLE/proprietary/vendor/bin/sensors.qti:$(TARGET_COPY_OUT_VENDOR)/bin/sensors.qti \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqmi_client_qmux.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqmi_client_qmux.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libdsutils.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libdsutils.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libmdmdetect.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libmdmdetect.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqmiservices.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqmiservices.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libidl.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libidl.so \
    vendor/nokia/PLE/proprietary/vendor/bin/qrtr-ns:$(TARGET_COPY_OUT_VENDOR)/bin/qrtr-ns \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqrtr.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqrtr.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/sensors.ssc.so:$(TARGET_COPY_OUT_VENDOR)/lib64/sensors.ssc.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libsensor1.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libsensor1.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libsensor_reg.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libsensor_reg.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqmi_cci.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqmi_cci.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqmi_csi.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqmi_csi.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqmi_common_so.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqmi_common_so.so \
    vendor/nokia/PLE/proprietary/vendor/lib64/libqmi_encdec.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libqmi_encdec.so \
    vendor/nokia/PLE/proprietary/vendor/etc/sensors/hals.conf:$(TARGET_COPY_OUT_VENDOR)/etc/sensors/hals.conf \
    vendor/nokia/PLE/proprietary/vendor/etc/sensors/sensor_def_qcomdev.conf:$(TARGET_COPY_OUT_VENDOR)/etc/sensors/sensor_def_qcomdev.conf \
    vendor/nokia/PLE/proprietary/vendor/etc/permissions/android.hardware.sensor.accelerometer.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.accelerometer.xml \
    vendor/nokia/PLE/proprietary/vendor/etc/permissions/android.hardware.sensor.compass.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.compass.xml \
    vendor/nokia/PLE/proprietary/vendor/etc/permissions/android.hardware.sensor.light.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.light.xml \
    vendor/nokia/PLE/proprietary/vendor/etc/permissions/android.hardware.sensor.proximity.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.proximity.xml \
    vendor/nokia/PLE/proprietary/vendor/etc/permissions/android.hardware.sensor.stepcounter.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.stepcounter.xml \
    vendor/nokia/PLE/proprietary/vendor/etc/permissions/android.hardware.sensor.stepdetector.xml:$(TARGET_COPY_OUT_VENDOR)/etc/permissions/android.hardware.sensor.stepdetector.xml
