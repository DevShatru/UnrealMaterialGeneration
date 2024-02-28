# Copyright (C) Shatrujit Aditya Kumar 2024. All Rights Reserved.
from enum import Enum

# Asset library texture, material directories & shader path
TEXTURES_LOCATION = "/Game/Textures"
MATERIALS_LOCATION = "/Game/Materials"
SHADER = "/Game/Shaders/M_UberBaked"

# Prefix to add to the created material/instance
MATERIAL_INSTANCE_PREFIX = "MI_"
MATERIAL_PREFIX = "M_"

# Accepted suffixes on textures maps, plus an array to easily iterate through them
BASE_SUFFIX = "_D"
NORMAL_SUFFIX = "_N"
PACKED_SUFFIX = "Packed"
HEIGHT_SUFFIX = "Height"
ROUGH_SUFFIX = "_R"
AO_SUFFIX = "_AO"

TEXTURES_SUFFIX = [ BASE_SUFFIX, NORMAL_SUFFIX, PACKED_SUFFIX, HEIGHT_SUFFIX, ROUGH_SUFFIX, AO_SUFFIX ]

# Map parameter names to the appropriate suffix
BASE_PARAM = "[ BASE ] BaseColor | Opacity (BC1)"
NORMAL_PARAM = "[ BASE ] NormalDX (BC5)"
PACKED_PARAM = "[ BASE ] Emissive | Rough | AO | Metal (BC1)"

SUFFIX_PARAM_MAP = {
    BASE_SUFFIX: BASE_PARAM,
    NORMAL_SUFFIX: NORMAL_PARAM,
    PACKED_SUFFIX: PACKED_PARAM
}

# Keys for material-texture mapping dictionary
MAPS_KEY = "maps"
PATHS_KEY = "path"
NAMES_KEY = "asset_names"

# Enums to map to the corresponding unreal enums for property node and sampler type
# Done to limit the number of unreal imports so all unreal communication can happen in AssetManipulation
class PropertyNode(Enum):
    BaseColor = 0,
    Normal = 1,
    AO = 2,
    Roughness = 3,
    Metallic = 4,
    Emissive = 5

class Sampler(Enum):
    Normal = 0,
    LinearColor = 1,
    LinearGrayscale = 2,
    Alpha = 3,