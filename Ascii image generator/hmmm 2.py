import bpy

# CONFIGURATION
image_path = r"C:\Users\matty\Pictures\Screenshots\Screenshot 2025-02-10 205256.png"  # Change to your image path
cube_size = 0.1  # Size of each cube
resize_width = 100  # Number of cubes along the width (adjust for detail)

def clearscreen():
    # Delete all existing objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    return 0

def setupimage(image_path, resize_width):
    # Load the image
    bpy.data.images.load(image_path, check_existing=True)
    image = bpy.data.images[image_path.split("\\")[-1]]

    # Calculate resize dimensions
    aspect_ratio = image.size[1] / image.size[0]
    new_height = int(resize_width * aspect_ratio)

    # Get pixel data
    pixels = list(image.pixels)
    pixel_data = [(pixels[i], pixels[i+1], pixels[i+2]) for i in range(0, len(pixels), 4)]

    # Create a single material using the object color
    mat = bpy.data.materials.new(name="CubeMaterial")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    object_info = mat.node_tree.nodes.new("ShaderNodeObjectInfo")
    mat.node_tree.links.new(object_info.outputs["Color"], bsdf.inputs["Base Color"])
    return mat

# Create a base cube with the bevel modifier and material
def createCube(mat):
    bpy.ops.mesh.primitive_cube_add(size=cube_size, location=(0, 0, 0))
    base_cube = bpy.context.object
    bpy.ops.object.modifier_add(type='BEVEL')
    bevel_modifier = base_cube.modifiers["Bevel"]
    bevel_modifier.width = 0.01
    bevel_modifier.segments = 4
    base_cube.data.materials.append(mat)
    return base_cube

def generateCubes(base_cube):
    # Generate the cubes with unique colors
    for x in range(resize_width):
        for y in range(new_height):
            pixel_x = int((x / resize_width) * image.size[0])
            pixel_y = int((y / new_height) * image.size[1])
            pixel_index = min((pixel_y * image.size[0]) + pixel_x, len(pixel_data) - 1)  # Clamp index
            r, g, b = pixel_data[pixel_index]

            # Create a linked duplicate
            cube = base_cube.copy()
            cube.location = (x * cube_size, y * cube_size, 0)
            bpy.context.collection.objects.link(cube)
            
            # Set the cube's object color
            cube.color = (r, g, b, 1)

    # Remove the original base cube
    bpy.data.objects.remove(base_cube)


def main():
    #clears screen obs
    clearscreen()
    mat = setupimage(image_path, resize_width)
    #create base cube var and sets it equal to return of createCube func
    base_cube = createCube(mat)
    #generates a base cube we can use to then create linked duplicates ohh and deletesbase cube
    generateCubes(base_cube)