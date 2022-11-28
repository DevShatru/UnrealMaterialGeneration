### **Asset Generation Scripts**
Author: Shatrujit Aditya Kumar (shatrujit95@gmail.com)
Last Updated: 4th October 2022
----------

A set of python scripts used to generate Materials and/or Material Instances for an Unreal Engine project.

The scripts check a directory of textures for files matching a predetermined naming convention and use those textures to create new assets. If the corresponding asset already exists, the scripts check the modification date of the asset against the modification date of each relevant texture and recreate the asset if the textures have been more recently modified.

#### **Installation**
--------
The scripts in this package need to be inside your project's Content folder, ideally in a "Python" directory with any other scripts you may be using.

#### **How to use**
--------
 - Populate the `Content/Textures` directory with textures you want to create materials/instances out of (Make sure they are saved after import)

 - Ensure that the imported textures follow the correct naming convention:
    - All textures related to the same material/instance must start with the same string ( eg: "Grenade" )
    - Textures must end with one of the predetermined suffixes ( eg: "_BaseColor", "_Normal" )
    - The exhaustive list of accepted suffixes can be found in `Content/Python/Constants.py`

 - Execute the relevant Python script
    - From the Menu Bar, click "File" -> "Execute Python Script..."
    - Navigate to the project root -> "Content" -> "Python"
    - To create materials, select "GenerateMaterials.py"
    - To create material instances using the uber baked shader, select "GenerateMaterialInstances.py"
    - The corresponding material/instance generated by the script will be placed in `Content/Materials`
    
#### **Known Issues**
--------
 - Of the currently accepted suffixes for materials, "Height" should create an expression mapped to the "World Position Offset" property. However, this property is not exposed to the Python API. So while the script still creates the node, it does not connect it to the relevant property.
 
 - The script currently does not check or account for prefixes (such as "T_") on the texture assets as our project does not use them. If required, this functionality will be added at a later date.
