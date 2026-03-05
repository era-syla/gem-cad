import cadquery as cq

# Parametric dimensions
plate_length = 100.0  # Length of the plate (X axis)
plate_width = 75.0    # Width of the plate (Y axis)
plate_thickness = 5.0 # Thickness of the plate (Z axis)

hole_diameter = 6.0   # Diameter of the through holes
csk_diameter = 12.0   # Diameter of the countersink top
csk_angle = 90.0      # Countersink angle in degrees
hole_spacing = 60.0   # Distance between the two holes

# Create the base plate
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Create the countersunk holes
# We select the top face, then locate points relative to the center.
# The holes are aligned along the long axis (X) in the image, but let's check.
# Looking at the image, the long edge is likely X. The holes are centered on the Y-axis (width),
# and spaced apart along the X-axis (length).
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([(hole_spacing / 2, 0), (-hole_spacing / 2, 0)])
    .cskHole(hole_diameter, csk_diameter, csk_angle)
)