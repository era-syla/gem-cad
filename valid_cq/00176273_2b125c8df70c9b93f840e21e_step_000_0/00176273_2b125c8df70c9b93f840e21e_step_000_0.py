import cadquery as cq

# Parametric dimensions for the model
wall_length = 100.0
wall_height = 50.0
wall_thickness = 4.0

# Dimensions for the horizontal trellis/frame structure
frame_length = 60.0    # Length along the wall
frame_depth = 30.0     # Distance extending out from the wall
beam_thickness = 2.0   # Thickness of the frame members
num_bays = 3           # Number of openings in the grid

# 1. Create the Main Wall
# A rectangular solid standing vertically
wall = (cq.Workplane("XY")
        .box(wall_length, wall_thickness, wall_height)
        .translate((0, 0, wall_height / 2)))

# 2. Create the Horizontal Frame Structure
# Located at the top of the wall, offset to one side
frame_center_x = (wall_length / 2) - (frame_length / 2)
frame_center_y = (wall_thickness / 2) + (frame_depth / 2)
frame_center_z = wall_height - (beam_thickness / 2)

# Create longitudinal rails (parallel to wall)
rail_inner = (cq.Workplane("XY")
              .box(frame_length, beam_thickness, beam_thickness)
              .translate((frame_center_x, (wall_thickness/2) + (beam_thickness/2), frame_center_z)))

rail_outer = (cq.Workplane("XY")
              .box(frame_length, beam_thickness, beam_thickness)
              .translate((frame_center_x, (wall_thickness/2) + frame_depth - (beam_thickness/2), frame_center_z)))

# Create transverse beams (perpendicular to wall)
transverse_beams = []
# Calculate spacing to create equal bays
start_x = frame_center_x - (frame_length / 2) + (beam_thickness / 2)
spacing = (frame_length - beam_thickness) / num_bays

for i in range(num_bays + 1):
    pos_x = start_x + (i * spacing)
    beam = (cq.Workplane("XY")
            .box(beam_thickness, frame_depth, beam_thickness)
            .translate((pos_x, frame_center_y, frame_center_z)))
    transverse_beams.append(beam)

# 3. Create Vertical Posts/Rods (representing the thin lines in the image)
post_height = wall_height + 15.0
post_radius = 0.4
post_offset = 10.0

post1 = (cq.Workplane("XY")
         .circle(post_radius)
         .extrude(post_height)
         .translate((-wall_length/2 - post_offset, 0, 0)))

post2 = (cq.Workplane("XY")
         .circle(post_radius)
         .extrude(post_height * 0.7)
         .translate((-wall_length/2 - post_offset - 5, 5, 0)))

# 4. Combine all geometries into the final result
result = wall.union(rail_inner).union(rail_outer)

for b in transverse_beams:
    result = result.union(b)

result = result.union(post1).union(post2)