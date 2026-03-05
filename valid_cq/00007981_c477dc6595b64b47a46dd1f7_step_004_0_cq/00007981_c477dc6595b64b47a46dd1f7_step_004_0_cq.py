import cadquery as cq

# Parametric dimensions
tube_outer_radius = 20.0
tube_wall_thickness = 2.0
tube_height = 80.0

plate_length = 60.0  # Length across the top
plate_width = 15.0   # Width of the rectangular strip
plate_thickness = 4.0 # Thickness of the plate

# Derived dimensions
tube_inner_radius = tube_outer_radius - tube_wall_thickness

# 1. Create the main cylindrical tube
# Create a solid cylinder
tube = cq.Workplane("XY").circle(tube_outer_radius).extrude(tube_height)

# Hollow it out to create a tube
# We cut a cylinder from the center
tube = tube.faces("<Z").workplane().circle(tube_inner_radius).cutThruAll()

# 2. Create the rectangular plate at the top
# We start a sketch on the top face of the tube (at Z = tube_height)
# The plate is centered on the tube's axis
plate = (
    cq.Workplane("XY")
    .workplane(offset=tube_height)
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# 3. Combine the parts
result = tube.union(plate)

# Optional: Export or display the result (standard practice for verification)
# cq.exporters.export(result, "model.step")