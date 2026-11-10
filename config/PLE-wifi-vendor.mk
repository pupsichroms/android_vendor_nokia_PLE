# SPDX-License-Identifier: Apache-2.0
# Exact PLE619F paths and hashes: config/manifests/wifi.tsv; use extract-files.sh.
PRODUCT_COPY_FILES += \
    vendor/nokia/PLE/proprietary/vendor/etc/wifi/WCNSS_qcom_cfg.ini:$(TARGET_COPY_OUT_VENDOR)/etc/wifi/WCNSS_qcom_cfg.ini \
    vendor/nokia/PLE/proprietary/vendor/firmware/wlan/prima/WCNSS_cfg.dat:$(TARGET_COPY_OUT_VENDOR)/firmware/wlan/prima/WCNSS_cfg.dat
