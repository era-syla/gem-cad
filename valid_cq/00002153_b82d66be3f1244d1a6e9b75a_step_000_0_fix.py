import cadquery as cq

# Parameters
outer_radius = 50
inner_radius = 44
height = 20
wall_thickness = outer_radius - inner_radius
floor_thickness = 3

# Slot parameters
slot_width = 8
slot_depth = 15  # how deep into the wall the slot goes (radially)
slot_height = height  # full height slot (open top)

# Boss/post parameters
boss_outer_radius = 4
boss_inner_radius = 1.5
boss_height = 12
boss_pattern_radius = 36  # radial distance from center

# Create the outer cylindrical shell
outer_cyl = cq.Workplane("XY").circle(outer_radius).extrude(height)

# Create inner cutout (hollow the inside, leaving floor)
inner_cut = cq.Workplane("XY").workplane(offset=floor_thickness).circle(inner_radius).extrude(height)

result = outer_cyl.cut(inner_cut)

# Add two slots on opposite sides (notches in the wall from top)
# Slot 1 at 0 degrees
slot1 = (cq.Workplane("XY")
         .workplane(offset=0)
         .transformed(offset=(outer_radius - slot_depth/2, 0, 0))
         .rect(slot_depth + 4, slot_width)
         .extrude(height))

# Slot 2 at 180 degrees
slot2 = (cq.Workplane("XY")
         .workplane(offset=0)
         .transformed(offset=(-(outer_radius - slot_depth/2), 0, 0))
         .rect(slot_depth + 4, slot_width)
         .extrude(height))

result = result.cut(slot1).cut(slot2)

# Add 4 mounting bosses (hollow posts) on the floor
# Positions at 45, 135, 225, 315 degrees
import math

boss_positions = [
    (boss_pattern_radius * math.cos(math.radians(45)),
     boss_pattern_radius * math.sin(math.radians(45))),
    (boss_pattern_radius * math.cos(math.radians(135)),
     boss_pattern_radius * math.sin(math.radians(135))),
    (boss_pattern_radius * math.cos(math.radians(225)),
     boss_pattern_radius * math.sin(math.radians(225))),
    (boss_pattern_radius * math.cos(math.radians(315)),
     boss_pattern_radius * math.sin(math.radians(315))),
]

for (bx, by) in boss_positions:
    # Outer boss cylinder
    boss_outer = (cq.Workplane("XY")
                  .workplane(offset=floor_thickness)
                  .transformed(offset=(bx, by, 0))
                  .circle(boss_outer_radius)
                  .extrude(boss_height))
    
    # Inner hole in boss
    boss_inner = (cq.Workplane("XY")
                  .workplane(offset=floor_thickness)
                  .transformed(offset=(bx, by, 0))
                  .circle(boss_inner_radius)
                  .extrude(boss_height))
    
    result = result.union(boss_outer).cut(boss_inner)

# Add small screw holes in the floor (countersink style)
screw_hole_radius = 1.5
screw_positions = [
    (boss_pattern_radius * math.cos(math.radians(45)),
     boss_pattern_radius * math.sin(math.radians(45))),
    (boss_pattern_radius * math.cos(math.radians(135)),
     boss_pattern_radius * math.sin(math.radians(135))),
    (boss_pattern_radius * math.cos(math.radians(225)),
     boss_pattern_radius * math.sin(math.radians(225))),
    (boss_pattern_radius * math.cos(math.radians(315)),
     boss_pattern_radius * math.sin(math.radians(315))),
]

for (sx, sy) in screw_positions:
    hole = (cq.Workplane("XY")
            .transformed(offset=(sx, sy, 0))
            .circle(screw_hole_radius)
            .extrude(floor_thickness))
    result = result.cut(hole)