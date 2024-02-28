# Copyright (C) Shatrujit Aditya Kumar 2024. All Rights Reserved.

import unreal
import os.path

import Constants
import PositionCalculator

# Maps Constants.PropertyNode enum to unreal.MaterialProperty enum
PropertyMap = {
    Constants.PropertyNode.BaseColor: unreal.MaterialProperty.MP_BASE_COLOR,
    Constants.PropertyNode.Normal: unreal.MaterialProperty.MP_NORMAL,
    Constants.PropertyNode.AO: unreal.MaterialProperty.MP_AMBIENT_OCCLUSION,
    Constants.PropertyNode.Roughness: unreal.MaterialProperty.MP_ROUGHNESS,
    Constants.PropertyNode.Metallic: unreal.MaterialProperty.MP_METALLIC,
    Constants.PropertyNode.Emissive: unreal.MaterialProperty.MP_EMISSIVE_COLOR
}

# Maps Constants.Sampler enum to unreal.MaterialSamplerType enum
SamplerMap = {
    Constants.Sampler.Normal: unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL,
    Constants.Sampler.LinearColor: unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR,
    Constants.Sampler.LinearGrayscale: unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_GRAYSCALE,
    Constants.Sampler.Alpha: unreal.MaterialSamplerType.SAMPLERTYPE_ALPHA,
}

# Aliases for unreal classes
AssetLibrary = unreal.EditorAssetLibrary
SystemLibrary = unreal.SystemLibrary
MaterialLibrary = unreal.MaterialEditingLibrary
AssetTools = unreal.AssetToolsHelpers.get_asset_tools()

# Generates a material/material instance called `name`, with file path `location`
def generate_material_asset( name, location, isMaterial = True):
    create_directory( location )
    if isMaterial:
        return AssetTools.create_asset( name, location, unreal.Material, unreal.MaterialFactoryNew() )
    
    return AssetTools.create_asset( name, location, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew() )

# Creates directory if it doesn't exist
def create_directory( path ):
    if AssetLibrary.does_directory_exist( path ):
        return
        
    AssetLibrary.make_directory( path )

# Generates a material expression/node
def generate_node( material, iterator, size ):
    return MaterialLibrary.create_material_expression(  material, 
                                                        unreal.MaterialExpressionTextureSample, 
                                                        node_pos_x=PositionCalculator.get_x_pos(), 
                                                        node_pos_y=PositionCalculator.get_y_pos( iterator, size ))

# Sets a material property from a node output
def set_node_property( node, output, property ):
    MaterialLibrary.connect_material_property( node, output, PropertyMap[ property ])

# Returns an unreal.MaterialSamplerType for corresponding Constants.Sampler
def get_sampler_from_map( key ):
    return SamplerMap[ key ]

# Saves a uasset file
def save_asset( assetObj ):
    assetPath = AssetLibrary.get_path_name_for_loaded_asset( assetObj )
    AssetLibrary.save_asset( assetPath )

# Gets simple name from texture maps without suffix, used to generate the appropriate name for the material
def get_name_without_suffix( filename ):

    removedPath = strip_path_and_extension( filename )
    splitAtUnderscore = removedPath.split( "_" )
    splitAtUnderscore.pop()

    removedSuffix = "_".join( splitAtUnderscore )
    
    return removedSuffix

# Helper to strip file path and extension from a filename
def strip_path_and_extension( filename ):

    removedExtension = filename.split( "." )[ 0 ]
    splitAtSlash = removedExtension.split( "/" )
    removedPath = splitAtSlash[ len(splitAtSlash) - 1 ]

    return removedPath

# Converts Asset Library path to absolute path
def get_absolute_path( libraryPath ):
    asset = AssetLibrary.load_asset( libraryPath )
    systemPath = SystemLibrary.get_system_path( asset )
    return systemPath

# Uses os.path module to get the modification time of a file, requires absolute path
def get_modified_time( libraryPath ):
    return os.path.getmtime( get_absolute_path( libraryPath ))