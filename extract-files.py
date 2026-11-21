#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/samsung/sm8350-common',
    'vendor/samsung/sm8350-common',
    'vendor/qcom/opensource/display',
]


blob_fixups: blob_fixups_user_type = {
    # Samsung HIDL interfaces have no hidl_interface in the build, so host_init_verifier
    # rejects them. The services still register at boot with class hal
    (
        'vendor/etc/init/nxp.android.hardware.nfc@1.2-service.rc',
        'vendor/etc/init/vendor.samsung.hardware.camera.provider@4.0-service_64.rc',
    ): blob_fixup()
        .regex_replace(r'\n[ \t]*interface vendor\.samsung\.hardware\.[^\n]*', ''),
    # android::base::Trim(const std::string&) is gone from Android 16's libbase
    'vendor/lib64/nfc_nci_nxpsn.so': blob_fixup()
        .add_needed('libbase_shim.so'),
    # Loaded inside the camera provider with the binder pool already running, and
    # Android 16's libhidlbase aborts ("Binder threadpool cannot be shrunk")
    'vendor/lib64/vendor.qti.hardware.camera.postproc@1.0-service-impl.so': blob_fixup()
        .add_needed('libhidlbase_shim_sm8350.so')
        .binary_regex_replace(b'_ZN7android8hardware22configureRpcThreadpoolEmb',
                              b'_ZN7android8hardware22configureRpcTh_pathcedEmb'),
    # ALooper_*_forCamera from Samsung's libsensorndkbridge; without them CamX can't
    # load com.ss.stats.aec and aborts when opening any camera
    (
        'vendor/lib/libsensorlistener.so',
        'vendor/lib/libvdis_core.so',
        'vendor/lib64/libhypermotion_core.so',
        'vendor/lib64/libsensorlistener.so',
        'vendor/lib64/libvdis_core.so',
    ): blob_fixup()
        .add_needed('libsensorndkbridge_shim.so'),
    'vendor/lib64/hw/camera.qcom.so': blob_fixup()
        .binary_regex_replace(b'ro.boot.flash.locked', b'ro.camera.notify_nfc'),
    'vendor/lib64/hw/com.qti.chi.override.so': blob_fixup()
        # SecUsecaseFastAec::Initialize creates its mutex after Session::Initialize, but the
        # pipeline finalize thread notifies earlier: SessionCbNotifyMessage locks a null
        # mutex and crashes the provider on camera open. The callback only logs, so
        # make it return right away (GXF1)
        .sig_replace(
            'FF C3 00 D1 FD 7B 01 A9 FD 43 00 91 F4 4F 02 A9 34 00 40 F9 F3 03 00 AA 14 01 00 B4 88 02 40 F9 '
            '2A 09 00 B0 4A A1 02 91 0B 5E 84 52 4C 01 0B 8B 1F 01 0C EB E1 00 00 54 28 08 40 B9 28 02 00 34 '
            'F4 4F 42 A9 FD 7B 41 A9 FF C3 00 91 C0 03 5F D6 60 F4 94 D2 62 1B 00 F0 20 DC A5 F2 42 C0 13 91 '
            'A0 76 C1 F2 E1 07 00 F9 20 58 FA F2 E1 03 08 AA 9A 74 04 94 E1 07 40 F9 28 08 40 B9 28 FE FF 35',
            'FF C3 00 D1 FD 7B 01 A9 FD 43 00 91 F4 4F 02 A9 34 00 40 F9 F3 03 00 AA 14 01 00 B4 88 02 40 F9 '
            '2A 09 00 B0 4A A1 02 91 0B 5E 84 52 4C 01 0B 8B 1F 01 0C EB E1 00 00 54 28 08 40 B9 1F 20 03 D5 '
            'F4 4F 42 A9 FD 7B 41 A9 FF C3 00 91 C0 03 5F D6 60 F4 94 D2 62 1B 00 F0 20 DC A5 F2 42 C0 13 91 '
            'A0 76 C1 F2 E1 07 00 F9 20 58 FA F2 E1 03 08 AA 9A 74 04 94 E1 07 40 F9 28 08 40 B9 F1 FF FF 17'
        )
        .sig_replace(
            '80 06 40 F9 2D 79 00 94 80 01 00 34 A2 DB FF B0 C3 DD FF D0 A5 DC FF F0 E6 03 00 2A',
            '1F 20 03 D5 1F 20 03 D5 1F 20 03 D5 1F 20 03 D5 1F 20 03 D5 1F 20 03 D5 1F 20 03 D5'
        )
        .sig_replace(
            '42 EC 2F 91 63 70 1E 91 A5 34 30 91 A4 11 80 52 E0 03 1F 2A 21 00 80 52 8D FE FF 97 80 06 40 F9',
            '1F 20 03 D5 1F 20 03 D5 1F 20 03 D5 1F 20 03 D5 1F 20 03 D5 1F 20 03 D5 1F 20 03 D5 80 06 40 F9'
        ),
}  # fmt: skip

module = ExtractUtilsModule(
    'r9q',
    'samsung',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device_with_common(
        module, 'sm8350-common', module.vendor
    )
    utils.run()
