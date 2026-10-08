#!/usr/bin/env python3
"""Bring up retail Adreno 845 (Maili), KGSL chip_id 0x44041430.

Qualcomm's 2026-09-23 A845 kernel series identifies A8XX_GEN2, three
slices, the six-SP mask 0x3f, and 12 MiB GMEM. The attached device
confirms the chip ID and GMEM via KGSL_PROP_DEVICE_INFO.
Start with GPU sysmem rendering while the new GMEM layout is validated.
"""
from pathlib import Path
p = Path('src/freedreno/common/freedreno_devices.py')
s = p.read_text()
if 'GPUId(chip_id=0x44041430' in s:
    raise SystemExit('A845 already present; review upstream support before applying')
anchor = 'add_gpus([\n        GPUId(chip_id=0xffff44050A31'
if s.count(anchor) != 1:
    raise SystemExit('A840 insertion anchor changed')
entry = '''# Maili / Adreno 845: KGSL retail revision observed on SM8950.
# A8XX_GEN2 and 3 slices / 6 SPs: Qualcomm A845 kernel bring-up series.
# GPU sysmem first: do not assume the 12 MiB GMEM layout matches A840.
add_gpus([
        GPUId(chip_id=0x44041430, name="Adreno (TM) 845"),
    ], A6xxGPUInfo(
        CHIP.A8XX,
        [a7xx_base, a7xx_gen3, a8xx_base, a8xx_gen2,
         GPUProps(shading_rate_matches_vk = True, disable_gmem = True)],
        num_ccu = 6,
        num_slices = 3,
        tile_align_w = 96,
        tile_align_h = 32,
        tile_max_w = 16416,
        tile_max_h = 16384,
        num_vsc_pipes = 32,
        cs_shared_mem_size = 32 * 1024,
        wave_granularity = 2,
        fibers_per_sp = 128 * 2 * 16,
        raw_magic_regs = a8xx_base_raw_magic_regs,
    ))

'''
p.write_text(s.replace(anchor, entry + anchor))
print('Applied A845 KGSL 0x44041430, A8xx gen2, 6 CCUs, 3 slices, GPU sysmem bring-up')
