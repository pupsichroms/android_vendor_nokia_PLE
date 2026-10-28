# Phase 8 initial proprietary boundary

The initial LineageOS Recovery target selects zero proprietary payloads.
Recovery uses the source-built 4.19 kernel framebuffer, input, storage, and USB
configfs paths, so no stock userspace binary has a proven boot-critical role at
this stage. Adding an unnecessary Android 9 executable or library would enlarge
the compatibility and licensing boundary without improving recovery startup.

`blob-spec.tsv` is therefore header-only. The generated `provenance.tsv` and
`elf-closure.tsv` record zero selected files, zero ELF records, and zero
unresolved edges. The generator still validates all future rows against the
exact extracted `Nokia6_V6.19F` filesystem path and SHA-256 before copying a
payload. It rejects Android 8.1/5580, modified LineageOS 18.1, Xiaomi, paths
outside stock, missing licenses, and hash mismatches.

Graphics, camera, radio, audio, and other stock blobs are not implicitly
approved by this empty recovery boundary. They require separate Phase 8/9 ABI
closure and runtime justification before being added.
