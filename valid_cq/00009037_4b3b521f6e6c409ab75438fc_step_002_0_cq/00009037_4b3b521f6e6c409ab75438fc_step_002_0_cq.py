import cadquery as cq

# --- Parameters ---
length = 200.0      # Total length of the profile
width = 30.0        # Width of the horizontal flange
height = 30.0       # Height of the vertical flange
thickness = 3.0     # Thickness of the material
notch_width = 15.0  # Width of the cutout notch
notch_depth = 20.0  # Depth of the cutout notch from top edge
notch_offset = 10.0 # Distance of notch from the left end

# --- Modeling ---

# 1. Create the base L-profile
# We'll sketch the L-shape on the YZ plane and extrude it along X.
# Alternatively, sketch on XY and extrude Z? Let's do sketch on YZ (side profile) and extrude X (length).
# Profile points for an L-shape:
# (0,0) -> (width, 0) -> (width, thickness) -> (thickness, thickness) -> (thickness, height) -> (0, height) -> close

pts = [
    (0, 0),
    (width, 0),
    (width, thickness),
    (thickness, thickness),
    (thickness, height),
    (0, height)
]

# Create the main extrusion
base_profile = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# 2. Create the Notch
# The notch is on the vertical flange.
# Let's orient ourselves.
# YZ plane was the sketch plane. Extrusion was along X.
# So:
# X axis = Length
# Y axis = Width (horizontal flange)
# Z axis = Height (vertical flange)
#
# The vertical flange is at Y close to 0 (specifically from Y=0 to Y=thickness).
# We want to cut a rectangle out of this flange.
# The cut needs to be positioned along X (length).
#
# Let's select the face of the vertical flange.
# It is likely the face with normal -Y or +Y depending on sketch orientation.
# Based on points: (0,0) to (0, height) is on the Y=0 plane. (thickness, thickness) to (thickness, height) is on Y=thickness plane.
# Let's select the "back" face (closest to Y=0) or just cut through the whole object in that area.

# We'll create a box to subtract for the notch.
# Notch dimensions:
# - Length (along X): notch_width
# - Width (along Y): thickness * 2 (make it wider to ensure cut)
# - Height (along Z): notch_depth
# Position:
# - X: notch_offset from the start (or end). Let's assume from the start (X=0).
#   Center of notch would be at x = notch_offset + notch_width/2
# - Y: centered on the flange thickness
# - Z: At the top edge going down. Top is Z=height. Center of box would be height - notch_depth/2.

notch_center_x = notch_offset + notch_width / 2.0
notch_center_z = height - notch_depth / 2.0

# Using a simple cut operation with a box
# We need to orient the box correctly.
# Workplane("XY") is the ground plane.
# Let's create a solid box and cut it.

# Location of the notch box center relative to the origin of the extrusion
notch_location = cq.Location(
    cq.Vector(notch_center_x, 0, notch_center_z)
)

notch_solid = (
    cq.Workplane("XY")
    .box(notch_width, width * 2, notch_depth) # Make Y huge to cut through flange easily
    .val()
    .located(notch_location)
)

result = base_profile.cut(notch_solid)

# Export or display the result (for validation during thought process, omitted in final code)