# Experimental Adreno 845 bring-up

Validated against Mesa commit `5a2730169b755d3594b2313eb92cb08826884d09` using the balanced Android and Linux builds.

## Device profile

- KGSL chip ID: `0x44041430`.
- A8xx gen2 profile; 3 slices, 6 CCUs and 12 MiB GMEM reported by the attached device.
- GMEM rendering remains disabled. Only sysmem rendering has been validated.

`patches/add_a845.py` adds the retail device profile. Both build entrypoints apply it. The A825 profile and Linux mesh-shader patch are adapted to the same Mesa API used for the successful builds.

## Validation

Device creation, GPU submission, compute readback, image clear, graphics readback, Steam Big Picture presentation, BC1/BC3 texture sampling and RGBA16F LUT compute/raster tests passed on the device. These checks do not establish Vulkan conformance or general game compatibility.

## Unity game rendering workaround

Magical Girl Witch Trials / manosaba (Steam app 3101040, Unity 6000.0.48f1) initially showed a black window with Direct3D 11. Native Vulkan displayed the game but rendered character/background images in grayscale.

The uploaded textures were colored and the captured saturation parameter was 1. Replaying the original game LUT fragment SPIR-V with captured uniforms and default curve inputs produced 31,744 incorrect channels versus lavapipe. With `IR3_SHADER_DEBUG=expandrpt`, that count fell to zero at an absolute-error threshold of 0.01; the maximum difference was approximately 0.00006166.

The validated per-game settings are:

- Steam launch options: `-force-vulkan`.
- Game environment: `IR3_SHADER_DEBUG=expandrpt`.

Two launches displayed colored title menus and entered colored story scenes; dialogue and scene transitions advanced. Temporary capture/logging and cache-disable overrides were removed. Long-duration stability is unverified. The exact instruction encoding or hardware restriction causing the repeat-path error has not been isolated, so this patch does not introduce a permanent IR3 workaround or enable it globally.
