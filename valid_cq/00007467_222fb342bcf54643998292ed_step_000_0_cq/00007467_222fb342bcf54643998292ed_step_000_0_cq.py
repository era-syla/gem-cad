import cadquery as cq

# Parameters
cyl_count = 6
cyl_radius = 5.0
wall_thickness = 1.0
height = 30.0
spacing = 9.0  # Slightly less than 2*radius to ensure overlap/merge

# Back bracket parameters
bracket_width = 15.0
bracket_depth = 5.0
bracket_height = 8.0 # Top portion
bracket_gap_height = 15.0 # How far down the bracket starts
clip_thickness = 2.0

# Derived parameters
cyl_outer_diam = cyl_radius * 2
cyl_inner_radius = cyl_radius - wall_thickness

# Create the main row of cylinders
# We construct the base profile first
cylinders = cq.Workplane("XY")

for i in range(cyl_count):
    # Calculate center position for each cylinder
    x_pos = i * spacing
    
    # Create a cylinder solid
    new_cyl = (
        cq.Workplane("XY")
        .center(x_pos, 0)
        .circle(cyl_radius)
        .extrude(height)
    )
    
    # Union with the main object
    if i == 0:
        cylinders = new_cyl
    else:
        cylinders = cylinders.union(new_cyl)

# Create the holes
holes = cq.Workplane("XY")
for i in range(cyl_count):
    x_pos = i * spacing
    new_hole = (
        cq.Workplane("XY")
        .center(x_pos, 0)
        .circle(cyl_inner_radius)
        .extrude(height)
    )
    if i == 0:
        holes = new_hole
    else:
        holes = holes.union(new_hole)

# Subtract holes from the main body
main_body = cylinders.cut(holes)

# Create the back bracket feature
# Calculate center of the cylinder array to align the bracket
total_width = (cyl_count - 1) * spacing
center_x = total_width / 2.0

# Positioning the bracket
# It appears attached to the back (positive Y in standard orientation relative to the cylinders)
bracket_y_offset = cyl_radius - 1.0 # Slight overlap into the cylinders

bracket = (
    cq.Workplane("XY")
    .center(center_x, bracket_y_offset)
    .rect(bracket_width, bracket_depth * 2, centered=True) # Double depth because we'll cut half
    .extrude(height)
)

# Refine the bracket shape
# It looks like a U-shape or a clip attached to the back
# Let's build a specific shape for the clip on the YZ plane (side view) or simply extrude a profile from top

# Re-approach bracket: Draw the profile on the top (XY) and extrude down?
# Or draw on the back face.
# Let's create a separate solid for the bracket structure.

# Main block of the bracket
bracket_block = (
    cq.Workplane("XY")
    .workplane(offset=height - bracket_height) # Start near the top
    .center(center_x, bracket_y_offset)
    .moveTo(0, 0)
    .rect(bracket_width, bracket_depth * 2, centered=True) # Initial block
    .extrude(bracket_height)
)

# Only keep the part sticking out the back (positive Y relative to cylinder center line)
# And shift it so it starts from the cylinder surface
back_mount = (
    cq.Workplane("XY")
    .workplane(offset=height - bracket_height - 2.0) # Position z
    .center(center_x, cyl_radius * 0.8) # Position x, y
    .box(bracket_width, bracket_depth + 2.0, bracket_height + 2.0, centered=(True, False, False))
)

# Create the "hook" or inner cutout of the bracket
# The image shows a rectangular housing with a thin wall
bracket_outer = (
    cq.Workplane("XY")
    .workplane(offset=height - 10.0) # Position vertical
    .center(center_x, cyl_radius - 1.0) # Center X, Start Y inside cylinder
    .rect(bracket_width, 8.0, centered=(True, False)) # Draw rectangle backwards
    .extrude(10.0)
)

bracket_cutout = (
    cq.Workplane("XY")
    .workplane(offset=height - 10.0)
    .center(center_x, cyl_radius + clip_thickness) 
    .rect(bracket_width - (clip_thickness*2), 8.0, centered=(True, False))
    .extrude(10.0)
)

final_bracket = bracket_outer.cut(bracket_cutout)

# Add the little retaining lip on the bracket
lip = (
    cq.Workplane("XY")
    .workplane(offset=height - 2.0)
    .center(center_x, cyl_radius + 6.0) # Further back
    .rect(bracket_width - (clip_thickness*2), 1.5, centered=(True, False))
    .extrude(2.0)
)

# Combine everything
result = main_body.union(final_bracket).union(lip)

# Center the whole assembly for better view
result = result.translate((-center_x, 0, 0))