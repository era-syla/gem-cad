import cadquery as cq

# Parametric dimensions
thickness = 5.0
height = 10.0
center_offset = 15.0  # Vertical offset of the central "bridge"
center_width = 20.0   # Width of the central "bridge" section
side_length = 25.0    # Length of each side wing
hole_diameter = 4.0
hole_offset = 12.5    # Distance from the end of the wing to the hole center

# Calculate derived dimensions for drawing
# We will draw the profile on the XZ plane and extrude along Y (or depth)
total_width = (side_length * 2) + center_width

# Create the sketch points for the profile
# Starting from bottom-left corner and going clockwise
# Let's center the part on the origin (X=0)

# Coordinates calculation:
# The shape is symmetric. Let's define the path.
x_center_half = center_width / 2.0
x_total_half = x_center_half + side_length

pts = [
    (-x_total_half, 0),                 # Bottom-left outer corner
    (-x_center_half, 0),                # Bottom-left inner corner (start of rise)
    (-x_center_half, center_offset),    # Top-left inner corner
    (x_center_half, center_offset),     # Top-right inner corner
    (x_center_half, 0),                 # Bottom-right inner corner (end of rise)
    (x_total_half, 0),                  # Bottom-right outer corner
    (x_total_half, thickness),          # Top-right outer corner
    (x_center_half + thickness, thickness), # Top-right outer (on flat) - wait, this approach assumes constant thickness
]

# Better approach: Draw the centerline or the bottom line, offset it, or just draw the polygon explicitly.
# Let's draw the polygon explicitly to ensure uniform thickness visually.
# Actually, the image shows vertical walls for the bridge, so simple offsetting might create angled corners if not careful.
# Looking at the image, the vertical sections are vertical.

# Let's define the profile as a wire on the Front plane (XZ)
# Points for the "bottom" path
p1 = (-x_total_half, 0)
p2 = (-x_center_half, 0)
p3 = (-x_center_half, center_offset)
p4 = (x_center_half, center_offset)
p5 = (x_center_half, 0)
p6 = (x_total_half, 0)

# Points for the "top" path (offset by thickness)
p7 = (x_total_half, thickness)
p8 = (x_center_half + thickness, thickness) # Wait, if vertical wall is thickness wide?
# Let's assume the wall thickness is constant everywhere.
# If the wall thickness is 'thickness', then:
# The vertical wall goes from x = -x_center_half to x = -x_center_half + thickness ? No, that changes the inner width.
# Usually, dimensions are interior or exterior. Let's assume the given dimensions define the *shape* and thickness is added "outwards" or "upwards".

# Let's try a simpler constructive geometry approach:
# 1. Create a base flat bar.
# 2. Create the U-shape in the middle.
# 3. Union them? No.

# Let's go back to the wire profile. It's the most robust.
# Let's assume the thickness applies to the vertical direction for horizontal segments 
# and horizontal direction for vertical segments. This is a common sheet metal or machined shape.

# Bottom-left point
bl_start = (-x_total_half, 0)
# Go right to start of bridge
bl_bridge_start = (-x_center_half, 0)
# Go up to bridge height
tl_bridge_corner = (-x_center_half, center_offset)
# Go right across bridge
tr_bridge_corner = (x_center_half, center_offset)
# Go down
br_bridge_corner = (x_center_half, 0)
# Go right to end
br_end = (x_total_half, 0)

# Now the return path (upper surface), offsetting by thickness
tr_end = (x_total_half, thickness)
# Top-right inner corner (above br_bridge_corner)
tr_inner = (x_center_half + thickness, thickness) # This makes the vertical leg thicker? 
# No, let's keep thickness constant.
# If vertical leg is thickness T, outer X is x_center_half + T? No usually bridge width is internal.
# Let's assume the image shows a bent strap.
# If it's a bent strap, CadQuery's thicken is perfect, or a sweep.

# Path for sweep approach:
path = (
    cq.Workplane("XZ")
    .moveTo(-x_total_half, thickness/2)
    .lineTo(-x_center_half, thickness/2)
    .lineTo(-x_center_half, center_offset + thickness/2)
    .lineTo(x_center_half, center_offset + thickness/2)
    .lineTo(x_center_half, thickness/2)
    .lineTo(x_total_half, thickness/2)
)

# However, the corners in the image are sharp (machined), not rounded (bent).
# So I will construct the solid by extruding a specific profile.

