import bpy  # Import Blender's Python API

def createsphere(radius, xloc, yloc, zloc, name):
    """Creates a UV sphere at the specified location and returns it."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(xloc, yloc, zloc))  # Add a sphere
    sphere = bpy.context.object  # Get the newly created sphere
    sphere.name = name  # Assign a name to the sphere
    return sphere  # Return the sphere object

def clearscreen():
    """Deletes all objects in the scene to start fresh."""
    bpy.ops.object.select_all(action='SELECT')  # Select all objects
    bpy.ops.object.delete()  # Delete selected objects

def main():
    """Main function to clear the scene and create a sphere."""
    clearscreen()  # Remove all objects in the scene
    sphere = createsphere(1, 0, 0, 0, "test")  # Create a sphere at (0,0,0) with name "test"

main()  # Run the script
