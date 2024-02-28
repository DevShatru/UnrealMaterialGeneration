# Copyright (C) Shatrujit Aditya Kumar 2024. All Rights Reserved. 

SCALE = 16 # Size of a grid square in the material graph

# The remaining constants are in grid-scale, i.e, need to be multiplied by Scale before being set to a Material Expression
HORIZONTAL_OFFSET = -26 # Offset of every expression from the property node
NODE_HEIGHT = 14 # Height of the Texture Sample expression
VERTICAL_HEIGHT = 35 # Vertical height of the property node
SPACING_BETWEEN = 1 # Space between each generate Texture Sample expression

# Calculate the Y-index based on the index of the current expression, and total number of expressions
def get_y_pos( index, size ):

    center = ( VERTICAL_HEIGHT - NODE_HEIGHT ) / 2
    middleIndex = ( size - 1 ) / 2
    nodeOffset = SPACING_BETWEEN + NODE_HEIGHT
    
    if size % 2 == 0:
        center = ( VERTICAL_HEIGHT + SPACING_BETWEEN ) / 2
        middleIndex = size / 2
        
    return SCALE * ( center - ( middleIndex - index ) * nodeOffset)

# Return the constant X-offset
def get_x_pos():
    return HORIZONTAL_OFFSET * SCALE