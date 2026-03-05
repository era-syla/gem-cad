import cadquery as cq

# Parametric dimensions
disk_diameter = 50.0   # Diameter of the main disk
disk_thickness = 5.0   # Thickness of the disk
hole_diameter = 2.0    # Diameter of the center hole

# Create the disk
# 1. Start with a workplane (XY plane)
# 2. Draw a circle for the disk
# 3. Extrude it to create the solid cylinder
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .extrude(disk_thickness)
)

# Create the center hole
# 1. Select the top face of the disk
# 2. Draw a circle for the hole
# 3. Cut through the entire object
result = (
    result.faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# Alternative concise one-liner approach:
# result = cq.Workplane("XY").circle(disk_diameter/2).extrude(disk_thickness).faces(">Z").workplane().hole(hole_diameter)