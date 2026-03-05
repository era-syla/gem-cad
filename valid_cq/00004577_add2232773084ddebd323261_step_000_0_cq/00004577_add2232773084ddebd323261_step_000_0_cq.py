import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions based on visual estimation
base_length = 50.0  # Length of the horizontal arm
base_width = 3.0    # Width of the horizontal arm (thickness of the L-shape)
vertical_height = 50.0 # Height of the vertical arm
vertical_width = 3.0   # Width of the vertical arm (thickness of the L-shape)
thickness = 1.0     # Thickness of the material (thin wall)

# Gusset dimensions
gusset_base = 30.0   # Length of gusset along the base
gusset_height = 30.0 # Height of gusset along the vertical part
gusset_thickness = 1.0

# Small base tab dimensions (the part sticking out at the bottom right)
tab_length = 15.0
tab_width = 10.0
tab_thickness = 1.0

# --- Geometry Construction ---

# 1. Create the L-shaped frame (long horizontal arm and vertical post)
# We'll create the horizontal arm first
horizontal_arm = (
    cq.Workplane("XY")
    .box(base_length, thickness, base_width)
    .translate((-base_length/2 + thickness/2, 0, 0)) # Align to corner
)

# Create the vertical post
vertical_post = (
    cq.Workplane("XY")
    .box(thickness, thickness, vertical_height)
    .translate((0, 0, vertical_height/2 - base_width/2)) # Align vertically
)

# 2. Create the triangular gusset
# The gusset connects the horizontal arm and the vertical post
gusset_points = [
    (0, 0),
    (-gusset_base, 0),
    (0, gusset_height)
]

gusset = (
    cq.Workplane("XZ")
    .polyline(gusset_points)
    .close()
    .extrude(gusset_thickness)
    .translate((0, -gusset_thickness/2, base_width/2)) # Align to center of the frame
)

# 3. Create the bottom tab (the small rectangular piece at the corner)
# It extends in the Y direction from the corner
bottom_tab = (
    cq.Workplane("XY")
    .box(thickness, tab_length, tab_width)
    .translate((0, tab_length/2 + thickness/2, 0)) # Position at the corner extending out
    .rotate((1,0,0), (0,0,0), 90) # Rotate to lie flat if needed, but image suggests it's another plane
)
# Looking closely at the image, the bottom tab seems to be perpendicular to the main horizontal arm.
# Let's re-evaluate the orientation.
# Let's assume the L-bracket is in the XZ plane mostly.
# - Horizontal arm along -X
# - Vertical post along +Z
# - Gusset in XZ plane
# - There is a third flange. It looks like a T-section or an L-section at the base.
# Let's try a different approach to match the visual better.

# Re-evaluating based on "T" intersection at the corner:
# It looks like three planes intersecting at a corner:
# Plane 1: XZ plane (The gusset and the thin vertical/horizontal edges)
# Plane 2: XY plane (The bottom tab)
# Plane 3: YZ plane (The vertical spine?)

# Let's try this composition:
# 1. A vertical spine (cylinder or thin box) at the origin going up Z.
# 2. A horizontal spine going along -X.
# 3. A triangular plate (gusset) connecting them in the XZ plane.
# 4. A rectangular plate at the bottom corner, extending into +Y.

# Revised Parameters
spine_thickness = 1.5  # Thickness of the 'rods' or edges
flange_thickness = 0.5 # Thickness of the plate material

# 1. Vertical Rod/Edge
vert_rod = (
    cq.Workplane("XY")
    .circle(spine_thickness/2)
    .extrude(vertical_height)
)

# 2. Horizontal Rod/Edge
horiz_rod = (
    cq.Workplane("YZ")
    .circle(spine_thickness/2)
    .extrude(base_length)
    .rotate((0,1,0), (0,0,0), -90) # Point along -X
)

# 3. The Gusset Plate
# Drawn in XZ plane, connecting the two rods
gusset_plate = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(-gusset_base, 0)
    .lineTo(0, gusset_height)
    .close()
    .extrude(flange_thickness)
    .translate((0, -flange_thickness/2, 0)) # Center on the rods
)

