import cadquery as cq

# --- Parameters ---
r_in = 30.0              # Inner radius of the curved section
r_out = 50.0             # Outer radius of the curved section
thickness = 20.0         # Total height of the part
wall_thickness = 4.0     # Thickness of the top and bottom plates
ext_length = 25.0        # Length of the straight rectangular block at the back
hole_dia_tip = 6.0       # Diameter of the hole at the rounded tip
hole_dia_top = 3.0       # Diameter of the small mounting holes on top
rect_hole_w = 12.0       # Width of the rectangular cutout in the back block

# --- Derived Dimensions ---
mid_radius = (r_in + r_out) / 2.0
strip_width = r_out - r_in
tip_radius = strip_width / 2.0
gap_height = thickness - (2 * wall_thickness)

# Points for constructing the arc segments (90 degrees)
# 45-degree midpoint for 3-point arcs
p_out_mid = (r_out * 0.70710678, r_out * 0.70710678)
p_in_mid = (r_in * 0.70710678, r_in * 0.70710678)

# --- Geometry Construction ---

# 1. Base Profile Sketch
# The shape consists of a straight rectangular section extending into a curved C-shape.
# Orientation: Arc center at (0,0). Straight block extends along -X axis.
base_sketch = (
    cq.Workplane("XY")
    .moveTo(-ext_length, r_in)
    .lineTo(-ext_length, r_out)  # Back flat face
    .lineTo(0, r_out)            # Straight outer edge
    .threePointArc(p_out_mid, (r_out, 0))  # Outer arc
    .threePointArc((mid_radius, -tip_radius), (r_in, 0)) # Rounded tip (180 deg turn)
    .threePointArc(p_in_mid, (0, r_in))    # Inner arc
    .close()
)

# 2. Extrude Main Solid Body
result = base_sketch.extrude(thickness)

# 3. Create and Cut the Curved Slot
# This removes the material between the top and bottom plates in the curved section.
# It cuts completely through the radial width at the curve.
slot_sketch = (
    cq.Workplane("XY")
    .moveTo(0, r_in)
    .lineTo(0, r_out)
    .threePointArc(p_out_mid, (r_out, 0))
    .threePointArc((mid_radius, -tip_radius), (r_in, 0))
    .threePointArc(p_in_mid, (0, r_in))
    .close()
)

# Extrude the slot cutter and position it in the middle of the Z-height
slot_cutter = slot_sketch.extrude(gap_height).translate((0, 0, wall_thickness))
result = result.cut(slot_cutter)

# 4. Create and Cut the Rectangular Hole in the Back Block
# This hole goes through the back block, connecting to the curved slot.
# It leaves side walls, creating a box frame at the back.
block_hole_cutter = (
    cq.Workplane("XY")
    .rect(ext_length, rect_hole_w)  # Rectangle centered at (0,0)
    .extrude(gap_height)
    # Move to correct position:
    # X: Centered on the block length (-ext_length/2)
    # Y: Centered on the arc radius (mid_radius)
    # Z: Lifted to the gap height (wall_thickness)
    .translate((-ext_length / 2.0, mid_radius, wall_thickness))
)
result = result.cut(block_hole_cutter)

# 5. Add Mounting Holes
# Hole at the rounded tip (vertical, through all)
result = (
    result.faces("<Z")
    .workplane()
    .moveTo(mid_radius, 0)
    .circle(hole_dia_tip / 2.0)
    .cutThruAll()
)

# Small holes on the top surface of the back block
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(-8, mid_radius)
    .circle(hole_dia_top / 2.0)
    .moveTo(-18, mid_radius)
    .circle(hole_dia_top / 2.0)
    .cutBlind(-10)  # Cut deep enough to go through the top plate
)