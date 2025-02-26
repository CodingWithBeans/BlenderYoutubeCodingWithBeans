import bpy
import random
import math
#Before you run check the max value in setFrames(): set this to your intended maximum frame (lower values will cause inner planets to move very fast)
#sun is 30000 times smaller than other planets, all orbits are synced so neptunes lasts 1 cycle, this means pluto does not complete a single orbit.
#sun has a bary center # pluto texture https://planet-texture-maps.fandom.com/wiki/Pluto




##### sun as emission node, saturns rings.
planets = {
    #name : SMA (10^6), diameter(Km), day(hours), year(earth day)
    "Sun": [0.8, 1392700, 840, 4331.865],
    "Mercury": [57.9, 4879, 4222.6, 88.0],
    "Venus": [108.2, 12104, 2802.0, 224.7],
    "Earth": [149.6, 12756, 24.0, 365.2],
    "Mars": [228.0, 6792, 24.7, 687.0],
    "Jupiter": [778.5, 142984, 9.9, 4331],
    "Saturn": [1432.0, 120536, 10.7	, 10747],
    "Uranus": [2867.0, 51118, 17.2, 30589],
    "Neptune": [4515.0, 49528, 16.1, 59800],
    "Pluto": [5906.4, 2376, 153.3, 90560],
}
saturn_ring_data = [7.5, 4.0, 150] # radius width, segments

###################################################################           SCENE SET UP  ###########################################################################################################
def setFrames():
    max=10000
    #sets the first frame to 1
    bpy.data.scenes[0].frame_start = 1
    #sets the last frame to be the value max defaults to 10000
    bpy.data.scenes[0].frame_end = max
    return max

def clearScene():
    #selects all objects in scene and deletes
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def setEndView():
    #bpy.context.space_data.shading.type = 'RENDERED'

    for a in bpy.context.screen.areas:
        if a.type == 'VIEW_3D':
            for s in a.spaces:
                if s.type == 'VIEW_3D':
                    s.clip_end = 10000

def setUpScene():
    #clears the scene and sets the max frames to 1000
    clearScene()
    setEndView()
    maxFrame = setFrames()
    return maxFrame



################################################################################## CREATE OBJECTS/ DRIVERS    ####################################################################################################

def createUVSphere(name, location, scale):
    #creates a uv sphere gives it the location (x,y,z) and the radius is set to the scale of the planet 
    bpy.ops.mesh.primitive_uv_sphere_add(location=location, radius=scale)
    #select the last object created (the sphere)
    sphere = bpy.context.object
    #we name the sphere
    sphere.name = name
    bpy.ops.object.shade_smooth()
    return sphere

def createcircle(name, scale):
    bpy.ops.curve.primitive_bezier_circle_add(radius=scale, location=(0, 0, 0))
    curve = bpy.context.object
    curve.name = name
    return curve

def subdivideCircle(curve, n):
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.mode_set(mode='EDIT')
    for i in range(n):
        bpy.ops.curve.subdivide(number_cuts=1)
    bpy.ops.object.mode_set(mode='OBJECT')
    return curve

def create_icosphere_at_vertex(position, parent, marble_texture):
    bpy.ops.mesh.primitive_ico_sphere_add(radius=((random.uniform(0.1, 1)) * 2), location=position)
    icosphere = bpy.context.object
    icosphere.name = "Icosphere_Vertex"
    multiplier = random.uniform(-20, 20)
    icosphere.location.z += multiplier
    zDriverloc = icosphere.driver_add("location", 2)
    zDriverloc.driver.expression = f"{multiplier} * sin(frame / 100)"
    
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

def attach_random_icospheres_to_curve(curve, marble_texture, count, min_radius=5):
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
            create_icosphere_at_vertex(new_position, curve, marble_texture)

def newNode(nodes, type, location=(0, 0)):
    node = nodes.new(type=type)  # Create a new node of the specified type
    node.location = location  # Set the node's location in the node editor
    return node  # Return the created node


def createMaterialplanets(name, imagePath):
    
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

def createMaterialSaturnsRings(name):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True

    nodes = material.node_tree.nodes  
    links = material.node_tree.links  

    for node in nodes:
        nodes.remove(node)

    output_node = newNode(nodes, "ShaderNodeOutputMaterial", (400, 0))
    principled_bsdf = newNode(nodes, "ShaderNodeBsdfPrincipled", (0, 0))
    transparent_bsdf = newNode(nodes, "ShaderNodeBsdfTransparent", (-300, -200))  # Transparent BSDF shader
    mix_shader = newNode(nodes, "ShaderNodeMixShader", (200, 0))  # Mix Shader node

    links.new(principled_bsdf.outputs["BSDF"], mix_shader.inputs[1])
    links.new(mix_shader.outputs["Shader"], output_node.inputs["Surface"])
    links.new(transparent_bsdf.outputs["BSDF"], mix_shader.inputs[2])

    principled_bsdf.inputs["Roughness"].default_value = 0.032
    principled_bsdf.inputs[18].default_value = 0.6
    principled_bsdf.inputs["Alpha"].default_value = 0.191

    return material