# 4. The Bottom Tab
# It looks like a flat plate extending from the corner in the +Y direction.
# It seems to have a slight angle or is just rectangular.
tab_plate = (
    cq.Workplane("XY")
    .moveTo(0,0)
    .lineTo(0, 15) # Length in Y
    .lineTo(10, 15) # Width in X
    .lineTo(0, 0)   # Back to origin (making it triangular?)
    # Looking at the image again, the bottom piece is a rectangle.
)
tab_plate_rect = (
    cq.Workplane("XY")
    .box(10, 20, flange_thickness) # Width X, Length Y, Thickness Z
    .translate((5 - spine_thickness/2, 10, 0)) 
    # Adjust position to connect to corner.
    # The image shows a small rectangular foot.
)

# Let's simplify the bottom tab to match the image better.
# The image shows a distinct piece sticking out "towards" the viewer (if Y is towards viewer).
foot_length = 15.0
foot_width = 8.0
foot = (
    cq.Workplane("XY")
    .box(foot_width, foot_length, flange_thickness)
    .translate((foot_width/2 - spine_thickness/2, foot_length/2, 0))
)

# Combining everything
# Let's refine the "rods" to be square cross-section to match the sharp edges in the rendering better,
# or keep them as very thin boxes. The image looks like thin sheet metal or joined flat bars.

# Final Logic:
# 1. Vertical flat bar (Z axis)
# 2. Horizontal flat bar (X axis)
# 3. Gusset connecting them
# 4. Another flat bar extending in Y axis at the base.

w = 1.0 # Thickness of the bars

# Vertical Bar
v_bar = cq.Workplane("XY").box(w, w, vertical_height).translate((0,0,vertical_height/2))

# Horizontal Bar (Long)
h_bar = cq.Workplane("XY").box(base_length, w, w).translate((-base_length/2, 0, w/2))

# Gusset (Triangle)
# Points relative to the intersection
p1 = (0, 0)
p2 = (-base_length * 0.6, 0) # Gusset doesn't go all the way
p3 = (0, vertical_height * 0.7)
gusset_shape = (
    cq.Workplane("XZ")
    .polyline([p1, p2, p3])
    .close()
    .extrude(w/2) # Thin gusset
    .translate((0, -w/4, w/2)) # Align so it sits flush or centered
)

# The foot tab (Y axis)
# It looks like a wider, short tab
foot_tab = (
    cq.Workplane("XY")
    .box(w*8, w*12, w) # Wide and short
    .translate((w*2, w*6, w/2)) 
    # Positioned so corner touches origin
)

# Actually, looking at the "foot" in the image, it looks like a separate triangular prism or a chamfered block.
# Let's try a simple rectangular extrusion for the foot, perpendicular to the main L.
foot_bar = cq.Workplane("XY").box(w, 15, w).translate((0, 15/2, w/2))
foot_flange = (
    cq.Workplane("XY")
    .moveTo(0,0)
    .lineTo(5, 10)
    .lineTo(0, 10)
    .close()
    .extrude(w)
) # This is guessing. Let's stick to the visible dominant shapes.

# Dominant Shapes Reconstruction:
# 1. A long thin L-bracket in the XZ plane.
# 2. A triangular web (gusset) reinforcing the angle.
# 3. A rectangular tab extending in the +Y direction from the corner.

L_arm_len = 60.0
V_arm_len = 50.0
Tab_len = 15.0
Tab_width = 8.0
Thickness = 1.0

# Vertical
part1 = cq.Workplane("XY").box(Thickness, Thickness, V_arm_len).translate((0, 0, V_arm_len/2))

# Horizontal
part2 = cq.Workplane("XY").box(L_arm_len, Thickness, Thickness).translate((-L_arm_len/2 + Thickness/2, 0, Thickness/2))

# Gusset
# Create a right triangle in XZ plane
gusset = (
    cq.Workplane("XZ")
    .moveTo(0, Thickness) # Start slightly above bottom to align
    .lineTo(-L_arm_len * 0.6, Thickness)
    .lineTo(0, V_arm_len * 0.7)
    .close()
    .extrude(Thickness/2)
    .translate((0, -Thickness/4, 0))
)

# Bottom Tab (extending in Y)
# Based on the shadow/reflection, it looks like a flat plate
part3 = (
    cq.Workplane("XY")
    .box(Tab_width, Tab_len, Thickness)
    .translate((Tab_width/2 - Thickness/2, Tab_len/2, Thickness/2))
)

# Combine
result = part1.union(part2).union(gusset).union(part3)