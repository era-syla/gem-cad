import cadquery as cq

# Parametric definitions
length = 300.0       # Total length of the bar
width = 15.0         # Width of the main bar
thickness = 3.0      # Thickness of the material
hook_length = 8.0    # Length of the hook features at the ends
hook_width = 5.0     # Width of the hook neck
fillet_radius = 1.0  # Radius for edge fillets

# Create the main profile
# We will draw the 2D profile of the bar and then extrude it.
# The profile looks like a long rectangle with L-shaped notches at both ends.

# Define the points for one half of the shape (symmetry makes it easier, but direct plotting is fine for this simple shape)
# Let's draw the full outline counter-clockwise starting from bottom-left corner
# (assuming the bar runs along X, width along Y)

# Calculate key coordinates
x_total = length
y_total = width
y_notch_depth = width - hook_width
x_notch_length = hook_length

# Create the sketch
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(length, 0)                  # Bottom edge
    .lineTo(length, hook_width)         # Right side up to notch
    .lineTo(length - x_notch_length, hook_width) # Right notch horizontal
    .lineTo(length - x_notch_length, width)      # Right notch vertical up to top
    .lineTo(x_notch_length, width)      # Top edge across to left notch
    .lineTo(x_notch_length, hook_width) # Left notch vertical down
    .lineTo(0, hook_width)              # Left notch horizontal out
    .close()
    .extrude(thickness)
)

# Apply fillets to all vertical edges for a realistic manufactured look
result = result.edges("|Z").fillet(fillet_radius)

# Optional: Fillet the top and bottom faces slightly as well for a finished look
# result = result.edges("not |Z").fillet(fillet_radius / 2.0)