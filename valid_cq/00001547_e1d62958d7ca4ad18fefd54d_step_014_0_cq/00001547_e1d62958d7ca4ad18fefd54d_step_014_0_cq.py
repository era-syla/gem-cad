import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the object
width = 100.0   # Total width (X-axis)
depth = 60.0    # Total depth (Y-axis)
height = 50.0   # Total height (Z-axis)

# Wall thickness
thickness = 5.0

# --- Modeling Strategy ---
# 1. Start with a solid block representing the outer bounds.
# 2. Shell the object by removing specific faces (front and bottom).
#    Alternatively, and simpler for this geometry:
#    Create a box and cut out a smaller box from the bottom-front.

# --- CadQuery Construction ---

# Step 1: Create the main solid block
outer_box = cq.Workplane("XY").box(width, depth, height)

# Step 2: Create the cutout shape
# The cutout needs to be smaller by the thickness on the sides (Left, Right, Top, Back).
# We want to cut through the Front and Bottom.
cutout_width = width - (2 * thickness)
cutout_depth = depth - thickness  # Keep back wall
cutout_height = height - thickness # Keep top wall

# Position the cutout:
# It should be centered in X.
# It should be offset towards the front in Y (leaving the back wall).
# It should be offset towards the bottom in Z (leaving the top wall).

# Create the cutting tool
cutout = (cq.Workplane("XY")
          .box(cutout_width, cutout_depth, cutout_height)
          .translate((0, -thickness/2, -thickness/2)))

# Step 3: Perform the cut
result = outer_box.cut(cutout)

# Note: The translate logic works like this:
# The main box is centered at (0,0,0).
# The cutout box is created at (0,0,0).
# To leave a back wall (positive Y direction relative to center in standard view), 
# we shift the cutout slightly towards negative Y (front).
# To leave a top wall (positive Z direction), we shift the cutout slightly 
# towards negative Z (bottom).