import cadquery as cq

# Parameters
height = 50.0
width = 1.0
thickness = 0.2
num_notches = 20
notch_height = 0.5
notch_width = 0.6
margin = 1.0

# Create base strip
base = cq.Workplane("XY").box(width, thickness, height)

# Calculate notch spacing
usable_height = height - 2 * margin
spacing = usable_height / (num_notches - 1)

# Generate points for the notches along the height
pts = [(0, -height/2.0 + margin + i * spacing) for i in range(num_notches)]

# Cut notches through the strip
result = (
    base.faces(">Y")
    .workplane()
    .pushPoints(pts)
    .rect(notch_width, notch_height)
    .cutThruAll()
)