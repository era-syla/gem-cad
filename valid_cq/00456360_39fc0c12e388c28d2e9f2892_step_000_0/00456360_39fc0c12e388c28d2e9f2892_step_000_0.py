import cadquery as cq

# Define parametric dimensions
disk_diameter = 60.0       # Outer diameter of the disk
disk_thickness = 8.0       # Thickness of the disk
hole_diameter = 6.0        # Diameter of the through hole
csk_diameter = 12.0        # Outer diameter of the countersink
csk_angle = 90.0           # Angle of the countersink in degrees

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .extrude(disk_thickness)
    .faces(">Z")
    .workplane()
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)