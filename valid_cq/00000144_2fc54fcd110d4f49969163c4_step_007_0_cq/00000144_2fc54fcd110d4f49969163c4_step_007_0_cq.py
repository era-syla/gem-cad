import cadquery as cq

# Parametric dimensions
disk_diameter = 50.0   # Main diameter of the disk
disk_thickness = 15.0  # Thickness of the disk
hole_diameter = 10.0   # Diameter of the two through-holes
hole_spacing = 30.0    # Distance between the centers of the holes (center-to-center)

# Calculate hole offset from center
hole_offset = hole_spacing / 2.0

# Create the main disk
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .extrude(disk_thickness)
    .faces(">Z")
    .workplane()
    # Create the two holes using pushPoints to position them
    .pushPoints([(-hole_offset, 0), (hole_offset, 0)])
    .hole(hole_diameter)
)