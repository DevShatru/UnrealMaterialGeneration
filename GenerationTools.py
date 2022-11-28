# Copyright (C) Shatrujit Aditya Kumar 2022, All Rights Reserved

import Constants
import AssetManipulation

# Checks if the textures directory exists and if it's not empty
def do_textures_exist():
    
    directoryExists = AssetManipulation.AssetLibrary.does_directory_exist( Constants.TEXTURES_LOCATION )

    if directoryExists:
        directoryHasContent = AssetManipulation.AssetLibrary.does_directory_have_assets( Constants.TEXTURES_LOCATION )
        return directoryHasContent
    
    return directoryExists

# Runs through the assets in the textures directory and creates a dictionary mapping a material/instance to it's associated texture maps
def generate_texture_map( isMaterial = True ):

    map = {}
    textureList = AssetManipulation.AssetLibrary.list_assets( Constants.TEXTURES_LOCATION )

    for texture in textureList:

        toLower = texture.lower()
        for suffix in Constants.TEXTURES_SUFFIX:

            if toLower.find(suffix.lower()) != -1:

                simpleName = AssetManipulation.get_name_without_suffix(texture)

                # Compute what appropriately named instance/material should be
                #  remove_unmodified_maps() checks if either of them exists
                instanceName = Constants.MATERIAL_INSTANCE_PREFIX + simpleName
                materialName = Constants.MATERIAL_PREFIX + simpleName

                prefixedName = instanceName
                
                if isMaterial:
                    prefixedName = materialName

                if not prefixedName in map:
                    map[ prefixedName ] = { 
                        Constants.MAPS_KEY: {},
                        Constants.NAMES_KEY: [ instanceName, materialName ]
                    }
                
                map[ prefixedName ][ Constants.MAPS_KEY ][ suffix ] = texture
    
    return map

# Checks for each asset in the texture map if:
#   i) A corresponding material/instancce already exists
#   ii) It's modification date is more recent than the modification dates of all of it's texture maps
# Removes instance from the map if both (i) and (ii) are true
def remove_unmodified_maps( assetTexMap ):

    assetList = AssetManipulation.AssetLibrary.list_assets( Constants.MATERIALS_LOCATION )

    for asset in assetList:

        strippedName = AssetManipulation.strip_path_and_extension( asset )

        for mappedAsset in list( assetTexMap ):
            possibleNames = assetTexMap[ mappedAsset ][ Constants.NAMES_KEY ]
            if strippedName in possibleNames:
                instanceModTime = AssetManipulation.get_modified_time( asset )

                if mappedAsset == asset:
                    assetTexMap[ mappedAsset ][ Constants.PATHS_KEY ] = asset

                texturePaths = assetTexMap[ mappedAsset ][ Constants.MAPS_KEY ].values()
                shouldRegenerate = False

                for textures in texturePaths:

                    textureModTime = AssetManipulation.get_modified_time( textures )

                    if textureModTime > instanceModTime:

                        shouldRegenerate = True
                        break
                
                if not shouldRegenerate:
                    assetTexMap.pop( mappedAsset )

  
# Iterates through the filtered texture map and:
#   i) Deletes existing/outdated materials/instances
#   ii) Creates materials/instances, sets up nodes, and recompiles and saves the created asset
def generate_materials_from_map( matTexMap ):

    for mat in matTexMap:
        if Constants.PATHS_KEY in matTexMap[ mat ]:
            AssetManipulation.AssetLibrary.delete_asset( matTexMap[ mat ][ Constants.PATHS_KEY ])

        generatedMat = AssetManipulation.generate_material_asset( mat, Constants.MATERIALS_LOCATION )

        generate_nodes( matTexMap[ mat ][ Constants.MAPS_KEY ], generatedMat)

        AssetManipulation.MaterialLibrary.recompile_material( generatedMat )
        AssetManipulation.save_asset( generatedMat )
        

