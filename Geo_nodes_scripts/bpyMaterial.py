import bpy
import sys

script_dir = r"C:\Users\matty\Desktop\BlenderAPI\Geo_nodes_scripts"

if script_dir not in sys.path:
    sys.path.append(script_dir)

import helperfunction

print(helperfunction)

helperfunction.clearScene()

def createMetal(name):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True

    nodes = material.node_tree.nodes
    links = material.node_tree.links

    helperfunction.clearNodes(nodes)
    output_node = helperfunction.newNode(nodes, "ShaderNodeOutputMaterial", (400, 0)) 
    principled_bsdf = helperfunction.newNode(nodes, "ShaderNodeBsdfPrincipled", (0, 0))
    colour_ramp = helperfunction.newNode(nodes, "ShaderNodeValToRGB", (0,0))
    noise_texture = helperfunction.newNode(nodes, "ShaderNodeTexNoise", (0, 0))
    tex_coord = helperfunction.newNode(nodes, "ShaderNodeTexCoord", (0, 0))
    mapping = helperfunction.newNode(nodes, "ShaderNodeMapping", (0, 0))

    principled_bsdf.inputs["Metallic"].default_value = 1
    principled_bsdf.inputs["Base Color"].default_value = (0.321, 0.321, 0.321, 1.0)
    noise_texture.inputs["Scale"].default_value = 1
    noise_texture.inputs["Detail"].default_value = 12
    noise_texture.inputs["Roughness"].default_value = 0.917
    colour_ramp.color_ramp.elements[0].color = (0.060, 0.060, 0.060, 1.0)
    colour_ramp.color_ramp.elements[0].position = 0.203
    colour_ramp.color_ramp.elements[1].position = 0.691

    links.new(colour_ramp.outputs["Color"], principled_bsdf.inputs["Roughness"])
    links.new(principled_bsdf.outputs["BSDF"], output_node.inputs["Surface"])
    links.new(noise_texture.outputs["Fac"], colour_ramp.inputs["Fac"])
    links.new(mapping.outputs["Vector"], noise_texture.inputs["Vector"])
    links.new(tex_coord.outputs["Object"], mapping.inputs["Vector"])

    return material


def createMetalOrEmission(name):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    

    helperfunction.clearNodes(nodes)
    output_node = helperfunction.newNode(nodes, "ShaderNodeOutputMaterial", (400, 0)) 
    principled_bsdf = helperfunction.newNode(nodes, "ShaderNodeBsdfPrincipled", (0, 0))
    colour_ramp1 = helperfunction.newNode(nodes, "ShaderNodeValToRGB", (0,0))
    colour_ramp2 = helperfunction.newNode(nodes, "ShaderNodeValToRGB", (0,0))
    noise_texture1 = helperfunction.newNode(nodes, "ShaderNodeTexNoise", (0, 0))
    noise_texture2 = helperfunction.newNode(nodes, "ShaderNodeTexNoise", (0, 0))
    tex_coord = helperfunction.newNode(nodes, "ShaderNodeTexCoord", (0, 0))
    mapping1 = helperfunction.newNode(nodes, "ShaderNodeMapping", (0, 0))
    mapping2 = helperfunction.newNode(nodes, "ShaderNodeMapping", (0, 0))
    mix_shader = helperfunction.newNode(nodes, "ShaderNodeMixShader", (0, 0))
    obj_info = helperfunction.newNode(nodes, "ShaderNodeObjectInfo", (0, 0))
    emission = helperfunction.newNode(nodes, "ShaderNodeEmission", (0, 0))

    principled_bsdf.inputs["Metallic"].default_value = 1
    principled_bsdf.inputs["Base Color"].default_value = (0.321, 0.321, 0.321, 1.0)
    noise_texture1.inputs["Scale"].default_value = 1
    noise_texture1.inputs["Detail"].default_value = 12
    noise_texture1.inputs["Roughness"].default_value = 0.917
    colour_ramp1.color_ramp.elements[0].color = (0.060, 0.060, 0.060, 1.0)
    colour_ramp1.color_ramp.elements[0].position = 0.203
    colour_ramp1.color_ramp.elements[1].position = 0.691

    noise_texture2.inputs["Scale"].default_value = 5.1
    noise_texture2.inputs["Detail"].default_value = 2.3
    noise_texture2.inputs["Roughness"].default_value = 0.533
    colour_ramp2.color_ramp.interpolation = 'CONSTANT'
    colour_ramp2.color_ramp.elements[1].position = 0.430

    emission.inputs["Color"].default_value = (0.5, 0, 1, 1)
    emission.inputs["Strength"].default_value = 24

    links.new(colour_ramp1.outputs["Color"], principled_bsdf.inputs["Roughness"])
    links.new(principled_bsdf.outputs["BSDF"], mix_shader.inputs[1])
    links.new(mix_shader.outputs["Shader"], output_node.inputs["Surface"])
    links.new(noise_texture1.outputs["Fac"], colour_ramp1.inputs["Fac"])
    links.new(mapping1.outputs["Vector"], noise_texture1.inputs["Vector"])
    links.new(tex_coord.outputs["Object"], mapping1.inputs["Vector"])
    links.new(noise_texture2.outputs["Fac"], colour_ramp2.inputs["Fac"])
    links.new(mapping2.outputs["Vector"], noise_texture2.inputs["Vector"])
    links.new(colour_ramp2.outputs["Color"], mix_shader.inputs["Fac"])
    links.new(obj_info.outputs["Random"], mapping2.inputs["Vector"])
    links.new(emission.outputs["Emission"], mix_shader.inputs[2])
    
    return material