import cadquery as cq

# --- Parameter Definitions ---
# Overall plate dimensions
plate_width = 100.0  # Assumed width
plate_depth = 100.0  # Assumed depth (square)
plate_thickness = 2.0

# Mounting holes
hole_diameter = 5.0
hole_inset = 10.0  # Distance from edges to hole center

# Top surface component (small rectangular block)
comp_width = 10.0
comp_depth = 6.0
comp_height = 3.0
# Position relative to center. It looks offset towards one corner.
comp_offset_x = 0.0
comp_offset_y = -35.0 # Shifted towards the front edge

# Side cutout/notch feature
notch_depth = 1.5
notch_width = 15.0
notch_position_y = -30.0 # Position along the side edge

# --- Geometry Construction ---

# 1. Base Plate
base = cq.Workplane("XY").box(plate_width, plate_depth, plate_thickness)

# 2. Mounting Holes
# Create a list of (x, y) coordinates for the holes
x_pos = plate_width / 2 - hole_inset
y_pos = plate_depth / 2 - hole_inset
hole_locations = [
    (x_pos, y_pos),
    (x_pos, -y_pos),
    (-x_pos, y_pos),
    (-x_pos, -y_pos)
]

plate_with_holes = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .hole(hole_diameter)
)

# 3. Top Surface Component
# Located on the top face
component = (
    plate_with_holes.faces(">Z")
    .workplane()
    .center(comp_offset_x, comp_offset_y)
    .rect(comp_width, comp_depth)
    .extrude(comp_height)
)

# 4. Side Notch Feature
# Looking at the image, there is a small cutout or step on the left edge (negative X)
# We will create a cut on the -X face.
result = (
    component.faces("<X")
    .workplane(centerOption="CenterOfMass")
    .center(notch_position_y, 0) # Adjust Y position along the face
    .rect(notch_width, plate_thickness) # Cut the full thickness
    .cutBlind(notch_depth) # Cut into the plate
)

# If the side feature is actually an addition (a tab) rather than a cut, 
# the image is slightly ambiguous due to lighting, but it looks like a notch/relief.
# However, looking closely at the bottom left, it looks like a small depression 
# or a thinner section. Let's stick with the main plate + holes + top block as the primary features.

# Final Result
result = result