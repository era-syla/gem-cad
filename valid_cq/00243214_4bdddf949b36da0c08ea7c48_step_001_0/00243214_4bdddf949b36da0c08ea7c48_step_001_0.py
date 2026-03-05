import cadquery as cq

# --- Parameters ---
# Ladder main dimensions
ladder_height = 120.0
ladder_width = 40.0      # Center-to-center distance between rails
rail_size = 6.0          # Cross-section size of the square rails
rung_radius = 2.0        # Radius of the circular rungs
rung_spacing = 30.0      # Vertical distance from center to rungs

# Floating bars dimensions
bar_width = ladder_width + rail_size  # Full outer width
bar_height = 4.0         # Vertical dimension of the flat bar
bar_thickness = 1.5      # Thickness (Y dimension)
float_spacing = 20.0     # Spacing between floating elements
float_start_z = ladder_height / 2 + 30.0

# Hole pattern parameters
hole_pitch = 10.0
hole_radius = 0.8

# --- Geometry Construction ---

# 1. Create the Vertical Rail with Perforations
def create_perforated_rail():
    # Base rail geometry centered at origin
    rail = cq.Workplane("XY").box(rail_size, rail_size, ladder_height)
    
    # Generate points for holes along the Z-axis
    # Range ensures holes don't go too close to the very ends
    start_z = -int(ladder_height/2) + int(hole_pitch)
    end_z = int(ladder_height/2)
    hole_points = [(0, z) for z in range(start_z, end_z, int(hole_pitch))]
    
    # Create the cutter cylinders
    # We draw on XZ plane and extrude along Y (normal to XZ) to cut through the rail
    holes = (
        cq.Workplane("XZ")
        .pushPoints(hole_points)
        .circle(hole_radius)
        .extrude(rail_size * 2, both=True)
    )
    
    return rail.cut(holes)

# Generate one rail instance
rail_template = create_perforated_rail()

# Position Left and Right Rails
left_rail = rail_template.translate((-ladder_width / 2, 0, 0))
right_rail = rail_template.translate((ladder_width / 2, 0, 0))

# 2. Create the Rungs
# Calculate length to fit between the inner faces of the rails
rung_length = ladder_width - rail_size

# Create a single rung oriented along X-axis
rung_geo = (
    cq.Workplane("YZ")
    .circle(rung_radius)
    .extrude(rung_length)
    .translate((-rung_length / 2, 0, 0)) # Center the rung on the X-axis
)

# Position the two rungs
bottom_rung = rung_geo.translate((0, 0, -rung_spacing))
top_rung = rung_geo.translate((0, 0, rung_spacing))

# 3. Create the Floating Bars
# Rectangular bars positioned above the ladder structure
floating_bar_geo = cq.Workplane("XY").box(bar_width, bar_thickness, bar_height)

bar_1 = floating_bar_geo.translate((0, 0, float_start_z))
bar_2 = floating_bar_geo.translate((0, 0, float_start_z + float_spacing))

# --- Final Assembly ---
result = (
    left_rail
    .union(right_rail)
    .union(bottom_rung)
    .union(top_rung)
    .union(bar_1)
    .union(bar_2)
)