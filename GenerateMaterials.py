# Copyright (C) Shatrujit Aditya Kumar 2022, All Rights Reserved

import GenerationTools

def main():

    # Early return if the textures directory doesn't exist or is empty
    if not GenerationTools.do_textures_exist():
        return

    materialTextureMap = GenerationTools.generate_texture_map()
    
    GenerationTools.remove_unmodified_maps( materialTextureMap )

    GenerationTools.generate_materials_from_map( materialTextureMap )

main()