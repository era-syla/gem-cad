import cadquery as cq

# Parametric dimensions
plate_width = 100.0  # Total width of the plate
plate_height = 40.0  # Total height of the plate
plate_thickness = 5.0 # Thickness of the plate

hole_width = 40.0    # Width of the rectangular cutout
hole_height = 20.0   # Height of the rectangular cutout

# Create the main plate
# Workplane("XY") creates a 2D drawing surface on the XY plane
# box() creates the base rectangular solid centered at the origin
# rect() creates the profile for the cutout
# cutThruAll() subtracts the rectangular profile from the solid
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_height, plate_thickness)
    .faces(">Z")
    .workplane()
    .rect(hole_width, hole_height)
    .cutThruAll()
)

# Alternatively, using a 2D sketch approach which is often cleaner for flat plates:
# result = (
#     cq.Workplane("XY")
#     .rect(plate_width, plate_height)
#     .rect(hole_width, hole_height)
#     .extrude(plate_thickness)
# )

# The result variable is required for display in CQ-Editor