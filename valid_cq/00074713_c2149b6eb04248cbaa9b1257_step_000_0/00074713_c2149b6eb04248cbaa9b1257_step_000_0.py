import cadquery as cq

# Parametric dimensions based on the visual estimation of the image
length = 40.0          # Total length of the part
width = 20.0           # Width (extrusion depth)
height_left = 18.0     # Height at the tall end (left side)
height_right = 10.0    # Height at the short end (right side)
notch_length = 20.0    # Length of the cutout on the bottom right
notch_height = 6.0     # Height of the cutout on the bottom right
curve_bulge = 2.0      # Amount the top arc bulges above a straight line

# Generate the geometry
# We sketch the profile on the XZ plane (front view) and extrude along Y (width)
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, height_left)  # Left vertical edge
    .threePointArc(
        (length / 2.0, (height_left + height_right) / 2.0 + curve_bulge),  # Midpoint of the arc
        (length, height_right)   # End point of the arc (top right corner)
    )
    .lineTo(length, notch_height)              # Right vertical edge down to the notch
    .lineTo(length - notch_length, notch_height) # Horizontal step of the notch
    .lineTo(length - notch_length, 0)          # Vertical step of the notch
    .close()                                   # Closes the bottom edge back to (0,0)
    .extrude(width)
)