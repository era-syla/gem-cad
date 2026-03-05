import cadquery as cq

# --- Parametric Dimensions ---
length = 100.0   # Length of the beam
width = 25.0     # Outer width (flange width)
height = 15.0    # Outer depth/height (web height)
thickness = 3.0  # Wall thickness

# --- Modeling Strategy ---
# We will create a 2D U-profile sketch and extrude it.
# The profile consists of a rectangle with another rectangle cut out from it,
# or drawn explicitly using points/lines.
# Here, we will draw the profile centered on the web.

# Define the points for the U-channel profile
# Let's orient it so the "back" of the C is along the Y-axis,
# and the flanges extend along the X-axis.

# Coordinates calculations
# Assuming origin is at the bottom-left corner of the outer envelope in the sketch plane
pts = [
    (0, 0),                 # Bottom-left outer corner
    (width, 0),             # Bottom-right outer corner
    (width, thickness),     # Bottom-right inner corner (flange tip)
    (thickness, thickness), # Inner corner bottom
    (thickness, height - thickness), # Inner corner top
    (width, height - thickness),     # Top-right inner corner (flange tip)
    (width, height),        # Top-right outer corner
    (0, height)             # Top-left outer corner
]

# --- Geometry Construction ---
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(length)
)

# Optional: Fillets can be added to make it look more realistic (like rolled steel)
# but the prompt image looks quite sharp.
# result = result.edges("|Z").fillet(0.5) 

# Export or display is handled by the caller, variable 'result' is required.