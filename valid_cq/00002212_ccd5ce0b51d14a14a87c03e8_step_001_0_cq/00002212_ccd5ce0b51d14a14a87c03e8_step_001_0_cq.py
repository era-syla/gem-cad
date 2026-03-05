import cadquery as cq

# Parametric dimensions for the linear rail (Modeled after a generic miniature linear guide rail like MGN12)
rail_length = 300.0  # Total length of the rail
rail_width = 12.0    # Width of the rail base
rail_height = 8.0    # Height of the rail
groove_width = 6.0   # Width of the top groove
groove_depth = 3.5   # Depth of the top groove
base_thickness = rail_height - groove_depth
mounting_hole_diameter = 3.5
mounting_hole_spacing = 25.0
mounting_hole_start_offset = 12.5

# Create the profile of the rail
# The profile is essentially a rectangle with a U-shaped cutout on top for the carriage bearings
def create_rail_profile(width, height, g_width, g_depth):
    # Points defining half the cross-section (symmetric about Y-axis)
    # Origin is at bottom center
    pts = [
        (0, 0),
        (width / 2, 0),
        (width / 2, height),
        (g_width / 2, height),
        (g_width / 2, height - g_depth), # Vertical side of groove
        # Often there's a specific raceway geometry here, simplified to rectangular groove for this visual
        (0, height - g_depth)
    ]
    return cq.Workplane("XY").polyline(pts).mirrorY().extrude(rail_length)

# Create the base rail extrusion
rail = create_rail_profile(rail_width, rail_height, groove_width, groove_depth)

# Add mounting holes (counterbored)
# Calculate hole positions
num_holes = int((rail_length - 2 * mounting_hole_start_offset) / mounting_hole_spacing) + 1
hole_positions = []

for i in range(num_holes):
    z_pos = mounting_hole_start_offset + i * mounting_hole_spacing
    # Center the holes relative to the extrusion length which starts at z=0 and goes to z=rail_length
    hole_positions.append((0, z_pos))

# Rotate the rail so it lays flat along X or Y as typical, but the extrusion was along Z.
# Let's orient it so length is along X, width along Y, height along Z
result = rail.rotate((0,0,0), (1,0,0), -90).rotate((0,0,0), (0,0,1), -90)

# Re-orient helps with hole placement logic if we think in X/Y plane for the face
# Current orientation: Length along X, Width along Y, Up along Z.
# Let's verify center. The original extrusion started at Z=0.
# After rotation, the rail starts at X=0.

# Let's just create the holes on the "top" face which is now +Z, along the centerline.
# The holes usually go all the way through.
# Counterbores are typical for these rails.
cbore_dia = 6.0
cbore_depth = 4.0

# Define hole locations along the X axis now
x_hole_locations = [(mounting_hole_start_offset + i * mounting_hole_spacing, 0) for i in range(num_holes)]

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints(x_hole_locations)
    .cboreHole(mounting_hole_diameter, cbore_dia, cbore_depth)
)

# Optional: Add the specific raceway grooves on the sides of the main groove if desired for high detail,
# but the image shows a relatively simple profile at this zoom level.
# The current U-profile captures the main visual characteristic.

# Center the result
result = result.translate((-rail_length/2, 0, 0))