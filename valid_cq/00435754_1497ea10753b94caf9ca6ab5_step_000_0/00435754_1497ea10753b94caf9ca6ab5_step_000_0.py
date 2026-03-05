import cadquery as cq

# -- Parametric Dimensions --
# Estimated dimensions based on the visual proportions of the image
disk_diameter = 100.0   # Outer diameter of the disk
disk_thickness = 2.0    # Thickness of the disk
hole_diameter = 5.0     # Diameter of the central hole

# -- Geometry Generation --
# Create a workplane on the XY plane
# Draw the outer circle
# Draw the inner circle (which acts as a hole when extruded together)
# Extrude to create the solid 3D shape
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .circle(hole_diameter / 2.0)
    .extrude(disk_thickness)
)