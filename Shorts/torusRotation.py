import bpy
import math

# Function to create a torus object at a specified location with a given name
def create_torus(location, name):
    bpy.ops.mesh.primitive_torus_add(location=location)  # Add a torus at the specified location
    torus = bpy.context.object  # Get the created torus object
    torus.name = name  # Set the name of the torus object
    bpy.ops.object.shade_smooth()  # Apply smooth shading to the torus
    return torus  # Return the created torus object

# Function to delete all objects in the scene
def clear_screen():
    bpy.ops.object.select_all(action='SELECT')  # Select all objects in the scene
    bpy.ops.object.delete()  # Delete all selected objects

# Function to rotate an object from the first frame to the last frame
def rotation(obj, first=1, last=250, PImult=2):
    PImult = PImult * math.pi  # Calculate the total rotation (multiplied by pi)
    obj.rotation_euler = (0, 0, 0)  # Set the initial rotation to (0, 0, 0)
    obj.keyframe_insert(data_path="rotation_euler", frame=first)  # Insert a keyframe at the first frame
    
    obj.rotation_euler.x = PImult  # Set the final rotation on the X-axis
    obj.keyframe_insert(data_path="rotation_euler", frame=last)  # Insert a keyframe at the last frame

# Main function to execute the scene setup and animations
def main():
    clear_screen()  # Clear the scene of all objects
    torus1 = create_torus(location=(0, 0, 0), name="Rotation1")  # Create the first torus at the origin
    rotation(torus1, 1, 250, 2)  # Rotate the first torus from frame 1 to 250 with a 2x pi rotation
    torus2 = create_torus(location=(4, 0, 0), name="Rotation2")  # Create the second torus at (4, 0, 0)
    rotation(torus2, 1, 250, 4)  # Rotate the second torus from frame 1 to 250 with a 4x pi rotation

# Call the main function to run the script
main()