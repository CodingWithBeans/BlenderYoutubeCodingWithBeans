import bpy
import sys

script_dir = r"C:\Users\matty\Desktop\BlenderAPI\Geo_nodes_scripts"

if script_dir not in sys.path:
    sys.path.append(script_dir)

import helperfunction
import bpyGeoNodes
import bpyMaterial

print(helperfunction)

helperfunction.clearScene()

material = bpyMaterial.createMetal("pleasework")
material2 = bpyMaterial.createMetalOrEmission("test")

for i in range(1, 11):
    primitive = helperfunction.createPrimitive(i, ((i * 2), 0, 0))
    rls = i % 3
    driver = helperfunction.addDrivers(rls, rls, "frame / 10", primitive)
    primitive.data.materials.append(material)
    geoMod, nodeTree = helperfunction.CreateGeoNodes(primitive, "TestNodes")
    bpyGeoNodes.metalWiresBallsOnPoints(nodeTree, material, material2)