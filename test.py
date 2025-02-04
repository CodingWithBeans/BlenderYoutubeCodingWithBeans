# create a torus
# set to ext int
# set in = to ring int set ex = to ring out

# select all verticies > 0 and delete on z axis
# set z scale to 0
# # clear links
# # add sub inst cube
# create primitive torus

bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), abso_minor_rad=7, abso_major_rad= 40)