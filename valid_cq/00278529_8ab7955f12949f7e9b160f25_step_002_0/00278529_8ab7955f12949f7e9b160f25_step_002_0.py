import cadquery as cq

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
length = 100.0         # Total length of the bracket (X-axis)
width = 60.0           # Total width of the bracket (Y-axis)
thickness = 15.0       # Thickness of the plate (Z-axis)
leg_width = 15.0       # Width of the two parallel legs
base_thickness = 20.0  # Thickness of the solid base section
chamfer_size = 10.0    # Size of the chamfer on the back corners
slot_length = 40.0     # Length of the side guide slots
slot_width = 6.0       # Width (height) of the side guide slots
slot_depth = 2.0       # Depth of the side guide slots

# -----------------------------------------------------------------------------
# Derived Dimensions & Calculations
# -----------------------------------------------------------------------------
# The gap between legs
gap_width = width - (2 * leg_width)
# Radius of the inner U-turn
inner_radius = gap_width / 2.0

# Coordinate calculations (assuming box is centered at origin)
x_back = -length / 2.0
x_front = length / 2.0
# The X coordinate where the solid base ends and the gap begins
x_inner_wall = x_back + base_thickness
# The X coordinate for the center of the inner radius arc
x_arc_center = x_inner_wall + inner_radius
# The X coordinate to center the side slots (visual approximation: middle of the straight leg section)
x_slot_center = (x_arc_center + x_front) / 2.0

# -----------------------------------------------------------------------------
# Modeling
# -----------------------------------------------------------------------------

# 1. Create the main block
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Apply chamfers to the back corners
# Select edges that are vertical (|Z) and at the minimal X coordinate (<X)
result = result.edges("|Z and <X").chamfer(chamfer_size)

# 3. Create the central U-shaped cutout
# We define a cutting tool composed of a rectangle and a circle (cylinder)
# Rectangle part: Starts at arc center and extends past the front of the part
rect_cutter = (
    cq.Workplane("XY")
    .moveTo(x_arc_center, 0)
    .rect(length, gap_width, centered=(False, True))
    .extrude(thickness * 2, both=True)
)

# Circular part: The rounded end of the U-slot
circ_cutter = (
    cq.Workplane("XY")
    .moveTo(x_arc_center, 0)
    .circle(inner_radius)
    .extrude(thickness * 2, both=True)
)

# Union the cutters and remove material from the main body
full_cutter = rect_cutter.union(circ_cutter)
result = result.cut(full_cutter)

# 4. Create the side slots (recesses) on the legs
# Right side slot (>Y face)
result = (
    result.faces(">Y")
    .workplane(centerOption="CenterOfMass")
    .moveTo(x_slot_center, 0)
    .slot2D(slot_length, slot_width)
    .cutBlind(-slot_depth)
)

# Left side slot (<Y face)
result = (
    result.faces("<Y")
    .workplane(centerOption="CenterOfMass")
    .moveTo(x_slot_center, 0)
    .slot2D(slot_length, slot_width)
    .cutBlind(-slot_depth)
)