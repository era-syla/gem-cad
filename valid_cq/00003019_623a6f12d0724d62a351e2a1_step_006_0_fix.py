import cadquery as cq
import math

# Spool/reel dimensions
bottom_flange_radius = 60
bottom_flange_thickness = 6
top_flange_radius = 55
top_flange_thickness = 8
barrel_radius = 22
barrel_height = 45
total_height = bottom_flange_thickness + barrel_height + top_flange_thickness

# Build bottom flange
bottom_flange = (
    cq.Workplane("XY")
    .circle(bottom_flange_radius)
    .extrude(bottom_flange_thickness)
)

# Build barrel (cylinder connecting flanges)
barrel = (
    cq.Workplane("XY")
    .workplane(offset=bottom_flange_thickness)
    .circle(barrel_radius)
    .extrude(barrel_height)
)

# Build top flange
top_flange = (
    cq.Workplane("XY")
    .workplane(offset=bottom_flange_thickness + barrel_height)
    .circle(top_flange_radius)
    .extrude(top_flange_thickness)
)

# Combine all parts
spool = bottom_flange.union(barrel).union(top_flange)

# Add center hole through entire spool
center_hole_radius = 5
spool = (
    spool
    .faces(">Z")
    .workplane()
    .hole(center_hole_radius * 2)
)

# Add slots to top flange (rectangular cutouts near edge)
slot_length = 14
slot_width = 5
slot_depth = top_flange_thickness
slot_offset = top_flange_radius - 12

# Top flange slots - two slots on opposite sides
top_z = bottom_flange_thickness + barrel_height

spool = (
    spool
    .workplane(offset=top_z + top_flange_thickness)
    .pushPoints([(slot_offset, 0), (-slot_offset, 0)])
    .rect(slot_length, slot_width)
    .cutBlind(-slot_depth)
)

# Add slots to bottom flange
bottom_slot_offset = bottom_flange_radius - 12

spool = (
    spool
    .workplane(offset=bottom_flange_thickness)
    .pushPoints([(bottom_slot_offset, 0), (-bottom_slot_offset, 0)])
    .rect(slot_length, slot_width)
    .cutBlind(-bottom_flange_thickness)
)

# Add small holes on top flange face (visible in image)
small_hole_radius = 2.5
hole_pattern_radius = 20

# Two small holes on top flange
top_face_z = total_height

spool = (
    spool
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_pattern_radius * math.cos(math.radians(120)), hole_pattern_radius * math.sin(math.radians(120))),
        (hole_pattern_radius * math.cos(math.radians(240)), hole_pattern_radius * math.sin(math.radians(240))),
    ])
    .hole(small_hole_radius * 2, depth=4)
)

result = spool