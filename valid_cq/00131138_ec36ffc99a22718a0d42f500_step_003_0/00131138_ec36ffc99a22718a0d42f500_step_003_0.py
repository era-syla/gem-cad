import cadquery as cq

# --- Parametric Dimensions ---
length = 120.0       # Total length of the rectangular plate
width = 90.0         # Total width of the rectangular plate
thickness = 8.0      # Thickness of the plate
circle_diam = 50.0   # Diameter of the central circular section
hole_diam = 4.0      # Diameter of the small offset hole
hole_offset = 12.0   # Distance of small hole from center

# --- Geometry Construction ---

# 1. Create the central circular disk
# It is a cylinder with a small hole offset from the center
center_disk = (
    cq.Workplane("XY")
    .cylinder(height=thickness, radius=circle_diam / 2)
    .faces(">Z")
    .workplane()
    .center(hole_offset, 0)
    .hole(hole_diam)
)

# 2. Create the Left Plate Half
# A rectangular block covering the left side (-X), with a semi-circular cutout
left_plate = (
    cq.Workplane("XY")
    # Create box for the left half, shifted to the left
    .box(length / 2, width, thickness)
    .translate((-length / 4, 0, 0))
    # Cut out the central cylinder shape
    .cut(
        cq.Workplane("XY").cylinder(height=thickness, radius=circle_diam / 2)
    )
)

# 3. Create the Right Plate Half
# A rectangular block covering the right side (+X), with a semi-circular cutout
right_plate = (
    cq.Workplane("XY")
    # Create box for the right half, shifted to the right
    .box(length / 2, width, thickness)
    .translate((length / 4, 0, 0))
    # Cut out the central cylinder shape
    .cut(
        cq.Workplane("XY").cylinder(height=thickness, radius=circle_diam / 2)
    )
)

# --- Final Assembly ---
# Combine the three distinct solids into a single compound object.
# This method preserves the internal edges (seams) visible in the reference image.
result = cq.Workplane("XY")
result = result.add(left_plate.val())
result = result.add(right_plate.val())
result = result.add(center_disk.val())