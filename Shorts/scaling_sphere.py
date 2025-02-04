import bpy

def clearscene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def createSphere():
    bpy.ops.mesh.primitive_uv_sphere_add(radius= 1)
    sphere = bpy.context.object
    return sphere

def drivers(sphere):
    driverx = sphere.driver_add("scale", 0)
    driverx.driver.expression = "1 + cos(frame * 0.1)"

    drivery = sphere.driver_add("scale", 1)
    drivery.driver.expression = "1 + cos(frame * 0.1)"

    driverz = sphere.driver_add("scale", 2)
    driverz.driver.expression = "1 + cos(frame * 0.1)"

def main():
    clearscene()
    sphere = createSphere()
    drivers(sphere)

main()