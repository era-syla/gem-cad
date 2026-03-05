import cadquery as cq

# Parametric dimensions
length = 90.0        # Total length of the block
width = 20.0         # Thickness of the block
height = 35.0        # Height of the block
radius = 25.0        # Radius of the bottom semi-circular cutout
hole_dia = 6.0       # Diameter of the through holes
cbore_dia = 10.5     # Diameter of the counterbore
cbore_depth = 2.5    # Depth of the counterbore

# Derived calculation for hole positioning
# Holes are centered on the "legs" (solid material on either side of the arch)
# Leg X span is from 'radius' to 'length/2'
leg_center_x = radius + (length/2 - radius) / 2

# 1. Create the base block
# Centered on X and Y, but sitting on the Z plane (Z=0 to Z=height)
# This aligns the bottom face with Z=0, simplifying the arch cut
result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))

# 2. Create the central semi-circular cutout
# We create a cylinder along the Y-axis (XZ plane extrusion) centered at (0,0,0)
cutout = (
    cq.Workplane("XZ")
    .circle(radius)
    .extrude(width * 2, both=True)  # Extrude symmetrically to cut through the width
)

# Apply the cut
result = result.cut(cutout)

# 3. Add Top Mounting Holes
# Select the top face (>Z) and place counterbored holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(leg_center_x, 0), (-leg_center_x, 0)])
    .cboreHole(hole_dia, cbore_dia, cbore_depth)
)

# 4. Add Front Mounting Holes
# Select the front face (<Y)
# The workplane on this face will have its origin at the face center (Z = height/2)
# So (x, 0) corresponds to the vertical center of the block
result = (
    result.faces("<Y")
    .workplane()
    .pushPoints([(leg_center_x, 0), (-leg_center_x, 0)])
    .cboreHole(hole_dia, cbore_dia, cbore_depth)
)