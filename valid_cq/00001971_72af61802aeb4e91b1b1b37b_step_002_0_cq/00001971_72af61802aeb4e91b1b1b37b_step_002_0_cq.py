import cadquery as cq

# Parametric dimensions
length = 60.0       # Total length of the block
width = 50.0        # Total width/depth of the block
height = 30.0       # Total height of the block
wall_thickness = 10.0 # Thickness of the side walls and top
hole_diameter = 12.0 # Diameter of the through holes

# Derived dimensions
channel_width = length - (2 * wall_thickness)
channel_height = height - wall_thickness

# Create the main block
# Start with a solid box
base_block = cq.Workplane("XY").box(length, width, height)

# Create the channel cut (from the bottom)
# We select the bottom face ('<Z'), draw a rectangle, and cut it through the width
channel_cut = (
    base_block
    .faces("<Z")
    .workplane()
    .rect(channel_width, width)
    .cutBlind(-channel_height)
)

# Create the holes on the side face
# We select the front face (assuming 'front' corresponds to the side with holes in the view)
# or the appropriate side face based on orientation.
# Let's target the face that is perpendicular to the Y-axis (width direction)
# or the X-axis (length direction).
# Based on the image, the holes go through the "length" sides (the legs of the U).
# So we select one of the side faces (e.g., >X or <X) or front/back (>Y or <Y).
# Let's assume the length is along X, height along Z, width along Y.
# The holes are on the Face along the X-Z plane (Front view in standard orientation usually).

result = (
    channel_cut
    .faces(">Y") # Select the front face
    .workplane()
    # The holes need to be positioned. 
    # Center of left hole: x = -length/2 + wall_thickness/2
    # Center of right hole: x = length/2 - wall_thickness/2
    # Height of holes: likely centered in the "leg" height or centered overall?
    # Visually, they look centered in the vertical face of the leg.
    .pushPoints([
        (-length/2 + wall_thickness/2, -channel_height/2), # Left hole position relative to face center
        (length/2 - wall_thickness/2, -channel_height/2)   # Right hole position relative to face center
    ])
    .hole(hole_diameter)
)

# Alternative approach for clearer hole positioning if the previous one is ambiguous:
# Let's refine the hole positioning logic.
# The origin of the initial box is center (0,0,0).
# The legs are at X = +/- (length/2 - wall_thickness/2).
# The holes go through the Y-axis.
# Let's rebuild purely based on coordinates to be safe and robust.

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    # Cut the channel from the bottom (-Z)
    .faces("<Z").workplane()
    .rect(channel_width, width)
    .cutBlind(-channel_height)
    # Create holes
    # We want holes going through the Y axis (width), located in the legs.
    # The legs are located at X-coordinates.
    .faces(">Y").workplane()
    .pushPoints([
        (-(length - wall_thickness)/2, -height/2 + (height-wall_thickness)/2), 
        ((length - wall_thickness)/2, -height/2 + (height-wall_thickness)/2)
    ])
    # Correction: Visually the holes look like they are in the center of the vertical leg section.
    # The leg is 'channel_height' tall.
    # The Z-position relative to center (0,0,0) is: 
    # Bottom of block is -height/2. Top of leg is -height/2 + channel_height.
    # Center of leg vertically is -height/2 + channel_height/2.
    .hole(hole_diameter)
)