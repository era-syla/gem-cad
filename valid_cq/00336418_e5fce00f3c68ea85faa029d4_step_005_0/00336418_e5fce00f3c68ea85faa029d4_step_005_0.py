import cadquery as cq

# -- Parametric Definitions --
# Overall dimensions of the box
length = 150.0
width = 50.0
height = 50.0

# Construction parameters
wall_thickness = 3.0
num_compartments = 3

# -- Calculations --
# Calculate the length of a single compartment
# Formula: (Total Length - External Walls - Internal Dividers) / Count
# Number of internal dividers is (num_compartments - 1)
total_divider_thickness = (num_compartments - 1) * wall_thickness
total_external_wall_thickness = 2 * wall_thickness
available_internal_length = length - total_external_wall_thickness - total_divider_thickness

compartment_length = available_internal_length / num_compartments
compartment_width = width - (2 * wall_thickness)

# Distance between the centers of adjacent compartments
# (Half compartment + Wall + Half compartment) = Compartment Length + Wall Thickness
center_spacing_x = compartment_length + wall_thickness

# Depth of the cut (Total height - Floor thickness)
cut_depth = height - wall_thickness

# -- 3D Modeling --
result = (
    cq.Workplane("XY")
    # 1. Create the main outer block
    .box(length, width, height)
    
    # 2. Select the top face to start cutting
    .faces(">Z")
    .workplane()
    
    # 3. Create a linear array of points for the compartment centers
    .rarray(
        xSpacing=center_spacing_x, 
        ySpacing=1,               # Ignored since yCount is 1
        xCount=num_compartments, 
        yCount=1, 
        center=True
    )
    
    # 4. Sketch the rectangular profile for the compartments
    .rect(compartment_length, compartment_width)
    
    # 5. Perform the cut downwards, leaving the floor
    .cutBlind(-cut_depth)
)