#create a solar system with blender using the API bpy
#Y = KCOS(T) t = frames
#x = ksin(t) t = frames
import bpy

#list of all the planets with some data (name, AU distance, radius, day length, year length) [potential scale = /10]
#1000 frames
#clear the scene
#create UV spheres
#add drivers (location -> rotation)



planets = {
    #name : SMA (10^6), diameter(Km), day(hours), year(earth day)

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
def setFrames(max=1000):
    #sets the first frame to 1
    bpy.data.scenes[0].frame_start = 1
    #sets the last frame to be the value max defaults to 1000
    bpy.data.scenes[0].frame_end = max

def clearScene():
    #selects all objects in scene and deletes
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def setUpScene():
    #clears the scene and sets the max frames to 1000
    clearScene()
    setFrames()

################################################################################## CREATE OBJECTS/ DRIVERS    ####################################################################################################

def createUVSphere(name, location, scale):
    #creates a uv sphere gives it the location (x,y,z) and the radius is set to the scale of the planet 
    bpy.ops.mesh.primitive_uv_sphere_add(location=location, radius=scale)
    #select the last object created (the sphere)
    sphere = bpy.context.object
    #we name the sphere
    sphere.name = name
    return sphere

def addDriversLocation(obj, D, year):
    maxYear = (59800 / 365.2)
    #called a variable xdriver set a new location driver on channel 0 (x channel)
    xDriver= obj.driver_add("location", 0)
    xDriver.driver.expression = f"{D} * cos(frame / ({maxYear} / ({year} / 50)))"
    #called a variable xydriver set a new location driver on channel 1 (y channel)
    yDriver= obj.driver_add("location", 1)
    yDriver.driver.expression = f"{D} * sin(frame / ({maxYear} / ({year} / 50)))"


def addDriversRotation(obj, hour):
    #create a variable driver set it to rotation and z channel (2)
    day = hour * 24
    zDriver = obj.driver_add("rotation_euler", 2)
    zDriver.driver.expression = f"frame / {day}"

def createPlanets(planets):
    for name, (D, radius, hour, year) in planets.items():
        planet= createUVSphere(name, ((D / 10), 0, 0), (radius / 2000))
        addDriversLocation(planet, D, year)
        addDriversRotation(planet, hour)

def main():
    setUpScene()
    createPlanets(planets=planets)


main()


# for name, (D, radius, day, year) in planets.items():
#     print(f"""
#           Planet: {name}
#           distance : {D}
#           diameter: {radius}
#           day = {day}
#         year = {year}
#           """)
v