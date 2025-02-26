import bpy

#a collection of helper functions to be called within other scripts to make geonodes.

def createPrimitive(type, location):
    """
    Explination: creates a given primitive based on a list of meshes and returns said mesh
    
    Keywords:
        1) type (int) -> index value of list of types
        2) location (list floats allowed) [(xloc, yloc, zloc)] -> final frame

    Type Mapping:
        1 -> circle
        2 -> cone
        3 -> cube
        4 -> Cylinder
        5 -> Grid
        6 -> Ico Sphere
        7 -> monkey
        8 -> plane
        9 -> torus
        10 -> UV sphere
    """

    if type == 1:
        primitive = bpy.ops.mesh.primitive_circle_add(location= location)
    elif type == 2:
        primitive = bpy.ops.mesh.primitive_cone_add(location= location)
    elif type == 3:
        primitive = bpy.ops.mesh.primitive_cube_add(location= location)
    elif type == 4:
        primitive = bpy.ops.mesh.primitive_cylinder_add(location= location)
    elif type == 5:
        primitive = bpy.ops.mesh.primitive_grid_add(location= location)
    elif type == 6:
        primitive = bpy.ops.mesh.primitive_ico_sphere_add(location= location)
    elif type == 7:
        primitive = bpy.ops.mesh.primitive_monkey_add(location= location)
    elif type == 8:
        primitive = bpy.ops.mesh.primitive_plane_add(location= location)
    elif type == 9:
        primitive = bpy.ops.mesh.primitive_torus_add(location= location)
    elif type == 10:
        primitive = bpy.ops.mesh.primitive_uv_sphere_add(location= location)
    else:
        print("invalid type")

    primitive = bpy.context.object

    return primitive

def setFrame(start, end, scene = 0):
    """
    Explination: sets the start and end frame of a given scene

    Keywords:
        1) start (int) -> beginning frame
        2) end (int) -> final frame
        3) scene (int) -> 0 based index scene list defaults to 0
    """
    bpy.data.scenes[scene].frame_start = start
    bpy.data.scenes[scene].frame_end = end
    print(f"Start Frame set to {start}, End frame set to {end}, in scene {scene}")

def clearScene():
    """selects all objects in scene and deletes"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def addDrivers(rls, channel, expression, obj):
    """
    Explination: creates a driver based on a given channels and returns the driver
    
    Keywords:
        1) rls (roation location scale) (int) -> index value channels rotation, location, scale
        2) channel (x y z) (int) -> index value for respective channel
        3) expression string -> a f string
        4) obj -> object passed to add said driver to

    rls Mapping:
        0 -> rotation euler
        1 -> location
        2 -> scale

    channel values:
        0 -> x
        1 -> y
        2 -> z
    
    """
    rlsList = ["rotation_euler", "location", "scale"]

    if not isinstance(obj, bpy.types.Object):
        print("Error: Provided obj is not a valid Blender object.")
        return None

    Driver = obj.driver_add(rlsList[rls], channel)
    Driver.driver.expression = f"{expression}"

    return Driver

def newNode(nodes, type, location=(0, 0)):
    """
    Explination: creates a new node in a given tree
        
    Keywords:
        1) nodes (current node tree) (variable) -> nodes = material.node_tree.nodes
        2) type (node name) (string) -> "ShaderNodeBsdfPrincipled"
        3) location (list), int -> x, y locations
    """
    node = nodes.new(type=type)
    node.location = location

    return node

def clearNodes(nodes):
    """clears existing nodes"""
    for node in nodes:
        nodes.remove(node)

    return nodes

def CreateGeoNodes(obj, nodeName):
    """    
    Explination: creates a new geonodes node tree
        
    Keywords:
        1) obj (object) (variable) -> assigned outside the function
        2) nodeName (string) -> node set up name
        
    """
    
    geoMod = obj.modifiers.new(name="GeometryNodes", type='NODES')
    nodeName += "Tree"

    if not geoMod.node_group:
        nodeTree = bpy.data.node_groups.new(name="GeoNodesTree", type='GeometryNodeTree')
        geoMod.node_group = nodeTree
    
    return geoMod, nodeTree

def linkNodes(input, output, nodeTree):
    try:
        nodeTree.links.new(input, output)
    except Exception as e:
        raise RuntimeError(f"failed to link nodes input ->{input} output-> {output}")

