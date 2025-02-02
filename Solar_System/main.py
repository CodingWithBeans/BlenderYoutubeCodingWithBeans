#create a solar system with blender using the API bpy
#Y = KCOS(T) t = frames
#x = ksin(t) t = frames
import bpy

#list of all the planets with some data (name, AU distance, radius, day length, year length)
#1000 frames
#clear the scene
#create UV spheres
#add drivers (location -> rotation)

#             MERCURY 	 VENUS 	 EARTH 	MOON 	MARS 	JUPITER  SATURN     URANUS 	 NEPTUNE 	 PLUTO
# DIAMETER (km) 4879	12,104	12,756	3475	6792	142,984	 120,536	51,118	 49,528	     2376 RADIUS
# day length  4222.6	2802.0	24.0	708.7	24.7	9.9	      10.7	    17.2	  16.1	    153.3  DAY LENGTH (HOURS)
#D from s      57.9	   108.2	149.6	0.384*	228.0	778.5	 1432.0	    2867.0	  4515.0	5906.4   Distance from Sun (106 km) (will need to convert this somehow)
# year         88.0	  224.7	   365.2	27.3*	687.0	4331	10,747	    30,589	  59,800	90,560   YEAR IN DAYS




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

################################################################################## CREATE OBJECTS     ####################################################################################################



def main():
    setUpScene()