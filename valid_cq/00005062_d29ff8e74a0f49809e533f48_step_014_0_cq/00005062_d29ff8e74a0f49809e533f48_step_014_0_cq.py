import cadquery as cq

# Parametric dimensions
length = 200.0          # Total length of the part
thick_end_height = 20.0 # Height at the thicker end
thin_end_height = 10.0  # Height at the thinner end
thickness = 5.0         # Thickness of the plate
fillet_radius = 2.0     # Fillet radius for the thin end corners

# Hole parameters
num_holes = 5           # Number of holes
hole_diameter = 6.0     # Diameter of the holes
hole_spacing = 15.0     # Distance between hole centers
first_hole_offset = 30.0 # Distance from the center of the bar to the first hole

# Create the main tapered shape
# We'll sketch on the XY plane and extrude
# The shape is a trapezoid
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(length, 0)                  # Bottom edge
    .lineTo(length, thin_end_height)    # Thin end vertical edge
    .lineTo(0, thick_end_height)        # Top sloped edge
    .close()
    .extrude(thickness)
)

# Apply fillets to the thin end corners
# Selecting edges at the extreme X (length)
result = result.edges(f">X").fillet(fillet_radius)

# Create holes
# We need to calculate positions relative to the coordinate system
# The coordinate system origin (0,0,0) is at the bottom-left corner of the thick end.
# We will place holes along the centerline or biased towards the top edge based on the image.
# Looking at the image, the holes seem to follow the taper slope.

# Let's define a vector for the hole pattern direction
# Or simply place points individually.
# The holes are near the "middle" of the length.

# Let's adjust hole logic to match the visual reference better.
# The holes start around the middle and go towards the thin end.
hole_start_x = length * 0.45  # Starting X position approx halfway
hole_y_ratio = 0.6            # Height ratio relative to the local height

hole_centers = []
for i in range(num_holes):
    x_pos = hole_start_x + (i * hole_spacing)
    
    # Calculate local height at this x position for centering
    # Line equation: y = m*x + c
    # (0, thick_end_height) -> (length, thin_end_height)
    slope = (thin_end_height - thick_end_height) / length
    local_height = slope * x_pos + thick_end_height
    
    # Place hole at roughly half the local height, perhaps slightly higher visually
    y_pos = local_height * 0.5 
    
    hole_centers.append((x_pos, y_pos))

# Cut the holes
result = (
    result.faces(">Z")  # Select the top face (based on extrusion direction)
    .workplane()
    .pushPoints(hole_centers)
    .hole(hole_diameter)
)

# Center the part for better viewing if desired, but not strictly necessary.
# The current origin is at the bottom corner of the thick end.