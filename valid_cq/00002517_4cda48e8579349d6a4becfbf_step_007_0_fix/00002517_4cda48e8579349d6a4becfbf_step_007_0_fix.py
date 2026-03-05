import cadquery as cq

# Parameters
length, width, height = 100, 70, 15
wall_thickness, pocket_depth = 3, 7
outer_fillet = 3
boss_dia, boss_height, hole_dia = 8, 3, 4
rib_width, rib_height = 4, 2

inner_length = length - 2*wall_thickness
inner_width = width - 2*wall_thickness
rib_length = inner_length - 10

# Build the main box with rounded vertical edges
result = cq.Workplane("XY").box(length, width, height)
result = result.edges("|Z").fillet(outer_fillet)

# Cut out the interior pocket
result = result.faces(">Z").workplane().rect(inner_length, inner_width).cutBlind(-pocket_depth)

# Add the internal rib on the pocket floor
result = (
    result.faces(">Z")
          .workplane(offset=-pocket_depth)
          .center(0, inner_width/2 - wall_thickness - rib_width/2 - 2)
          .rect(rib_length, rib_width)
          .extrude(rib_height)
)

# Add corner bosses for screws
boss_offset = inner_length/2 - wall_thickness
boss_points = [
    ( boss_offset,  boss_offset),
    (-boss_offset,  boss_offset),
    (-boss_offset, -boss_offset),
    ( boss_offset, -boss_offset),
]
result = (
    result.faces(">Z")
          .workplane()
          .pushPoints(boss_points)
          .circle(boss_dia/2)
          .extrude(boss_height)
)

# Drill screw holes through the bosses
result = (
    result.faces(">Z")
          .workplane()
          .pushPoints(boss_points)
          .hole(hole_dia)
)