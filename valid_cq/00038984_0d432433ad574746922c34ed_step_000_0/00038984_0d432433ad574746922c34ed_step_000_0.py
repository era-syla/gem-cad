import cadquery as cq

# --- Parameters ---
rail_width = 8.0         # Width of the rail cross-section (x-y plane)
rail_thickness = 8.0     # Thickness of the rail (z-height)
front_length = 100.0     # Length of the straight parallel section
rear_curve_length = 40.0 # Length of the curved expanding section (projected on X)
rear_tip_length = 10.0   # Length of the straight tip after the curve
inner_width_front = 60.0 # Inner distance between rails at the straight section
inner_width_rear = 100.0 # Inner distance between rails at the flared end
crossbar_pos_x = 0.0     # X position of the crossbar center

# --- Derived Calculations ---
y_inner_front = inner_width_front / 2.0
y_outer_front = y_inner_front + rail_width
y_inner_rear = inner_width_rear / 2.0
y_outer_rear = y_inner_rear + rail_width

# Key X-coordinates
# We assume the crossbar is at X=0. The straight section extends to +X.
# The curved section extends to -X.
x_junction = crossbar_pos_x - (rail_width / 2.0)
x_curve_end = x_junction - rear_curve_length
x_total_end = x_curve_end - rear_tip_length

# Tangent magnitude for the spline generation
# Controls the 'tightness' of the S-curve. A value equal to the length is a standard starting point.
t_mag = rear_curve_length * 1.0

# --- Geometry Construction ---

# 1. Generate the Top Rail
# We define the profile in the XY plane by moving CCW around the perimeter
top_rail = (
    cq.Workplane("XY")
    # Start at the front-right outer corner
    .moveTo(front_length, y_outer_front)
    # Straight line to the start of the curve (junction area)
    .lineTo(x_junction, y_outer_front)
    # Outer S-curve: expanding outwards. Tangents are horizontal (-X direction).
    .spline([(x_curve_end, y_outer_rear)], 
            tangents=[(-t_mag, 0), (-t_mag, 0)], 
            includeCurrent=True)
    # Straight tip section
    .lineTo(x_total_end, y_outer_rear)
    # End cap of the rail
    .lineTo(x_total_end, y_inner_rear)
    # Inner side of the tip
    .lineTo(x_curve_end, y_inner_rear)
    # Inner S-curve: contracting inwards. Tangents are horizontal (+X direction).
    .spline([(x_junction, y_inner_front)], 
            tangents=[(t_mag, 0), (t_mag, 0)], 
            includeCurrent=True)
    # Inner straight section back to front
    .lineTo(front_length, y_inner_front)
    # Close the profile
    .close()
    # Extrude to create solid
    .extrude(rail_thickness)
    # Center the solid in Z
    .translate((0, 0, -rail_thickness / 2.0))
)

# 2. Generate the Bottom Rail
# Mirror the top rail across the XZ plane
bottom_rail = top_rail.mirror("XZ")

# 3. Generate the Crossbar
# A simple box connecting the inner faces of the straight sections
crossbar = (
    cq.Workplane("XY")
    # The box width corresponds to the gap.
    # Note: We use the full width and boolean union handles the overlap/merging.
    .box(rail_width, inner_width_front, rail_thickness)
    .translate((crossbar_pos_x, 0, 0))
)

# 4. Combine all components
result = top_rail.union(bottom_rail).union(crossbar)