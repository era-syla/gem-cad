import cadquery as cq
import math

# Parameters
gear_outer_radius = 45
gear_inner_radius = 35
gear_thickness = 8
num_teeth = 28
tooth_height = 8
tooth_width_angle = 2 * math.pi / num_teeth

hub_size = 28
hub_height = 12
hub_hole_radius = 8

shaft_radius = 4
shaft_height = 35

small_hole_radius = 2.5
small_hole_offset = 10

# Create the gear disk base
gear = cq.Workplane("XY").cylinder(gear_thickness, gear_inner_radius)

# Add teeth around the perimeter
teeth_solid = cq.Workplane("XY")

tooth_pts = []
for i in range(num_teeth):
    angle = 2 * math.pi * i / num_teeth
    
    # Each tooth is a small trapezoid extruded outward
    angle_half = tooth_width_angle * 0.35
    
    # Inner points (at gear_inner_radius)
    x1_in = gear_inner_radius * math.cos(angle - angle_half)
    y1_in = gear_inner_radius * math.sin(angle - angle_half)
    x2_in = gear_inner_radius * math.cos(angle + angle_half)
    y2_in = gear_inner_radius * math.sin(angle + angle_half)
    
    # Outer points (at gear_outer_radius) - slightly narrower for pointed teeth
    angle_half_out = tooth_width_angle * 0.15
    x1_out = gear_outer_radius * math.cos(angle - angle_half_out)
    y1_out = gear_outer_radius * math.sin(angle - angle_half_out)
    x2_out = gear_outer_radius * math.cos(angle + angle_half_out)
    y2_out = gear_outer_radius * math.sin(angle + angle_half_out)
    
    # Create tooth as a box approximation using polygon vertices
    tooth_verts = [
        (x1_in, y1_in),
        (x2_in, y2_in),
        (x2_out, y2_out),
        (x1_out, y1_out),
    ]
    
    tooth = (cq.Workplane("XY")
             .polyline(tooth_verts)
             .close()
             .extrude(gear_thickness))
    
    gear = gear.union(tooth)

# Create square hub on top of gear
hub = (cq.Workplane("XY")
       .workplane(offset=gear_thickness)
       .rect(hub_size, hub_size)
       .extrude(hub_height))

gear = gear.union(hub)

# Cut center hole through hub
gear = (gear
        .faces(">Z")
        .workplane()
        .circle(hub_hole_radius)
        .cutThruAll())

# Add small holes in hub face (bolt holes)
gear = (gear
        .workplane(offset=gear_thickness + hub_height)
        .pushPoints([
            (small_hole_offset, 0),
            (-small_hole_offset, 0),
        ])
        .circle(small_hole_radius)
        .cutBlind(-hub_height))

# Add shaft on top
shaft = (cq.Workplane("XY")
         .workplane(offset=gear_thickness + hub_height)
         .circle(shaft_radius)
         .extrude(shaft_height))

gear = gear.union(shaft)

result = gear