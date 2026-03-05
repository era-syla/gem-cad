import cadquery as cq

# Parametric dimensions
plate_length = 100.0
plate_width = 20.0
plate_thickness = 5.0

pin_diameter = 6.0
pin_length = 60.0
pin_spacing = 80.0  # Distance between pin centers

# Create the base plate
# We center it to make placing the pins easier
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Create the pins
# Calculate offset from center for the two pins
offset = pin_spacing / 2.0

# Select the top face of the plate to draw the circles for the pins
result = (
    plate
    .faces(">Z")
    .workplane()
    .pushPoints([(-offset, 0), (offset, 0)])
    .circle(pin_diameter / 2.0)
    .extrude(pin_length)
)