import cadquery as cq

# Parametric dimensions
height = 100.0      # Overall height
width = 60.0        # Overall width
thickness = 2.0     # Material thickness

# Features
slot_width = 15.0
slot_depth = 15.0
slot_x_offset = 10.0 # From left edge

taper_start_y = 60.0 # Height where the taper starts on the right side
taper_width = 25.0   # Width of the tapered section

# Create the main profile
# We will draw this on the XY plane and extrude it
# The shape is roughly rectangular with a cutout at the top and a taper on the right

# Define points for the profile
# Bottom-left corner is at (0,0)
p1 = (0, 0)
p2 = (width, 0)
p3 = (width, taper_start_y)
p4 = (width - taper_width, height) # Top right corner of main block after taper
# Note: Looking at the image, there seems to be a distinct rectangular section on the left
# and a triangular/trapezoidal wing on the right.
# Let's refine the points based on the "L" shape + wing structure.

# Let's assume a simpler construction: a rectangle with a notch, plus a wing.
# Left main body width
main_body_width = width - taper_width

result = (
    cq.Workplane("XY")
    .lineTo(main_body_width, 0)      # Bottom edge of main body
    .lineTo(width, 0)                # Bottom edge of wing
    .lineTo(width, taper_start_y)    # Vertical right edge of wing
    .lineTo(main_body_width, height) # Angled top edge of wing connecting to main body top
    .lineTo(0, height)               # Top edge of main body
    .close()
    .extrude(thickness)
)

# Create the notch at the top
notch = (
    cq.Workplane("XY")
    .rect(slot_width, slot_depth * 2) # Create a rectangle larger than needed in Y
    .extrude(thickness)
    .translate((slot_x_offset + slot_width/2, height, thickness/2)) # Position it
)

# Cut the notch from the main body
# Since coordinates in rect are centered, we need to be careful with positioning.
# Alternative: sketch the profile directly with the notch.

# Let's rebuild using a single sketch approach for cleanliness.
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(width, 0)                # Bottom edge
    .lineTo(width, taper_start_y)    # Right vertical edge
    .lineTo(main_body_width, height) # Angled edge
    # Top edge segment 1
    .lineTo(slot_x_offset + slot_width, height) 
    # Notch down
    .lineTo(slot_x_offset + slot_width, height - slot_depth)
    # Notch across
    .lineTo(slot_x_offset, height - slot_depth)
    # Notch up
    .lineTo(slot_x_offset, height)
    # Top edge segment 2
    .lineTo(0, height)
    # Left edge
    .close()
    .extrude(thickness)
)

# Rotate to match the isometric view in the image roughly (standing up)
result = result.rotate((0,0,0), (1,0,0), 90)