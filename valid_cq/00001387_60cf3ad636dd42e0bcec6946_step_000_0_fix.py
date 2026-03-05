import cadquery as cq
import math

# Gear parameters
num_teeth = 32
outer_radius = 40
root_radius = 33
pitch_radius = 36
hub_radius = 12
bore_radius = 7
thickness = 8
tooth_width = 3.5
tooth_height = outer_radius - root_radius

# Create the base gear disk
result = cq.Workplane("XY").cylinder(thickness, root_radius)

# Add teeth around the gear
tooth_pts = []
for i in range(num_teeth):
    angle = 2 * math.pi * i / num_teeth
    angle_deg = math.degrees(angle)
    
    # Create a single tooth as a box and rotate it
    half_w = tooth_width / 2
    tooth = (cq.Workplane("XY")
             .transformed(rotate=(0, 0, angle_deg))
             .transformed(offset=(root_radius + tooth_height/2, 0, 0))
             .box(tooth_height, tooth_width * 0.9, thickness))
    
    result = result.union(tooth)

# Cut the center bore
result = result.cut(
    cq.Workplane("XY").cylinder(thickness + 2, bore_radius)
)

# Add hub (raised cylinder around bore)
hub = cq.Workplane("XY").cylinder(thickness, hub_radius)
result = result.union(hub)

# Cut two small rectangular holes (keyway-style holes visible in image)
# These appear to be two rectangular cutouts symmetrically placed
hole_w = 4
hole_h = 5
hole_dist = 16

hole1 = (cq.Workplane("XY")
         .transformed(offset=(hole_dist/2, 0, 0))
         .box(hole_h, hole_w, thickness + 2))

hole2 = (cq.Workplane("XY")
         .transformed(offset=(-hole_dist/2, 0, 0))
         .box(hole_h, hole_w, thickness + 2))

result = result.cut(hole1).cut(hole2)

# Cut the bore again to ensure clean hole
result = result.cut(
    cq.Workplane("XY").cylinder(thickness + 2, bore_radius)
)