def createMarbleTexture():
    if "SharedMarbleTexture" not in bpy.data.textures:
        marble_texture = bpy.data.textures.new(name="SharedMarbleTexture", type='MARBLE')
        marble_texture.marble_type = 'SOFT'
        marble_texture.noise_basis = 'VORONOI_F1'
        marble_texture.turbulence = 10
    else:
        marble_texture = bpy.data.textures["SharedMarbleTexture"]
    return marble_texture

def addDriversLocation(obj, D, year, maxFrame):
    neptuneOrbitLim = maxFrame
    neptuneDays = 59800
    ratio = neptuneOrbitLim * (year / neptuneDays)
    #called a variable xdriver set a new location driver on channel 0 (x channel)
    xDriver= obj.driver_add("location", 0)
    xDriver.driver.expression = f"{D} * cos((2 * pi * frame) / {ratio})"
    #called a variable xydriver set a new location driver on channel 1 (y channel)
    yDriver= obj.driver_add("location", 1)
    yDriver.driver.expression = f"{D} * sin((2 * pi * frame) / {ratio})"


def addDriversRotation(obj, hour):
    #create a variable driver set it to rotation and z channel (2)
    day = hour * 24
    zDriver = obj.driver_add("rotation_euler", 2)
    zDriver.driver.expression = f"frame / {day}"

def checklastcharacter(object_name):
    return int(object_name[-1])

def createSaturnRing(ring_material, saturn_ring_data):

    #grab the data and assign from list
    radius = saturn_ring_data[0]  # Approximate Saturn ring inner radius
    width = saturn_ring_data[1]    # Width of the ring
    num_instances = int(saturn_ring_data[2])  # Number of small torus objects

    #making collection
    collection_name = "SaturnsRings"
    collection = bpy.data.collections.get(collection_name)

    if not collection:
        collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(collection)

    #making rings
    for i in range(num_instances):
        driverz = random.uniform(0, 2 * math.pi)
        anglex = random.uniform(-0.02, 0.02)
        distance = random.uniform(radius - width / 2, radius + width / 2) #  this randomnesss stops us naming the rings in sequential order
        z_bump = random.uniform(-0.1, 0.1)

        bpy.ops.mesh.primitive_torus_add(major_radius=distance, minor_radius = 0.02, major_segments=36, minor_segments=8)

        ring = bpy.context.object
        ring.data.materials.append(ring_material)

        s = 12
        location = 1432
        ring.scale = (s, s, s)
        ring.location = (location, 0, z_bump)
        ring.name = f"RingSegment_{i}"

        # Randomly rotate and tilt slightly
        ring.rotation_euler[0] = anglex

        # Add a driver for the Z rotation (ring spin)
        z_driver = ring.driver_add("rotation_euler", 2) 
        name = ring.name
        namelastchara = checklastcharacter(name)
        if namelastchara % 2 == 0:
            driverxpression = f"({driverz} + (frame / 100)) % (2 * pi)"
        else:
            driverxpression = f"(({driverz} + (frame / 100)) % (2 * pi) * -1)"

        # Set driver expression (this will make the ring spin)
        z_driver.driver.expression = driverxpression  # Randomized rotation per ring

        ring.data.name = f"RingSegmentMesh_{i}"


        #unlinks from main collection and links to targetted satrurns rings collection
        for col in ring.users_collection:
            col.objects.unlink(ring)
        
        collection.objects.link(ring)

        #selects saturn and parents the rings 
        saturn = bpy.data.objects.get("Saturn")
        saturn.select_set(True)
        bpy.context.view_layer.objects.active = saturn
        bpy.ops.object.parent_set(type='OBJECT')

def createAsteroidBelt():
    marble_texture = createMarbleTexture()
    curve = createcircle("AsteroidBelt", 300)
    zDriver = curve.driver_add("rotation_euler", 2)
    zDriver.driver.expression = f"frame / 10000"
    subdivideCircle(curve, 2)
    attach_random_icospheres_to_curve(curve, marble_texture, count=700, min_radius=5)


def createPlanets(maxFrame, planets):
    for name, (D, radius, hour, year) in planets.items():
        imagePath = f"C:\\Users\\matty\\Desktop\\BlenderAPI\\Solar_System\\Textures\\{name}.jpg"
        planetMaterial= createMaterialplanets(name, imagePath)
        
        scale_factor = 30000 if name == "Sun" else 2000
        
        planet= createUVSphere(name, ((D / 10), 0, 0), (radius / scale_factor))
        addDriversLocation(planet, D, year, maxFrame)
        addDriversRotation(planet, hour)
        planet.data.materials.append(planetMaterial)
        


def main():
    #sets up scene
    maxFrame =setUpScene()
    #creates planets inc sun
    createPlanets(maxFrame, planets=planets)
    ringmatname = "Ring Material"
    ring_material = createMaterialSaturnsRings(ringmatname)
    createSaturnRing(ring_material, saturn_ring_data=saturn_ring_data)
    createAsteroidBelt()
    
main()