# Iterates through the texture maps for a specific material,
# creates and connects materials expressions if they have a recognized suffix
def generate_nodes( textureMap, material ):
    
    numNodes = len( textureMap )
    iter = 0 # Tracking index for calculating position and spacing of nodes
    for texType in textureMap:
        node = AssetManipulation.generate_node( material, iter, numNodes)

        node.texture = AssetManipulation.AssetLibrary.load_asset( textureMap[ texType ] )
        texTypeLower = texType.lower()
        if texTypeLower == Constants.BASE_SUFFIX.lower():
            AssetManipulation.set_node_property( node, "RGB", Constants.PropertyNode.BaseColor )

        elif texTypeLower == Constants.NORMAL_SUFFIX.lower():
            node.sampler_type = AssetManipulation.get_sampler_from_map( Constants.Sampler.Normal )
            AssetManipulation.set_node_property( node, "RGB", Constants.PropertyNode.Normal )
        
        elif texTypeLower == Constants.PACKED_SUFFIX.lower():
            node.sampler_type = AssetManipulation.get_sampler_from_map( Constants.Sampler.LinearColor )
            AssetManipulation.set_node_property( node, "R", Constants.PropertyNode.Emissive )
            AssetManipulation.set_node_property( node, "G", Constants.PropertyNode.Roughness )
            AssetManipulation.set_node_property( node, "B", Constants.PropertyNode.AO )
            AssetManipulation.set_node_property( node, "A", Constants.PropertyNode.Metallic )

        elif texTypeLower == Constants.HEIGHT_SUFFIX.lower():
            node.sampler_type = AssetManipulation.get_sampler_from_map( Constants.Sampler.LinearColor )
            # Material Property for WPO isn't exposed to Python API

        elif texTypeLower == Constants.ROUGH_SUFFIX.lower():
            node.sampler_type = AssetManipulation.get_sampler_from_map( Constants.Sampler.LinearColor )
            AssetManipulation.set_node_property( node, "RGB", Constants.PropertyNode.Roughness )
        
        elif texTypeLower == Constants.AO_SUFFIX.lower():
            node.sampler_type = AssetManipulation.get_sampler_from_map( Constants.Sampler.LinearColor )
            AssetManipulation.set_node_property( node, "RGB", Constants.PropertyNode.AO )

        iter += 1
  
# Iterates through the filtered instance-texture map and:
#   i) Deletes existing/outdated materials instances
#   ii) Creates material instances, sets up nodes, and recompiles and saves the created asset
def generate_instances_from_map( instTexMap ):
    shader = AssetManipulation.AssetLibrary.load_asset( Constants.SHADER )

    for instance in instTexMap:
        if Constants.PATHS_KEY in instTexMap[instance]:
            AssetManipulation.AssetLibrary.delete_asset( instTexMap[ instance ][ Constants.PATHS_KEY ] )

        generatedInstance = AssetManipulation.generate_material_asset( instance, Constants.MATERIALS_LOCATION, False )
        AssetManipulation.save_asset( generatedInstance )
        
        AssetManipulation.MaterialLibrary.set_material_instance_parent( generatedInstance, shader )
        set_instance_params( instTexMap[ instance ][ Constants.MAPS_KEY ], generatedInstance )

        AssetManipulation.save_asset( generatedInstance )

# Iterates through the texture maps for a specific instance,
# sets texture params if they have a recognized suffix
def set_instance_params( textureMap, instance ):
    
    for texType in textureMap:
        param_name = ""
        texTypeLower = texType.lower()
        
        if texTypeLower == Constants.BASE_SUFFIX.lower():
            param_name = Constants.SUFFIX_PARAM_MAP[ Constants.BASE_SUFFIX ]

        elif texTypeLower == Constants.NORMAL_SUFFIX.lower():
            param_name = Constants.SUFFIX_PARAM_MAP[ Constants.NORMAL_SUFFIX ]
        
        elif texTypeLower == Constants.PACKED_SUFFIX.lower():
            param_name = Constants.SUFFIX_PARAM_MAP[ Constants.PACKED_SUFFIX ]
        
        AssetManipulation.MaterialLibrary.set_material_instance_texture_parameter_value( instance, param_name, AssetManipulation.AssetLibrary.load_asset( textureMap[ texType ] ))