pts_profile = [
    # Bottom path
    (-x_total_half, 0),
    (-x_center_half, 0),
    (-x_center_half, center_offset),
    (x_center_half, center_offset),
    (x_center_half, 0),
    (x_total_half, 0),
    
    # Top path (going backwards)
    (x_total_half, thickness),
    (x_center_half + thickness, thickness), # Assuming vertical wall thickness same as horizontal
    (x_center_half + thickness, center_offset + thickness),
    (-x_center_half - thickness, center_offset + thickness),
    (-x_center_half - thickness, thickness),
    (-x_total_half, thickness)
]
# The above logic makes the bridge wider and higher on the outside. 
# Looking at the image, the side wings align with the bottom of the central U.
# The central U goes *up*.
# The thickness seems uniform.

# Revised Profile Points
inner_u_width = center_width
wing_len = side_length
h = height  # This is actually the depth of the extrusion
thk = thickness
u_height = center_offset

result = (
    cq.Workplane("XY")
    # Draw the profile on the XY plane
    .moveTo(-inner_u_width/2 - thk - wing_len, 0)
    .lineTo(-inner_u_width/2 - thk, 0)
    .lineTo(-inner_u_width/2 - thk, u_height)
    .lineTo(-inner_u_width/2, u_height)
    .lineTo(-inner_u_width/2, thk)
    .lineTo(inner_u_width/2, thk)
    .lineTo(inner_u_width/2, u_height)
    .lineTo(inner_u_width/2 + thk, u_height)
    .lineTo(inner_u_width/2 + thk, 0)
    .lineTo(inner_u_width/2 + thk + wing_len, 0)
    .lineTo(inner_u_width/2 + thk + wing_len, -thk)
    .lineTo(-inner_u_width/2 - thk - wing_len, -thk)
    .close()
    .extrude(h)
)

# The shape created above is upside down compared to typical "bracket" orientation, 
# and the profile logic was a bit convoluted regarding the "u".
# Let's try the most straightforward polyline approach based on visual inspection.
# The part looks like a 'hat' section or omega profile.

# Dimensions
W_center = 20.0
H_center = 15.0
L_wing = 25.0
Thick = 5.0
Depth = 10.0
Hole_D = 4.0

# Define points for the profile on XZ plane
# Origin at bottom center of the void
pts = [
    (-W_center/2, 0),                      # Start inner bottom left
    (-W_center/2, H_center),               # Inner top left
    (-W_center/2 - Thick, H_center),       # Outer top left
    (-W_center/2 - Thick, Thick),          # Outer corner (start of wing)
    (-W_center/2 - Thick - L_wing, Thick), # End of left wing (top)
    (-W_center/2 - Thick - L_wing, 0),     # End of left wing (bottom)
    (-W_center/2 - Thick, 0),              # Bottom corner under wing
    (-W_center/2, 0)                       # Close loop? No, this is one side.
]

# Let's do the full loop
profile_pts = [
    # Start far left bottom
    (-W_center/2 - Thick - L_wing, 0),
    # Left wing top
    (-W_center/2 - Thick - L_wing, Thick),
    # Inner corner left
    (-W_center/2 - Thick, Thick),
    # Top left corner
    (-W_center/2 - Thick, H_center + Thick),
    # Top right corner
    (W_center/2 + Thick, H_center + Thick),
    # Inner corner right
    (W_center/2 + Thick, Thick),
    # Right wing top
    (W_center/2 + Thick + L_wing, Thick),
    # Right wing bottom
    (W_center/2 + Thick + L_wing, 0),
    # Right bottom inner corner
    (W_center/2, 0),
    # Right top inner corner
    (W_center/2, H_center),
    # Left top inner corner
    (-W_center/2, H_center),
    # Left bottom inner corner
    (-W_center/2, 0),
    # Close
    (-W_center/2 - Thick - L_wing, 0)
]

# Generate shape
result = (
    cq.Workplane("XZ")
    .polyline(profile_pts)
    .close()
    .extrude(Depth)
)

# Add holes
# Left hole
result = (
    result.faces(">Y")
    .workplane()
    .center(-W_center/2 - Thick - L_wing/2, Thick/2)
    .hole(Hole_D)
)

# Right hole
# We need to reset center or select the face again relative to global coords
result = (
    result.faces(">Y") # Select the front face again
    .workplane()
    .center(W_center/2 + Thick + L_wing/2, Thick/2)
    .hole(Hole_D)
)