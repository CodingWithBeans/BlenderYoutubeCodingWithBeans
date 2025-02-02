import bpy

# Function to create an axis object (a cube) with a given name, location, and scale
def create_axis(name, location, scale):
    bpy.ops.mesh.primitive_cube_add(location=location)  # Add a cube at the specified location
    axis = bpy.context.object  # Get the created object (cube)
    axis.name = name  # Set the name of the object
    axis.scale = scale  # Set the scale of the object
    return axis  # Return the created object

# Function to create a UV sphere object with a given name, location, and scale
def create_uv_sphere(name, location, scale):
    bpy.ops.mesh.primitive_uv_sphere_add(location=location, radius=scale)  # Add a UV sphere at the specified location
    sphere = bpy.context.object  # Get the created object (sphere)
    sphere.name = name  # Set the name of the object
    return sphere  # Return the created object

# Function to add a sine-based driver to control an object's location over time
def add_sine_driver(obj):
    # Add a driver to control the Z-axis location of the object
    z_driver = obj.driver_add("location", 2)
    z_driver.driver.expression = "sin(frame * 0.1) * 2"  # Sine wave driver, oscillates up and down
    # Add a driver to control the X-axis location of the object
    x_driver = obj.driver_add("location", 0)
    x_driver.driver.expression = "frame / 10"  # Linear movement along the X-axis over time

# Main function to create the scene objects and set them up
def main():
    # Create the X and Z axes (as fake axis representations)
    x_axis = create_axis("Fake_X_Axis", (10, 0, 0), (15, 0.05, 0.05))
    z_axis = create_axis("Fake_Z_Axis", (0, 0, 0), (0.05, 0.05, 2))
    
    # Create a small UV sphere (point) that will move based on drivers
    point = create_uv_sphere("Point", (0, 0, 1), 0.1)
    
    # Add drivers to the point for animated movement
    add_sine_driver(point)

# Call the main function to execute the script
main()
