# Copyright (C) Shatrujit Aditya Kumar 2024. All Rights Reserved.

import GenerationTools

def generate_material_instances():

    # Early return if the textures directory doesn't exist or is empty
    if not GenerationTools.do_textures_exist():
        return

    instanceTextureMap = GenerationTools.generate_texture_map( False )
    
    GenerationTools.remove_unmodified_maps( instanceTextureMap )

    GenerationTools.generate_instances_from_map( instanceTextureMap )
