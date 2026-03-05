import cadquery as cq
import math

# Parameters
outer_diameter = 70.0
thickness = 5.0
center_hole_diameter = 20.0
mount_hole_diameter = 6.0
mount_hole_radius = 25.0
mount_hole_angles = [0, 120, 240]

# Build the part
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
    # Create the center hole
    .faces(">Z")
    .workplane()
    .circle(center_hole_diameter / 2)
    .cutThruAll()
    # Create the three mounting holes
    .faces(">Z")
    .workplane()
    .pushPoints([
        (
            mount_hole_radius * math.cos(math.radians(angle)),
            mount_hole_radius * math.sin(math.radians(angle))
        )
        for angle in mount_hole_angles
    ])
    .circle(mount_hole_diameter / 2)
    .cutThruAll()
)
