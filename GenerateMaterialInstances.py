# Copyright (C) Shatrujit Aditya Kumar 2022, All Rights Reserved

import GenerationTools

def main():

    # Early return if the textures directory doesn't exist or is empty
    if not GenerationTools.do_textures_exist():
        return

    instanceTextureMap = GenerationTools.generate_texture_map( False )
    
    GenerationTools.remove_unmodified_maps( instanceTextureMap )

    GenerationTools.generate_instances_from_map( instanceTextureMap )

main()