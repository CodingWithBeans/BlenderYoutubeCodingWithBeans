import bpy
import random
import math

def createcircle(name, scale):
    bpy.ops.curve.primitive_bezier_circle_add(radius=scale, location=(0, 0, 0))
    curve = bpy.context.object
    curve.name = name
    return curve

def createMarbleTexture():
    if "SharedMarbleTexture" not in bpy.data.textures:
        marble_texture = bpy.data.textures.new(name="SharedMarbleTexture", type='MARBLE')
        marble_texture.marble_type = 'SOFT'
        marble_texture.noise_basis = 'VORONOI_F1'
        marble_texture.turbulence = 10
    else:
        marble_texture = bpy.data.textures["SharedMarbleTexture"]
    return marble_texture

def subdivideCircle(curve, n):
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.mode_set(mode='EDIT')
    for i in range(n):
        bpy.ops.curve.subdivide(number_cuts=1)
    bpy.ops.object.mode_set(mode='OBJECT')
    return curve

def create_icosphere_at_vertex(position, parent):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=(random.uniform(0.1, 1) * 0.1), location=position)
    icosphere = bpy.context.object
    icosphere.name = "Icosphere_Vertex"
    
    # Add a displacement modifier
    displace_mod = icosphere.modifiers.new(name="MarbleDisplace", type='DISPLACE')
    displace_mod.strength = 0.5
    displace_mod.texture = marble_texture
    displace_mod.texture_coords = 'OBJECT'

    # Parent the icosphere to the curve (or the object you want it to follow)
    icosphere.select_set(True)
    parent.select_set(True)
    bpy.context.view_layer.objects.active = parent
    bpy.ops.object.parent_set(type='OBJECT')

    return icosphere

def attach_random_icospheres_to_curve(curve, count, min_radius=5):
    """Attach icospheres to a random subset of vertices on the curve mesh, ensuring they spawn outside the circle."""
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.convert(target='MESH')
    
    mesh = curve.data
    vertex_indices = list(range(len(mesh.vertices)))  # Create a list of all vertex indices

    random_indices = random.sample(vertex_indices, min(count, len(vertex_indices)))
    
    for i in random_indices:
        vertex = mesh.vertices[i]
        
        # Get the distance of the vertex from the origin
        vertex_distance = vertex.co.length
        
        # Ensure the vertex is outside the circle radius (e.g., radius 5)
        if vertex_distance > min_radius:
            # Randomly adjust the distance further away while maintaining the initial random spread
            distance_factor = random.uniform(1.1, 2.0)  # Increase distance by 10% to 200%
            new_position = vertex.co * distance_factor
            create_icosphere_at_vertex(new_position, curve)

# Main script execution
marble_texture = createMarbleTexture()
curve = createcircle("SaturnRing", 5)
subdivideCircle(curve, 2)
attach_random_icospheres_to_curve(curve, count=700, min_radius=5)  # Place 700 icospheres outside the radius of the circle
