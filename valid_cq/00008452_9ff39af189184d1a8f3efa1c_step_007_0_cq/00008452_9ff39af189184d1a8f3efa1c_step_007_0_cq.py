import cadquery as cq

# Parametric dimensions
plate_length = 100.0  # Dimension along the X-axis
plate_width = 100.0   # Dimension along the Y-axis
plate_thickness = 2.0 # Thickness of the plate

# Create the solid plate
# We use Workplane("XY") to start drawing on the XY plane.
# box() automatically centers the object at the origin by default,
# which matches the isometric view perspective usually centering the object.
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# If centering is not desired, the alternative would be:
# result = cq.Workplane("XY").rect(plate_length, plate_width).extrude(plate_thickness)