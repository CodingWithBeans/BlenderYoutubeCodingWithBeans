import bpy  # Import Blender's Python API

# Function to create a new node in a material's node tree
def newNode(nodes, type, location=(0, 0)):
    node = nodes.new(type=type)  # Create a new node of the specified type
    node.location = location  # Set the node's location in the node editor
    return node  # Return the created node

# Function to create a UV sphere with a given radius, location, and name
def createSphere(radius, location, name):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)  # Add a UV sphere to the scene
    sphere = bpy.context.object  # Get the active object (the newly created sphere)
    sphere.name = name  # Set the object's name
    bpy.ops.object.shade_smooth()  # Apply smooth shading to the sphere
    return sphere  # Return the sphere object

# Function to delete all objects in the scene
def clearScreen():
    bpy.ops.object.select_all(action='SELECT')  # Select all objects in the scene
    bpy.ops.object.delete()  # Delete all selected objects

# Function to create a material using an image texture
def createEarthMaterial(name, imagePath):
    material = bpy.data.materials.new(name=name)  # Create a new material with the given name
    material.use_nodes = True  # Enable node-based shading for the material
    
    nodes = material.node_tree.nodes  # Get the material's node tree
    links = material.node_tree.links  # Get the node tree's links

    # Remove all existing nodes from the material
    for node in nodes:
        nodes.remove(node)

    # Create necessary shader nodes
    output_node = newNode(nodes, "ShaderNodeOutputMaterial", (400, 0))  # Create the Material Output node
    principled_bsdf = newNode(nodes, "ShaderNodeBsdfPrincipled", (0, 0))  # Create the Principled BSDF shader
    texureImage = newNode(nodes, "ShaderNodeTexImage", (-300, 0))  # Create an Image Texture node

    texureImage.image = bpy.data.images.load(imagePath)  # Load the image into the texture node

    # Connect the texture's colour output to the Base Color input of the Principled BSDF shader
    links.new(texureImage.outputs["Color"], principled_bsdf.inputs["Base Color"])
    # Connect the texture's alpha output to the Alpha input of the Principled BSDF shader
    links.new(texureImage.outputs["Alpha"], principled_bsdf.inputs["Alpha"])
    # Connect the Principled BSDF shader output to the Material Output node
    links.new(principled_bsdf.outputs["BSDF"], output_node.inputs["Surface"])

    return material  # Return the created material

# Main function to clear the scene, create an Earth sphere, and apply the material
def main():
    clearScreen()  # Clear the scene by deleting all objects
    earth = createSphere(radius=1, location=(0, 0, 0), name="Earth")  # Create a sphere named "Earth"
    earthMaterial = createEarthMaterial("earthMaterial", imagePath=r"")  # Create a material (image path needed)
    earth.data.materials.append(earthMaterial)  # Assign the material to the Earth sphere

main()  # Call the main function