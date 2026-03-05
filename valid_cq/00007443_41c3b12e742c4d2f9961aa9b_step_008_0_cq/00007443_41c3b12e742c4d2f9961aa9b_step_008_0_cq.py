import cadquery as cq

# Define parametric variables for common dimensions to ensure consistency
# General tolerances/sizes based on visual estimation of small mechanical hardware
hole_dia_small = 2.0
hole_dia_med = 3.0
hole_dia_large = 5.0
hex_size = 4.0  # Across flats
wall_thick = 1.0

# ---------------------------------------------------------
# Part 1: Hex Standoff / Spacer (Far Left)
# Description: Cylindrical body with internal hex hole
p1_outer_dia = 8.0
p1_height = 8.0
part1 = (
    cq.Workplane("XY")
    .circle(p1_outer_dia / 2)
    .extrude(p1_height)
    .faces(">Z")
    .polygon(6, hex_size * 1.1547) # 1.1547 converts flat-to-flat to dia
    .cutThruAll()
    .translate((-40, 0, 0))
)

# ---------------------------------------------------------
# Part 2: U-Bracket / Clip (Second from left)
# Description: U-shaped extrusion with a hole
p2_width = 8.0
p2_depth = 6.0
p2_thickness = 2.0
p2_height = 6.0

part2 = (
    cq.Workplane("XY")
    .box(p2_width, p2_depth, p2_height)
    # Cut the U-shape out of the middle
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(p2_width - 2*p2_thickness, p2_depth + 1)
    .cutBlind(-(p2_height - p2_thickness))
    # Add hole through the bottom
    .faces("<Z")
    .workplane()
    .center(0, 0)
    .circle(hole_dia_small / 2)
    .cutThruAll()
    # Rotate to match image orientation roughly
    .rotate((0,0,0), (1,0,0), 90)
    .translate((-30, 0, p2_depth/2))
)

# ---------------------------------------------------------
# Part 3: T-Nut / Sliding Nut (Third from left)
# Description: Rectangular nut with a tapped hole, possibly for extrusion profile
p3_width = 10.0
p3_length = 10.0
p3_thickness = 3.0

part3 = (
    cq.Workplane("XY")
    .box(p3_width, p3_length, p3_thickness)
    .faces(">Z")
    .workplane()
    .circle(hole_dia_med / 2)
    .cutThruAll()
    .translate((-20, 0, 0))
)

# ---------------------------------------------------------
# Part 4: Flat Plate / Shim (Fourth from left)
# Description: Simple rectangular plate with a hole
p4_width = 8.0
p4_length = 12.0
p4_thickness = 1.5

part4 = (
    cq.Workplane("XY")
    .box(p4_width, p4_length, p4_thickness)
    .faces(">Z")
    .workplane()
    .circle(hole_dia_small / 2)
    .cutThruAll()
    .translate((-10, 0, 0))
)

# ---------------------------------------------------------
# Part 5: Tall Spacer (Fifth from left)
# Description: Tall cylinder with through hole
p5_dia = 6.0
p5_height = 10.0

part5 = (
    cq.Workplane("XY")
    .circle(p5_dia / 2)
    .extrude(p5_height)
    .faces(">Z")
    .workplane()
    .circle(hole_dia_med / 2)
    .cutThruAll()
    .translate((0, 0, 0))
)

# ---------------------------------------------------------
# Part 6: Short Washer/Spacer (Sixth from left)
# Description: Short cylinder with through hole
p6_dia = 6.0
p6_height = 4.0

part6 = (
    cq.Workplane("XY")
    .circle(p6_dia / 2)
    .extrude(p6_height)
    .faces(">Z")
    .workplane()
    .circle(hole_dia_med / 2)
    .cutThruAll()
    .translate((10, 0, 0))
)

# ---------------------------------------------------------
# Part 7: Medium Spacer (Seventh from left)
# Description: Medium height cylinder with through hole
p7_dia = 6.0
p7_height = 7.0

part7 = (
    cq.Workplane("XY")
    .circle(p7_dia / 2)
    .extrude(p7_height)
    .faces(">Z")
    .workplane()
    .circle(hole_dia_med / 2)
    .cutThruAll()
    .translate((20, 0, 0))
)

# ---------------------------------------------------------
# Part 8: Threaded Insert / Brass Nut (Eighth from left)
# Description: Knurled insert look, smaller diameter
p8_dia = 4.0
p8_height = 5.0

part8 = (
    cq.Workplane("XY")
    .circle(p8_dia / 2)
    .extrude(p8_height)
    .faces(">Z")
    .workplane()
    .circle(hole_dia_small / 2)
    .cutThruAll()
    # Add a small chamfer to indicate it's an insert
    .faces(">Z or <Z")
    .chamfer(0.2)
    .translate((30, 0, 0))
)

# ---------------------------------------------------------
# Part 9: Lead Nut Block / Flange (Far Right)
# Description: Oblong block with large center hole and two mounting holes (hex recesses)
p9_length = 25.0
p9_width = 12.0
p9_height = 4.0
p9_center_hole = 5.0
p9_mount_hole = 3.0

part9 = (
    cq.Workplane("XY")
    .box(p9_length, p9_width, p9_height)
    .edges("|Z")
    .fillet(3.0) # Round the corners
    # Center Lead Screw Hole
    .faces(">Z")
    .workplane()
    .circle(p9_center_hole / 2)
    .cutThruAll()
    # Mounting holes with Hex Recess
    .faces(">Z")
    .workplane()
    .pushPoints([(-8, 0), (8, 0)])
    .polygon(6, hex_size * 1.1547) # Hex recess
    .cutBlind(-1.5)
    .faces(">Z")
    .workplane()
    .pushPoints([(-8, 0), (8, 0)])
    .circle(p9_mount_hole / 2) # Through hole
    .cutThruAll()
    .translate((50, 0, 0))
)

# ---------------------------------------------------------
# Part 10: Half-Moon / Woodruff Key (Below left group)
# Description: Half-cylinder shape
p10_dia = 8.0
p10_thick = 3.0

part10 = (
    cq.Workplane("XY")
    .circle(p10_dia/2)
    .extrude(p10_thick)
    # Cut in half to make moon shape
    .faces(">Z")
    .workplane()
    .rect(p10_dia, p10_dia/2)
    .translate((0, -p10_dia/4))
    .cutThruAll()
    # Add a hole
    .faces(">Z")
    .workplane()
    .circle(hole_dia_small/2)
    .cutThruAll()
    .rotate((0,0,0), (1,0,0), 90)
    .translate((-30, -15, p10_thick/2))
)


# Combine all parts into a single assembly result
result = (
    part1
    .union(part2)
    .union(part3)
    .union(part4)
    .union(part5)
    .union(part6)
    .union(part7)
    .union(part8)
    .union(part9)
    .union(part10)
)