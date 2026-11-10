# SPDX-License-Identifier: Apache-2.0
# Generated payloads: extract-goodix.py; input/output hashes: proprietary-goodix/provenance.tsv.
PLE_GOODIX_BLOBS := vendor/nokia/PLE/proprietary/vendor
PRODUCT_COPY_FILES += \
    $(PLE_GOODIX_BLOBS)/bin/gx_fpd:$(TARGET_COPY_OUT_VENDOR)/bin/gx_fpd \
    $(PLE_GOODIX_BLOBS)/lib64/libstdc++.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libstdc++.so \
    $(PLE_GOODIX_BLOBS)/lib64/libfpservice.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libfpservice.so \
    $(PLE_GOODIX_BLOBS)/lib64/libfp_client.so:$(TARGET_COPY_OUT_VENDOR)/lib64/libfp_client.so \
    $(PLE_GOODIX_BLOBS)/lib64/hw/fingerprint.goodix.so:$(TARGET_COPY_OUT_VENDOR)/lib64/hw/fingerprint.goodix.so \
    $(PLE_GOODIX_BLOBS)/lib64/hw/gxfingerprint.default.so:$(TARGET_COPY_OUT_VENDOR)/lib64/hw/gxfingerprint.default.so
PRODUCT_COPY_FILES += $(foreach name,goodixfp goodixfplv, \
    $(foreach ext,mdt b00 b01 b02 b03 b04 b05 b06, \
    $(PLE_GOODIX_BLOBS)/firmware/$(name).$(ext):$(TARGET_COPY_OUT_VENDOR)/firmware/$(name).$(ext)))
