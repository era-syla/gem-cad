import cadquery as cq

# --- Parameters ---
# Main body dimensions
thickness = 5.0
radius_disk = 25.0

# Top trapezoid dimensions
# Width at the very top
width_top = 45.0
# Y-coordinate of the top edge (relative to disk center)
height_top = 55.0
# Width of the neck where it connects to the disk
width_neck = 15.0
# Y-coordinate where the neck starts (overlapping inside the disk)
height_neck_start = 10.0

# Hole dimensions
hole_diameter = 4.0
hole_offset = 8.0  # Distance from the top edge

# Text configuration
text_string = "orlando"
text_size = 12.0
font_name = "Arial"

# --- Modeling ---

# 1. Create the base disk (centered at 0,0)
disk = cq.Workplane("XY").circle(radius_disk).extrude(thickness)

# 2. Create the top trapezoid shape
# Defined counter-clockwise
p1 = (-width_neck / 2, height_neck_start)
p2 = (width_neck / 2, height_neck_start)
p3 = (width_top / 2, height_top)
p4 = (-width_top / 2, height_top)

trapezoid = (
    cq.Workplane("XY")
    .polyline([p1, p2, p3, p4])
    .close()
    .extrude(thickness)
)

# 3. Fuse the disk and trapezoid
body = disk.union(trapezoid)

# 4. Cut the hanging hole
# Calculate center position of the hole
hole_y = height_top - hole_offset

body = (
    body.faces(">Z")
    .workplane()
    .moveTo(0, hole_y)
    .hole(hole_diameter)
)

# 5. Cut the text
# Using cut=True to subtract material
# Distance is negative to cut into the part from the >Z face
result = (
    body.faces(">Z")
    .workplane()
    .text(
        text_string,
        text_size,
        -thickness,
        font=font_name,
        kind="bold",
        halign="center",
        valign="center",
        cut=True
    )
)