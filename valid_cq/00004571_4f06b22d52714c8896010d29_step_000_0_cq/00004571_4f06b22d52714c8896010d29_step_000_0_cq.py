import cadquery as cq

# Parametric dimensions
length = 100.0   # Total length of the channel
width = 40.0     # Outer width of the base
height = 20.0    # Outer height of the flanges
thickness = 2.0  # Material thickness

# Create the profile
# We will draw the U-shape profile on the YZ plane and extrude it along the X axis
# Or draw on XY plane and extrude Z. Let's do XY plane for the cross-section and extrude Z for length.
# Wait, standard convention is often length along X or Y. Let's stick to X for length.
# So profile is on YZ plane.

# Define points for the outer U-shape
# Centering the base on the Y-axis makes sense for symmetry.

# Points approach:
# (width/2, height) -> (width/2, 0) -> (-width/2, 0) -> (-width/2, height)
# Then offset or draw the inner line to create thickness.

# Alternatively, just create a solid block and shell it or cut it.
# Drawing the sketch is usually cleaner for profiles.

# Let's draw the profile on the Front plane (XZ usually in some conventions, but let's just pick a workplane).
# Let's align length with Y axis, width with X, height with Z.
# Profile plane: XZ plane.

def u_channel(length, width, height, thickness):
    # Calculate inner dimensions
    inner_width = width - (2 * thickness)
    inner_height = height - thickness
    
    # We will sketch the cross section on the XZ plane centered at origin
    result = (
        cq.Workplane("XZ")
        .moveTo(-width / 2, height)
        .lineTo(-width / 2, 0)
        .lineTo(width / 2, 0)
        .lineTo(width / 2, height)
        .lineTo(width / 2 - thickness, height)
        .lineTo(width / 2 - thickness, thickness)
        .lineTo(-width / 2 + thickness, thickness)
        .lineTo(-width / 2 + thickness, height)
        .close()
        .extrude(length)
    )
    return result

# Generate the model
result = u_channel(length, width, height, thickness)