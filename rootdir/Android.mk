LOCAL_PATH := $(call my-dir)

# Init files

include $(CLEAR_VARS)
LOCAL_MODULE       := init.r9q.rc
LOCAL_MODULE_TAGS  := optional
LOCAL_MODULE_CLASS := ETC
LOCAL_SRC_FILES    := etc/init.r9q.rc
LOCAL_MODULE_PATH  := $(TARGET_OUT_VENDOR_ETC)/init/hw
include $(BUILD_PREBUILT)

# init_sm8350 sets the r9q2 codename on SM-G990B2 and init.target.rc imports
# init.${ro.product.vendor.device}.rc
include $(CLEAR_VARS)
LOCAL_MODULE       := init.r9q2.rc
LOCAL_MODULE_TAGS  := optional
LOCAL_MODULE_CLASS := ETC
LOCAL_SRC_FILES    := etc/init.r9q.rc
LOCAL_MODULE_PATH  := $(TARGET_OUT_VENDOR_ETC)/init/hw
include $(BUILD_PREBUILT)
