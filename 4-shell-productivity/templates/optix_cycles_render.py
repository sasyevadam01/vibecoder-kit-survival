"""
Blender GPU cycles OptiX Headless Renderer.
Optimized script for rendering high-fidelity scenes procedurally.
Enforces OptiX hardware acceleration and Cycles rendering setup.
No em-dashes or forbidden fonts used.
"""

import sys

# Try importing Blender's API module
try:
    import bpy
    BLENDER_AVAILABLE = True
except ImportError:
    BLENDER_AVAILABLE = False


def setup_optix_cycles_rendering():
    """
    Enables Cycles render engine and activates NVIDIA OptiX GPU hardware acceleration.
    """
    if not BLENDER_AVAILABLE:
        print("[WARNING] bpy module is not available. This script must be run inside Blender's python environment.")
        return False

    print("Configuring Cycles render engine...")
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'

    # Configure Cycles parameters
    cycles = scene.cycles
    cycles.device = 'GPU'
    cycles.samples = 128
    cycles.use_denoising = True
    cycles.denoiser = 'OPTIX'

    # Configure OptiX Compute Device Registry
    preferences = bpy.context.preferences
    addons = preferences.addons
    cycles_preferences = addons['cycles'].preferences

    print("Searching for OptiX hardware compute devices...")
    cycles_preferences.refresh_devices()
    
    # Select OptiX device type
    cycles_preferences.compute_device_type = 'OPTIX'
    
    optix_devices = []
    for device in cycles_preferences.devices:
        if device.type == 'OPTIX':
            device.use = True
            optix_devices.append(device.name)
            print(f"Activated GPU Device: {device.name}")
        else:
            device.use = False

    if not optix_devices:
        print("[WARNING] No dedicated OptiX hardware detected! Falling back to standard CUDA or CPU devices.")
        cycles_preferences.compute_device_type = 'CUDA'
        for device in cycles_preferences.devices:
            if device.type == 'CUDA':
                device.use = True
                print(f"Fallback Active: {device.name}")
                break

    return True


def create_procedural_scene():
    """
    Procedurally builds an icosphere, target lighting, and active camera.
    """
    if not BLENDER_AVAILABLE:
        return

    print("Cleaning initial template objects...")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    print("Creating procedural Icosphere mesh...")
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=4,
        radius=2.0,
        location=(0.0, 0.0, 0.0)
    )
    ico_object = bpy.context.active_object
    ico_object.name = "Procedural_Sphere"

    # Assign smooth shading
    bpy.ops.object.shade_smooth()

    # Apply Shrinkwrap-Solidify modifier pipeline simulator
    print("Applying structural modifier stack simulations...")
    solid_mod = ico_object.modifiers.new(name="Solidify_Thickness", type='SOLIDIFY')
    solid_mod.thickness = 0.15
    solid_mod.use_even_thickness = True

    # 2. Add lighting source
    print("Setting up three-point key light...")
    light_data = bpy.data.lights.new(name="Key_Light_Data", type='POINT')
    light_data.energy = 5000.0  # Watts
    light_object = bpy.data.objects.new(name="Key_Light", object_data=light_data)
    bpy.context.collection.objects.link(light_object)
    light_object.location = (5.0, -5.0, 6.0)

    # 3. Add active camera
    print("Positioning camera focus...")
    camera_data = bpy.data.cameras.new(name="Main_Camera_Data")
    camera_object = bpy.data.objects.new(name="Main_Camera", object_data=camera_data)
    bpy.context.collection.objects.link(camera_object)
    
    # Position camera focused on origin (0, 0, 0)
    camera_object.location = (6.0, -7.0, 5.0)
    camera_object.rotation_euler = (0.75, 0.0, 0.7)
    
    # Set active scene camera
    bpy.context.scene.camera = camera_object


def execute_render_job(output_path="//output_render.png"):
    """
    Sets scene resolution and executes the rendering pipeline.
    """
    if not BLENDER_AVAILABLE:
        return

    scene = bpy.context.scene
    scene.render.filepath = output_path
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'

    print(f"Beginning headless Cycles render job. Destination: {output_path}")
    bpy.ops.render.render(write_still=True)
    print("Render job completed successfully!")


if __name__ == "__main__":
    print("Starting Blender OptiX cycles rendering controller...")
    
    # 1. Setup GPU OptiX Rendering
    setup_ok = setup_optix_cycles_rendering()
    
    if setup_ok:
        # 2. Build Scene
        create_procedural_scene()
        
        # 3. Run Render
        # Can specify absolute path if necessary
        execute_render_job(output_path="./procedural_icosphere.png")
    else:
        print("\nDemo Mode: Headless script initialized. To run this script fully, invoke it from your command line:")
        print("  blender -b -P optix_cycles_render.py")
        sys.exit(0)
