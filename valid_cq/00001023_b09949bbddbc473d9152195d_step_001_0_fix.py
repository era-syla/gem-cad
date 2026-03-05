import cadquery as cq
import math

# Parameters
outer_radius = 30
inner_radius = 15
height = 30
num_teeth = 16
tooth_radius = 4.5
tooth_center_radius = outer_radius - 1  # center of tooth cylinders

# Create the main cylindrical body
body = cq.Workplane("XY").cylinder(height, outer_radius)

# Create the central hole
body = body.faces(">Z").workplane().circle(inner_radius).cutThruAll()

# Create gear teeth by adding cylinders around the perimeter
# Each tooth is a cylinder placed at the outer edge
teeth = cq.Workplane("XY")

for i in range(num_teeth):
    angle = 2 * math.pi * i / num_teeth
    x = tooth_center_radius * math.cos(angle)
    y = tooth_center_radius * math.sin(angle)
    
    tooth = cq.Workplane("XY").center(x, y).cylinder(height, tooth_radius)
    
    if i == 0:
        teeth = tooth
    else:
        teeth = teeth.union(tooth)

# Union body with teeth
result = body.union(teeth)

# Add rim/flange on the inner side - the image shows a slight inner rim
# Create inner ring slightly larger than hole
inner_ring = cq.Workplane("XY").cylinder(height * 0.15, inner_radius + 3).faces(">Z").workplane().circle(inner_radius).cutThruAll()

# The image shows flanges/lips at top and bottom of the inner bore
# Add top flange ring
top_flange = cq.Workplane("XY").workplane(offset=height/2 - 2).circle(inner_radius + 5).circle(inner_radius).extrude(2)
bot_flange = cq.Workplane("XY").workplane(offset=-height/2).circle(inner_radius + 5).circle(inner_radius).extrude(2)

result = result.union(top_flange).union(bot_flange)