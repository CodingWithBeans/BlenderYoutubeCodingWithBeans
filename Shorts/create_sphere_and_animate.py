import bpy  # Import Blender's Python API

def createsphere(radius, xloc, yloc, zloc, name):
    """Creates a UV sphere at the specified location and returns it."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(xloc, yloc, zloc))  # Add a sphere
    sphere = bpy.context.object  # Get the newly created sphere
    sphere.name = name  # Assign a name to the sphere
    return sphere  # Return the sphere object

def createcurve(radius, xloc, yloc, zloc, name):
    """Creates a Bezier circle at the specified location and returns it."""
    bpy.ops.curve.primitive_bezier_circle_add(radius=radius, location=(xloc, yloc, zloc))  # Add a circular curve
    circle = bpy.context.object  # Get the newly created circle
    circle.name = name  # Assign a name to the circle
    circle.data.use_path = True  # Enable path usage for animation
    return circle  # Return the circle object

def clearscreen():
    """Deletes all objects in the scene to start fresh."""
    bpy.ops.object.select_all(action='SELECT')  # Select all objects
    bpy.ops.object.delete()  # Delete selected objects

def animatingSphereToCircle(sphere, circle):
    """Applies a Follow Path constraint to the sphere to make it follow the circular path."""

    constraint = sphere.constraints.new(type='FOLLOW_PATH')  # Create a Follow Path constraint
    constraint.target = circle  # Set the target path to the Bezier circle
    constraint.use_curve_follow = True  # Enable rotation to follow the path

    bpy.context.view_layer.objects.active = sphere  # Set the sphere as the active object
    sphere.select_set(True)  # Select the sphere

    bpy.ops.object.constraint_add(type='FOLLOW_PATH')  # Add Follow Path constraint via Blender operator
    bpy.ops.constraint.followpath_path_animate(constraint=constraint.name, owner='OBJECT')  # Animate the constraint

def main():
    """Main function to clear the scene, create objects, and animate."""

    clearscreen()  # Remove all objects in the scene

    sphere = createsphere(1, 0, 0, 0, "testSphere")  # Create a sphere at (0,0,0)
    circle = createcurve(1, 0, 0, 0, "testCircle")  # Create a circular path at (0,0,0)

    animatingSphereToCircle(sphere, circle)  # Make the sphere follow the circular path

main()  # Run the script
