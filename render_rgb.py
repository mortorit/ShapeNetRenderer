import argparse, sys, os, math
import bpy

def main(views, obj, output_folder, scale, remove_doubles, edge_split, color_depth, format, resolution, engine):
    # Set up rendering
    scene = bpy.context.scene
    render = scene.render

    render.engine = engine
    render.image_settings.color_mode = 'RGBA'
    render.image_settings.color_depth = color_depth
    render.image_settings.file_format = format
    render.resolution_x = resolution
    render.resolution_y = resolution
    render.resolution_percentage = 100
    render.film_transparent = True

    if bpy.context.active_object is not None:
        bpy.context.active_object.select_set(True)
    bpy.ops.object.delete()

    # Import textured mesh
    bpy.ops.wm.obj_import(filepath=obj)  # Make sure this matches your Blender version's import function

    obj = bpy.context.selected_objects[0]  # Assumes the imported object is selected
    bpy.context.view_layer.objects.active = obj

    # Apply transformations
    if scale != 1:
        bpy.ops.transform.resize(value=(scale, scale, scale))
        bpy.ops.object.transform_apply(scale=True)
    if remove_doubles:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT')
    if edge_split:
        bpy.ops.object.modifier_add(type='EDGE_SPLIT')
        bpy.context.object.modifiers["EdgeSplit"].split_angle = 1.32645
        bpy.ops.object.modifier_apply(modifier="EdgeSplit")


    # Configure lighting and camera
    # Make light just directional, disable shadows
    light = bpy.data.lights.get('Light')
    if light:
        light.type = 'SUN'
        light.use_shadow = False
        light.specular_factor = 1.0
        light.energy = 10.0

    # Add another light source
    bpy.ops.object.light_add(type='SUN')
    light2 = bpy.data.lights['Sun']
    light2.use_shadow = False
    light2.specular_factor = 1.0
    light2.energy = 0.015
    bpy.data.objects['Sun'].rotation_euler = (math.radians(180), 0, 0)


    # Place camera
    cam = scene.objects['Camera']
    cam.location = (0, 1.5, 0.6)
    cam.data.lens = 35
    cam.data.sensor_width = 32

    cam_constraint = cam.constraints.new(type='TRACK_TO')
    cam_constraint.track_axis = 'TRACK_NEGATIVE_Z'
    cam_constraint.up_axis = 'UP_Y'

    cam_empty = bpy.data.objects.new("Empty", None)
    cam_empty.location = (0, 0, 0)
    cam.parent = cam_empty

    context = bpy.context
    scene.collection.objects.link(cam_empty)
    context.view_layer.objects.active = cam_empty
    cam_constraint.target = cam_empty

    stepsize = 360.0 / views
    rotation_mode = 'XYZ'

    # Render views
    stepsize = 360.0 / views
    for i in range(0, views):
        print("Rendering view {}...".format(i + 1))
        render.filepath = os.path.join(output_folder, f"render_{i:03d}")
        bpy.ops.render.render(write_still=True)
        cam_empty.rotation_euler[2] += math.radians(stepsize)


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Renders given obj file by rotating a camera around it.')
    parser.add_argument('--views', type=int, default=30, help='number of views to be rendered')
    parser.add_argument('--obj', type=str, help='Path to the obj file to be rendered.')
    parser.add_argument('--output_folder', type=str, default='/tmp', help='The path the output will be dumped to.')
    parser.add_argument('--scale', type=float, default=1,
                        help='Scaling factor applied to model. Depends on size of mesh.')
    parser.add_argument('--remove_doubles', type=bool, default=True,
                        help='Remove double vertices to improve mesh quality.')
    parser.add_argument('--edge_split', type=bool, default=True, help='Adds edge split filter.')
    parser.add_argument('--color_depth', type=str, default='8',
                        help='Number of bit per channel used for output. Either 8 or 16.')
    parser.add_argument('--format', type=str, default='PNG', help='Format of files generated. Either PNG or OPEN_EXR')
    parser.add_argument('--resolution', type=int, default=600, help='Resolution of the images.')
    parser.add_argument('--engine', type=str, default='BLENDER_EEVEE',
                        help='Blender internal engine for rendering. E.g., CYCLES, BLENDER_EEVEE')

    argv = sys.argv[sys.argv.index("--") + 1:]  # Extract script-specific arguments
    args = parser.parse_args(argv)

    # Call the main function with the provided arguments
    main(**vars(args))