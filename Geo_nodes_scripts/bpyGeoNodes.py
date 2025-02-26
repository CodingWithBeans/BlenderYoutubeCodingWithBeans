import bpy
import sys

script_dir = r"C:\Users\matty\Desktop\BlenderAPI\Geo_nodes_scripts"

if script_dir not in sys.path:
    sys.path.append(script_dir)


import helperfunction

print(helperfunction)

helperfunction.clearScene()

def metalWiresBallsOnPoints(nodeTree, material, material2):
    
    group_input = nodeTree.nodes.new(type='NodeGroupInput')
    group_output = nodeTree.nodes.new(type='NodeGroupOutput')
    triangulate_node = nodeTree.nodes.new(type="GeometryNodeTriangulate")
    dual_mesh = nodeTree.nodes.new(type="GeometryNodeDualMesh")
    separate_geometry = nodeTree.nodes.new(type="GeometryNodeSeparateGeometry")
    mesh_to_curve = nodeTree.nodes.new(type="GeometryNodeMeshToCurve")
    curve_to_mesh = nodeTree.nodes.new(type="GeometryNodeCurveToMesh")
    set_material_1 = nodeTree.nodes.new(type="GeometryNodeSetMaterial")
    set_material_2 = nodeTree.nodes.new(type="GeometryNodeSetMaterial")
    join_geometry = nodeTree.nodes.new(type="GeometryNodeJoinGeometry")
    instance_on_points = nodeTree.nodes.new(type="GeometryNodeInstanceOnPoints")
    curve_circle = nodeTree.nodes.new(type="GeometryNodeCurvePrimitiveCircle")
    ico_sphere = nodeTree.nodes.new(type="GeometryNodeMeshIcoSphere")
    random_value_1 = nodeTree.nodes.new(type="FunctionNodeRandomValue")
    random_value_2 = nodeTree.nodes.new(type="FunctionNodeRandomValue")
    set_shade_smooth = nodeTree.nodes.new(type="GeometryNodeSetShadeSmooth")
    
    group_input.location = (-200, 0)
    group_output.location = (200, 0)

    separate_geometry.domain = 'FACE'
    curve_circle.inputs["Radius"].default_value = 0.01
    ico_sphere.inputs["Radius"].default_value = 0.05
    ico_sphere.inputs["Subdivisions"].default_value = 4
    random_value_1.data_type = 'BOOLEAN'
    random_value_1.location = (0, 50)
    set_material_1.inputs["Material"].default_value = material
    set_material_2.inputs["Material"].default_value = material2

    nodeTree.interface.new_socket(name="Geometry", in_out='INPUT', socket_type="NodeSocketGeometry")
    nodeTree.interface.new_socket(name="Geometry", in_out='OUTPUT', socket_type="NodeSocketGeometry")

    inlist = [
        triangulate_node.outputs[0],
        dual_mesh.outputs[0],
        random_value_1.outputs["Value"],
        separate_geometry.outputs["Selection"],
        mesh_to_curve.outputs["Curve"],
        curve_circle.outputs["Curve"],
        curve_to_mesh.outputs["Mesh"],
        set_material_1.outputs["Geometry"],
        join_geometry.outputs["Geometry"],
        separate_geometry.outputs["Selection"],
        ico_sphere.outputs["Mesh"],
        random_value_2.outputs["Value"],
        instance_on_points.outputs["Instances"],
        set_shade_smooth.outputs["Geometry"],
        set_material_2.outputs["Geometry"],
        group_input.outputs[0],
    ]
    outlist= [
        dual_mesh.inputs[0],
        separate_geometry.inputs["Geometry"],
        separate_geometry.inputs["Selection"],
        mesh_to_curve.inputs["Mesh"],
        curve_to_mesh.inputs["Curve"],
        curve_to_mesh.inputs["Profile Curve"],
        set_material_1.inputs["Geometry"],
        join_geometry.inputs["Geometry"],
        group_output.inputs[0],
        instance_on_points.inputs["Points"],
        instance_on_points.inputs["Instance"],
        instance_on_points.inputs["Scale"],
        set_shade_smooth.inputs["Geometry"],
        set_material_2.inputs["Geometry"],
        join_geometry.inputs["Geometry"],
        triangulate_node.inputs["Mesh"],
    ]
    endp1 = (len(inlist) + 1)
    print(f"endp1 - >{endp1}")
    for i in range(1, endp1):
        print(f"i ->{i}")
        inputN = inlist[(i - 1)]
        outputN = outlist[(i - 1)]
        print(f"input N outputN: {inputN}, {outputN}")
        helperfunction.linkNodes(inputN, outputN, nodeTree)