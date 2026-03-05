import cadquery as cq
import math

# Timing pulley parameters
num_teeth = 20
tooth_height = 1.5
tooth_width = 2.0
belt_width = 10.0
pulley_radius = 15.0  # pitch radius
flange_radius = 20.0
flange_thickness = 2.0
hub_radius = 6.0
hub_height = 8.0
bore_radius = 3.5
total_height = belt_width + 2 * flange_thickness

# Build the main pulley body (cylinder)
result = cq.Workplane("XY").cylinder(belt_width, pulley_radius)

# Add teeth around the pulley
tooth_angle = 360.0 / num_teeth
for i in range(num_teeth):
    angle = i * tooth_angle
    angle_rad = math.radians(angle)
    
    # Position of tooth center on the surface
    tx = pulley_radius * math.cos(angle_rad)
    ty = pulley_radius * math.sin(angle_rad)
    
    # Create a tooth as a small box and union it
    tooth = (
        cq.Workplane("XY")
        .transformed(offset=(tx, ty, 0), rotate=(0, 0, math.degrees(angle_rad)))
        .box(tooth_height * 2, tooth_width * 0.8, belt_width, centered=True)
    )
    result = result.union(tooth)

# Add top flange
top_flange = cq.Workplane("XY").workplane(offset=belt_width / 2).circle(flange_radius).extrude(flange_thickness)
result = result.union(top_flange)

# Add bottom flange
bottom_flange = cq.Workplane("XY").workplane(offset=-belt_width / 2 - flange_thickness).circle(flange_radius).extrude(flange_thickness)
result = result.union(bottom_flange)

# Add hub on top
hub = cq.Workplane("XY").workplane(offset=belt_width / 2 + flange_thickness).circle(hub_radius).extrude(hub_height)
result = result.union(hub)

# Add small bottom hub/stem
bottom_hub_height = 4.0
bottom_hub = cq.Workplane("XY").workplane(offset=-belt_width / 2 - flange_thickness - bottom_hub_height).circle(hub_radius).extrude(bottom_hub_height)
result = result.union(bottom_hub)

# Cut bore through entire assembly
bore_depth = belt_width / 2 + flange_thickness + hub_height + bottom_hub_height + belt_width / 2
bore = cq.Workplane("XY").workplane(offset=-(belt_width / 2 + flange_thickness + bottom_hub_height)).circle(bore_radius).extrude(bore_depth + 2)
result = result.cut(bore)

# Cut tooth slots around the pulley to create actual teeth profile
slot_depth = tooth_height
slot_width = tooth_width * 0.9
for i in range(num_teeth):
    angle = (i + 0.5) * tooth_angle  # offset by half tooth to cut between teeth
    angle_rad = math.radians(angle)
    
    tx = (pulley_radius + 0.5) * math.cos(angle_rad)
    ty = (pulley_radius + 0.5) * math.sin(angle_rad)
    
    slot = (
        cq.Workplane("XY")
        .transformed(offset=(tx, ty, 0), rotate=(0, 0, math.degrees(angle_rad)))
        .box(slot_depth * 2 + 1, slot_width, belt_width + 0.2, centered=True)
    )
    result = result.cut(slot)