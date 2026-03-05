import cadquery as cq
import math

# Parameters
outer_radius = 40
disk_thickness = 6
hole_radius = 5
num_teeth = 10
tooth_width = 6
tooth_height = 5
tooth_thickness = 4

# Create the main disk
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(disk_thickness)
)

# Add teeth around the perimeter
# Each tooth is a small rectangular protrusion on the outer edge
for i in range(num_teeth):
    angle = i * (360.0 / num_teeth)
    angle_rad = math.radians(angle)
    
    # Position of tooth center on the outer edge
    tx = outer_radius * math.cos(angle_rad)
    ty = outer_radius * math.sin(angle_rad)
    
    # Create a tooth as a box positioned at the edge
    tooth = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(tx, ty, 0), rotate=cq.Vector(0, 0, angle))
        .rect(tooth_height, tooth_width)
        .extrude(tooth_thickness)
        .translate((0, 0, (disk_thickness - tooth_thickness) / 2))
    )
    
    result = result.union(tooth)

# Cut center hole
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutThruAll()
)