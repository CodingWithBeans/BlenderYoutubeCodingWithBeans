import bpy
import os

# CONFIGURATION
image_path = r"C:\Users\matty\Pictures\Screenshots\Screenshot 2025-02-10 205256.png"  # Change this path
cube_size = 0.1  # Size of each cube
resize_width = 100  # Number of cubes along the width (adjust for detail)

def clearscreen():
    """Delete all existing objects in the scene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def setup_image(image_path, resize_width):
    """Load the image and extract pixel data."""
    try:
        image = bpy.data.images.load(image_path)
    except RuntimeError:
        print(f"Error: Could not load image {image_path}")
        return None, None, None

    # Compute aspect ratio
    aspect_ratio = image.size[1] / image.size[0]
    new_height = int(resize_width * aspect_ratio)

    # Extract pixel data (RGB only, ignoring alpha)
    pixels = list(image.pixels)
    pixel_data = [(pixels[i], pixels[i+1], pixels[i+2]) for i in range(0, len(pixels), 4)]
    
    return new_height, pixel_data, image

def create_material():
    """Creates a material with object color support."""
    mat = bpy.data.materials.new(name="CubeMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    
    if bsdf:
        object_info = mat.node_tree.nodes.new("ShaderNodeObjectInfo")
        mat.node_tree.links.new(object_info.outputs["Color"], bsdf.inputs["Base Color"])
    
    return mat

def create_base_cube(mat):
    """Creates a base cube with a bevel modifier and applies material."""
    bpy.ops.mesh.primitive_cube_add(size=cube_size, location=(0, 0, 0))
    base_cube = bpy.context.object
    bpy.ops.object.modifier_add(type='BEVEL')
    
    base_cube.modifiers["Bevel"].width = 0.01
    base_cube.modifiers["Bevel"].segments = 4
    base_cube.data.materials.append(mat)
    
    return base_cube

def generate_cubes(base_cube, new_height, pixel_data, image):
    """Creates cubes based on pixel data and assigns colors."""
    for y in range(resize_width):
        for x in range(new_height):
            pixel_x = int((x / resize_width) * image.size[0])                    
            pixel_y = int((y / new_height) * image.size[1])                        
            pixel_index = min((pixel_y * image.size[0]) + pixel_x, len(pixel_data) - 1)  # Clamp index
            r, g, b = pixel_data[pixel_index]

            # Create an instance (linked duplicate for performance)
            cube = base_cube.copy()
            cube.data = base_cube.data  # Share mesh data
            bpy.context.collection.objects.link(cube)

            # Position the cube
            cube.location = (x * cube_size, y * cube_size, 0)

            # Set object color
            cube.color = (r, g, b, 1)

    # Remove the original base cube (optional)
    bpy.data.objects.remove(base_cube)

def main():
    clearscreen()
    new_height, pixel_data, image = setup_image(image_path, resize_width)

    if not pixel_data:
        print("No pixel data available. Exiting...")
        return

    mat = create_material()
    base_cube = create_base_cube(mat)
    generate_cubes(base_cube, new_height, pixel_data, image)

main()
