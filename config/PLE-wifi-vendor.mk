# SPDX-License-Identifier: Apache-2.0
# Exact PLE619F files, see device/nokia/PLE/docs/wifi-provenance.md.
PRODUCT_COPY_FILES += \
    vendor/nokia/PLE/proprietary/vendor/etc/wifi/WCNSS_qcom_cfg.ini:$(TARGET_COPY_OUT_VENDOR)/etc/wifi/WCNSS_qcom_cfg.ini \
    vendor/nokia/PLE/proprietary/vendor/firmware/wlan/prima/WCNSS_cfg.dat:$(TARGET_COPY_OUT_VENDOR)/firmware/wlan/prima/WCNSS_cfg.dat
