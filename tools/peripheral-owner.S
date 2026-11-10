// Exact PLE619F pm-service main only: allocate the 96-byte manager using its
// existing operator new; relocate every live alias and retain a real main sp<>.
// No RefBase guard, Binder protocol, SSR/QMI or other function is modified.
.text
pm_start:
.equ pm_new, 0x3bc8
.equ ref_ctor, 0x3d68
.equ interface_ctor, 0x3d78
.equ binder_ctor, 0x3d88
.equ owner_acquire, 0x3e38
.equ owner_release, 0x3df8
.equ canary_epilogue, 0x5bf4
.macro call target, pc
    .inst 0x94000000 | (((\target - \pc) >> 2) & 0x03ffffff)
.endm
.macro adr_absolute reg, target, pc
    .inst 0x10000000 | (((\target - \pc) & 3) << 29) | ((((\target - \pc) >> 2) & 0x7ffff) << 5) | \reg
.endm
.org 0x559c
    mov w24, w0
    mov x23, x1
    stur x8, [x29, #-0x58]
    mov w0, #96
    call pm_new, 0x55ac
    mov x19, x0
    add x25, x19, #0x50
    mov x0, x25
    call ref_ctor, 0x55bc
    adr_absolute 20, 0x1f210, 0x55c0
    add x1, x20, #0x18
    mov x0, x19
    call interface_ctor, 0x55cc
    add x28, x19, #8
    add x1, x20, #0x38
    mov x0, x28
    call binder_ctor, 0x55dc
    adr_absolute 8, 0x1f0a8, 0x55e0
    add x9, x8, #0x78
    stp x8, x9, [x19]
    add x8, x8, #0x138
    stp xzr, x8, [x19, #0x48]
    add x9, x19, #0x20
    stp x9, x9, [x19, #0x20]
    stp xzr, xzr, [x19, #0x38]
    str xzr, [x19, #0x30]
    stp xzr, x28, [sp, #0x38]
    mov x0, x25
    add x1, sp, #0x40
    call owner_acquire, 0x5610
.org 0x56e4
    sub x0, x28, #8
.org 0x585c
    ldr x8, [x28]
.org 0x58dc
    sub x19, x28, #8
.org 0x5968
    ldr x21, [x28, #0x20]
.org 0x5a18
    ldr x19, [x28, #0x20]
.org 0x5ac4
    ldr x19, [x28, #0x20]
    sub x8, x28, #8
.org 0x5aec
    ldr x19, [x28, #0x20]
.org 0x5b5c
    mov x0, x25
    add x1, sp, #0x40
    call owner_release, 0x5b64
    .inst 0x14000000 | (((canary_epilogue - 0x5b68) >> 2) & 0x03ffffff)
