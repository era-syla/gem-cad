import cadquery as cq

# Define parameters for dimensions (approximate based on visual scale)
# The long beam on the left
left_beam_length = 200.0
left_beam_width = 10.0
left_beam_thickness = 2.0

# The short tab attached to the left beam
left_tab_length = 30.0
left_tab_width = 15.0  # Slightly wider than the beam
left_tab_thickness = 2.0

# The long beam on the right (part 1)
right_beam1_length = 180.0
right_beam1_width = 8.0
right_beam1_thickness = 2.0

# The shorter beam on the right (part 2)
right_beam2_length = 100.0
right_beam2_width = 8.0
right_beam2_thickness = 2.0

# --- Left Part Construction ---
# Create the main long beam
left_beam = (
    cq.Workplane("XY")
    .box(left_beam_length, left_beam_width, left_beam_thickness)
    .translate((-left_beam_length / 2, 0, 0))
)

# Create the perpendicular tab
# It's attached at one end, rotated 90 degrees
left_tab = (
    cq.Workplane("XY")
    .box(left_tab_width, left_tab_thickness, left_tab_length) # Swap dims to make it vertical-ish relative to beam
    .rotate((0,0,0), (0,0,1), 90) # Rotate to be perpendicular
    .translate((0, 0, left_tab_length/2 - left_beam_thickness/2)) # Move up
    .translate((left_tab_thickness/2, 0, 0)) # Shift to align edge
)

# Combine left assembly (Note: in the image they look joined)
# It looks like an L-bracket shape where the long part is flat and the short part sticks up/down.
# Let's refine the placement to match the image:
# The long part is horizontal. At the end, there is a short part perpendicular to it.
part_left = (
    cq.Workplane("XY")
    .box(left_beam_length, left_beam_width, left_beam_thickness)
    .translate((-left_beam_length / 2, 0, 0))
)

tab_left = (
    cq.Workplane("YZ")
    .workplane(offset=0) 
    .box(left_tab_length, left_tab_thickness, left_tab_width)
    .rotate((0,0,0), (0,1,0), 90) # Orient vertical
    .translate((0, 0, left_tab_length/2 - left_beam_thickness/2))
)
# Actually, looking closer at the left shape, it's an L-shape made of flat bar.
# One leg is long, lying flat. The other leg is short, vertical, at 90 degrees.
left_assembly = (
    cq.Workplane("XY")
    .box(left_beam_length, left_beam_width, left_beam_thickness)
    .translate((-left_beam_length/2, 0, 0))
    .union(
        cq.Workplane("YZ")
        .box(left_tab_width, left_tab_length, left_tab_thickness)
        .rotate((0,0,0), (0,1,0), 90) # Stand it up
        .translate((left_tab_thickness/2, 0, left_tab_length/2 - left_beam_thickness/2))
    )
)


# --- Right Part Construction ---
# Two separate beams angled relative to the viewer.
# They look like they are floating separately.

# First right beam (long one)
right_part1 = (
    cq.Workplane("XY")
    .box(right_beam1_length, right_beam1_width, right_beam1_thickness)
    .rotate((0,0,0), (0,0,1), -60) # Angled in XY plane
    .translate((100, -80, 0)) # Position relative to left part
)

# Second right beam (shorter one, angled differently)
right_part2 = (
    cq.Workplane("XY")
    .box(right_beam2_length, right_beam2_width, right_beam2_thickness)
    .rotate((0,0,0), (0,0,1), -75) # Slightly different angle
    .translate((130, -50, 0)) # Offset position
)

# Combine all into one result
result = left_assembly.union(right_part1).union(right_part2)