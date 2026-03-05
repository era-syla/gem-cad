import cadquery as cq
import math

# Main hub assembly - wheel hub with gear ring

# Base flange disc
base = cq.Workplane("XY").circle(45).extrude(8)

# Gear ring on the bottom of the flange
num_teeth = 48
gear_outer = 45
gear_inner = 38
tooth_height = 4
tooth_width = math.pi * 2 * gear_outer / num_teeth * 0.4

gear_ring = cq.Workplane("XY").circle(gear_outer).circle(gear_inner).extrude(-6)

# Add teeth to gear ring
teeth_assembly = cq.Workplane("XY")
for i in range(num_teeth):
    angle = i * 360.0 / num_teeth
    rad = math.radians(angle)
    x = (gear_outer + tooth_height/2) * math.cos(rad)
    y = (gear_outer + tooth_height/2) * math.sin(rad)
    tooth = (cq.Workplane("XY")
             .transformed(offset=(x, y, 0), rotate=(0, 0, math.degrees(rad)))
             .box(tooth_height, tooth_width, 6))
    teeth_assembly = teeth_assembly.union(tooth)

gear_assembly = gear_ring.union(teeth_assembly)

# Main hub cylinder
hub_outer = cq.Workplane("XY").circle(22).extrude(35)
hub_inner = cq.Workplane("XY").circle(14).extrude(35)
hub_cylinder = hub_outer.cut(hub_inner)

# Inner bearing seat
bearing_outer = cq.Workplane("XY").workplane(offset=8).circle(18).extrude(20)
bearing_inner = cq.Workplane("XY").workplane(offset=8).circle(14).extrude(20)
bearing_seat = bearing_outer.cut(bearing_inner)

# Combine base elements
result = base.union(gear_assembly).union(hub_cylinder)

# Cut center bore through everything
center_bore = cq.Workplane("XY").workplane(offset=-6).circle(13).extrude(50)
result = result.cut(center_bore)

# Add mounting studs/pins on top of flange
stud_positions = [(28, 0), (0, 28), (-28, 0)]
for pos in stud_positions:
    stud = (cq.Workplane("XY")
            .workplane(offset=8)
            .transformed(offset=(pos[0], pos[1], 0))
            .circle(4)
            .extrude(30))
    result = result.union(stud)

# Add bolt holes in flange
bolt_hole_positions = [(32, 0, 0), (0, 32, 0), (-32, 0, 0), (0, -32, 0)]
for pos in bolt_hole_positions:
    hole = (cq.Workplane("XY")
            .transformed(offset=(pos[0], pos[1], 0))
            .circle(3.5)
            .extrude(8))
    result = result.cut(hole)

# Add rectangular tabs/brackets on the side
tab_angles = [90, 270]
for angle in tab_angles:
    rad = math.radians(angle)
    x = 42 * math.cos(rad)
    y = 42 * math.sin(rad)
    tab = (cq.Workplane("XY")
           .workplane(offset=2)
           .transformed(offset=(x, y, 0))
           .rect(8, 14)
           .extrude(28))
    result = result.union(tab)

# Add slots/cutouts in hub collar area
slot_angles = [45, 135, 225, 315]
for angle in slot_angles:
    rad = math.radians(angle)
    x = 17 * math.cos(rad)
    y = 17 * math.sin(rad)
    slot = (cq.Workplane("XY")
            .workplane(offset=10)
            .transformed(offset=(x, y, 0))
            .rect(6, 6)
            .extrude(15))
    result = result.cut(slot)

# Inner step/shoulder inside hub
shoulder = (cq.Workplane("XY")
            .workplane(offset=20)
            .circle(16)
            .circle(13)
            .extrude(3))
result = result.union(shoulder)