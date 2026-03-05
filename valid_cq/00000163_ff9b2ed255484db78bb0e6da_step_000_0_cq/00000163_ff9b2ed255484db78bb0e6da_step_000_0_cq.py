import cadquery as cq

# --- Parameter Definition ---
# These parameters control the dimensions of the model
radius = 50.0      # Outer radius of the top/bottom plates
total_height = 60.0 # Total height of the object
plate_thickness = 5.0 # Thickness of the top and bottom plates
neck_width = 15.0   # Width of the narrow vertical section in the middle
neck_height = 20.0  # Height of the vertical section

# Calculated parameters for the profile
taper_height = (total_height - (2 * plate_thickness) - neck_height) / 2

# --- Geometric Construction ---

# Strategy: Create a 2D profile on the XZ plane and revolve it 90 degrees around the Z axis.
# The profile represents half of the cross-section.

# Define points for the 2D profile (starting from top-right, going counter-clockwise)
# We are drawing on the XZ plane, so (X, Z) coordinates.
# The Z-axis is the axis of revolution.
pts = [
    (0, total_height / 2),                         # Top-center
    (radius, total_height / 2),                    # Top-right edge
    (radius, (total_height / 2) - plate_thickness),# Bottom of top plate edge
    (neck_width, (neck_height / 2)),               # Top of neck
    (neck_width, -(neck_height / 2)),              # Bottom of neck
    (radius, -((total_height / 2) - plate_thickness)), # Top of bottom plate edge
    (radius, -(total_height / 2)),                 # Bottom-right edge
    (0, -(total_height / 2))                       # Bottom-center
]

# Create the solid by revolving the profile 90 degrees
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(90, (0, 0, 0), (0, 1, 0)) # Revolve around Z-axis (which is Y in the local Workplane "XZ")
)

# Alternatively, to ensure correct orientation relative to global Z-up:
# The Workplane("XZ") sets Y as global Z.
# So revolving around local Y means revolving around global Z.