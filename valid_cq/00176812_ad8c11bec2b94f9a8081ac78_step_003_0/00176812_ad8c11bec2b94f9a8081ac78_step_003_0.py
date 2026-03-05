import cadquery as cq

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
# Dimensions estimated from the visual aspect ratio of the image
plate_length = 300.0  # Length along the X axis
plate_width = 200.0   # Width along the Y axis
plate_thickness = 15.0 # Thickness along the Z axis

# -----------------------------------------------------------------------------
# Geometry Generation
# -----------------------------------------------------------------------------
# Create a solid rectangular block (box) centered on the XY plane.
# This represents the base plate geometry shown in the image.
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)