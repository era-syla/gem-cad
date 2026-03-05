import cadquery as cq
import math

# Parameters
block_x = 100
block_y = 50
block_z = 30

# Top small holes with countersinks
top_hole_centers = [(-30, 0), (0, 0), (30, 0)]
countersink_dia = 16
countersink_depth = 2
top_hole_dia = 8

# Circular boss on top
boss_center = (30, 0)
boss_rad = 20
boss_h = 5
boss_hole_dia = 8
boss_hole_rad = 15
small_hole_dia = 4
small_hole_rad = 10

# Side bosses
side_boss_positions = [(-20, 0), (20, 0)]
side_boss_size = 12
side_boss_h = 5
side_boss_hole_dia = 8

# Rectangular recess on one side
recess_size = (30, 8)
recess_depth = 3

# Start with main block
result = cq.Workplane("XY").box(block_x, block_y, block_z)

# Top countersunk holes
top = result.faces(">Z").workplane()
top = top.pushPoints(top_hole_centers)
top = top.circle(countersink_dia/2).cutBlind(-countersink_depth)
top = top.workplane(offset=-countersink_depth).circle(top_hole_dia/2).cutBlind(-block_z)

# Circular boss
result = result.faces(">Z").workplane().pushPoints([boss_center]).circle(boss_rad).extrude(boss_h)

# Holes around boss
angles = [0, 90, 180, 270]
pts = [(boss_center[0] + boss_hole_rad*math.cos(math.radians(a)),
        boss_center[1] + boss_hole_rad*math.sin(math.radians(a)))
       for a in angles]
result = result.faces(">Z").workplane().pushPoints(pts).circle(boss_hole_dia/2).cutBlind(boss_h + block_z)
# Small holes
pts2 = [(boss_center[0] + small_hole_rad*math.cos(math.radians(a)),
         boss_center[1] + small_hole_rad*math.sin(math.radians(a)))
        for a in angles]
result = result.faces(">Z").workplane().pushPoints(pts2).circle(small_hole_dia/2).cutBlind(boss_h + block_z)

# Side bosses with holes on +Y and -Y faces
for face in ["<Y", ">Y"]:
    wp = result.faces(face).workplane()
    wp = wp.pushPoints(side_boss_positions)
    wp = wp.rect(side_boss_size, side_boss_size).extrude(side_boss_h)
    # holes through side bosses
    wp2 = result.faces(face).workplane().pushPoints(side_boss_positions)
    result = wp2.circle(side_boss_hole_dia/2).cutThruAll()

# Rectangular recess on -Y face
result = result.faces("<Y").workplane().center(15, 0).rect(recess_size[0], recess_size[1]).cutBlind(recess_depth)

# Chamfer all vertical edges
result = result.edges("|Z").chamfer(1)

# Final result
# Assign to variable 'result'
pass
