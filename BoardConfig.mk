#
# Copyright (C) 2023 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

DEVICE_PATH := device/samsung/r9q

include device/samsung/sm8350-common/BoardConfigCommon.mk

# Kernel
TARGET_KERNEL_CONFIG        := vendor/r9q_eur_openx2_defconfig
# r530567 (used by the common tree) is gone from the Android 16 prebuilts
TARGET_KERNEL_CLANG_VERSION := r547379
BOARD_NAME                 := SRPVC21A007

# Kernel modules
BOARD_VENDOR_KERNEL_MODULES_LOAD := $(strip $(shell cat $(DEVICE_PATH)/modules.load))
# vendor_modprobe.sh (early-init) loads every module with -b: wlan waits for
# cnss2 calibration, which only starts in post-fs-data, blocking init for 70 s.
# init.r9q.rc loads it on boot
BOARD_VENDOR_KERNEL_MODULES_BLOCKLIST_FILE := $(DEVICE_PATH)/modules.blocklist
BOARD_RECOVERY_RAMDISK_KERNEL_MODULES_LOAD := $(strip $(shell cat $(DEVICE_PATH)/modules.load.recovery))
RECOVERY_KERNEL_MODULES := $(BOARD_RECOVERY_RAMDISK_KERNEL_MODULES_LOAD)

# Recovery
TARGET_BOARD_INFO_FILE := $(DEVICE_PATH)/board-info.txt

# Display
TARGET_SCREEN_DENSITY := 450

# OTA assert
TARGET_OTA_ASSERT_DEVICE := r9q

# Security patch
VENDOR_SECURITY_PATCH := 2024-06-01

# UDFPS
TARGET_SURFACEFLINGER_UDFPS_LIB := //$(DEVICE_PATH):libudfps_extension.r9q
TARGET_ADDITIONAL_GRALLOC_10_USAGE_BITS := 0x2000U | 0x400000000LL
SOONG_CONFIG_qtidisplay_udfps := true

# Properties
TARGET_VENDOR_PROP += $(DEVICE_PATH)/vendor.prop
