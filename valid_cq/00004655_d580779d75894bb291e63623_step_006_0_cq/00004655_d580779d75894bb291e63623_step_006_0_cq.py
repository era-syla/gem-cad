import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the main bar
length = 200.0
width = 15.0
height = 15.0

# End hole dimensions (large counterbored holes)
end_hole_dia = 6.0
end_cbore_dia = 10.0
end_cbore_depth = 5.0
end_hole_offset = 10.0  # Distance from the end edge

# Side mounting holes (smaller holes along the top face)
side_hole_dia = 4.0
side_hole_spacing = 30.0  # Spacing relative to ends/center
num_side_holes = 2

# Rail/Groove feature dimensions
rail_width = 8.0
rail_depth = 3.0
# The rail cutout seems to be on the front face
rail_y_pos = height / 2.0  # Centered vertically on the face

# Internal mechanism/slider details (simplified representation based on image)
# There appear to be two thinner cylindrical rods or rails inside the main groove
inner_rod_dia = 2.5
inner_rod_spacing = 4.0

# Central cutout/mechanism block
center_cutout_width = 20.0
center_cutout_depth = 4.0

# --- Modeling ---

# 1. Base Block
# Create the main rectangular body
base = cq.Workplane("XY").box(length, width, height)

# 2. Main Longitudinal Groove/Pocket
# This is the recess on the front face (-Y direction)
groove = (
    cq.Workplane("XZ")
    .workplane(offset=-width/2.0)  # Move to the front face
    .center(0, 0)
    .rect(length - (end_hole_offset * 2), rail_width)
    .extrude(-rail_depth, combine=False) # Extrude inward (negative)
)
result = base.cut(groove)

# 3. End Counterbored Holes
# Holes on the top face (+Z) at both ends
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-(length/2 - end_hole_offset), 0),
        ((length/2 - end_hole_offset), 0)
    ])
    .cboreHole(end_hole_dia, end_cbore_dia, end_cbore_depth)
)

# 4. End Holes (Through holes on the side/ends)
# Looking at the image, there are holes on the end faces (-X, +X) or side face.
# The image shows a hole on the small end face (-X)
result = (
    result.faces("<X")
    .workplane()
    .hole(end_hole_dia, width) # Through hole along X axis at the end
)
result = (
    result.faces(">X")
    .workplane()
    .hole(end_hole_dia, width) # Through hole along X axis at the other end
)

# 5. Top Mounting Holes
# Smaller holes along the top surface, inwards from the large end holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-(length/2 - end_hole_offset - side_hole_spacing), 0),
        ((length/2 - end_hole_offset - side_hole_spacing), 0)
    ])
    .hole(side_hole_dia)
)

# 6. Internal Rods/Rails (The mechanical looking part inside the groove)
# We add two small cylinders inside the groove created in step 2.
rod_length = length - (end_hole_offset * 2.5) # Slightly shorter than the groove

rod_1 = (
    cq.Workplane("YZ")
    .workplane(offset=-(length/2 - end_hole_offset * 1.25)) # Start position X
    .center(-width/2 + rail_depth/2, inner_rod_spacing/2) # Position in YZ plane
    .circle(inner_rod_dia/2)
    .extrude(rod_length)
)

rod_2 = (
    cq.Workplane("YZ")
    .workplane(offset=-(length/2 - end_hole_offset * 1.25))
    .center(-width/2 + rail_depth/2, -inner_rod_spacing/2)
    .circle(inner_rod_dia/2)
    .extrude(rod_length)
)

# Combine rods into the main body
result = result.union(rod_1).union(rod_2)

# 7. Central Slider Block / Mechanism
# There is a small block in the very center interrupting the rods
center_block = (
    cq.Workplane("XY")
    .workplane(offset=0) # Z=0
    .center(0, -width/2 + rail_depth/2) # Center X, Offset Y to be in groove
    .box(center_cutout_width, rail_depth, rail_width - 1.0)
)
result = result.union(center_block)

# 8. Side Screws/Pins on the internal mechanism
# The image shows small black dots/holes on the internal rail assembly
# We will cut small holes into the rods/groove area to simulate these fasteners
pin_locations = [
    -center_cutout_width/2 - 10, 
    -center_cutout_width/2 - 35,
    center_cutout_width/2 + 10,
    center_cutout_width/2 + 35
]

for x_loc in pin_locations:
    # Cut holes through the rails on the front face
    result = (
        result.faces("<Y")
        .workplane()
        .center(x_loc, 0)
        .hole(1.5, depth=rail_depth + 1.0)
    )

# 9. Square protruding tab/stop on the left side of the groove
tab_size = 4.0
tab_pos_x = -(length/2 - end_hole_offset) + 2.0
tab = (
    cq.Workplane("XY")
    .center(tab_pos_x, -width/2)
    .box(tab_size, 2.0, tab_size)
)
result = result.union(tab)


# Final Result
# result is already updated in previous steps