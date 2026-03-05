import cadquery as cq

# Parameters
disc_radius = 50
disc_thickness = 3
block_x = 10   # block size in X direction (horizontal on disc)
block_y = 30   # block size in Y direction (vertical on disc)
block_z = 20   # block thickness (depth, into screen)
large_hole_dia = 12
small_hole_dia = 4
small_hole_offset = 8  # Y offset for the two small holes
small_hole_separation = 8  # spacing in X for small holes

# Build disc and block
result = (
    cq.Workplane("XY")
    .circle(disc_radius)
    .extrude(disc_thickness)
    .faces(">Z")
    .workplane()
    .rect(block_x, block_y)
    .extrude(block_z)
)

# Large central hole in the block top face
result = result.faces(">Z").workplane().hole(large_hole_dia)

# Two small holes on the block top face
small_holes = [(-small_hole_separation/2, small_hole_offset),
               ( small_hole_separation/2, small_hole_offset)]
result = result.faces(">Z").workplane().pushPoints(small_holes).hole(small_hole_dia)

# 'result' now holds the final solid
result