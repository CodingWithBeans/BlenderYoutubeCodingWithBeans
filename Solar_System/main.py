import bpy
import os
#Before you run check the max value in setFrames(): set this to your intended maximum frame (lower values will cause inner planets to move very fast)
#sun is 30000 times smaller than other planets, all orbits are synced so neptunes lasts 1 cycle, this means pluto does not complete a single orbit.
#sun has a bary center # pluto texture https://planet-texture-maps.fandom.com/wiki/Pluto

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
    return sphere

def newNode(nodes, type, location=(0, 0)):
    node = nodes.new(type=type)  # Create a new node of the specified type
    node.location = location  # Set the node's location in the node editor
    return node  # Return the created node


def createMaterial(name, imagePath):
    
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

def createPlanets(maxFrame, planets):
    for name, (D, radius, hour, year) in planets.items():
        imagePath = f"C:\\Users\\matty\\Desktop\\BlenderAPI\\Solar_System\\Textures\\{name}.jpg"
        planetMaterial= createMaterial(name, imagePath)
        
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
    
main()