import cadquery as cq
from math import pi, tan, radians

# --- Parameters ---
module = 1.0                # Module of the gear rack
num_teeth = 50              # Number of teeth
pressure_angle = 20.0       # Pressure angle in degrees
rack_width = 8.0            # Width (thickness) of the rack
base_height = 6.0           # Height of the solid base below the teeth roots

# --- Derived Geometry Calculations ---
pitch = pi * module
alpha_rad = radians(pressure_angle)

addendum = module
dedendum = 1.25 * module
tooth_depth = addendum + dedendum
total_height = base_height + tooth_depth
total_length = num_teeth * pitch

# Calculate horizontal offsets for the trapezoidal tooth profile
# The profile is defined by the pressure angle
dx_addendum = addendum * tan(alpha_rad)
dx_dedendum = dedendum * tan(alpha_rad)

# --- Profile Generation ---
# We generate a list of (x, z) points to define the side profile of the rack
points = []

# Start at the origin (bottom-left)
points.append((0.0, 0.0))

# Bottom edge to bottom-right
points.append((total_length, 0.0))

# Right edge up to the root height
points.append((total_length, base_height))

# Generate teeth coordinates
# We iterate from right to left (high X to low X) to maintain 
# a counter-clockwise winding order for the polygon.
for i in range(num_teeth - 1, -1, -1):
    # X coordinate of the start of the current tooth cycle
    cycle_start_x = i * pitch
    
    # Calculate X coordinates for the four corners of a rack tooth
    # Reference: Center of tooth at pitch line is at (cycle_start_x + 0.5*pitch)
    # Tooth thickness at pitch line is 0.5*pitch
    
    # Point D: Right Root (start of slope up)
    # 0.75*pitch is the center of the right flank at the pitch line
    x_root_right = cycle_start_x + (0.75 * pitch) + dx_dedendum
    
    # Point C: Right Tip (end of slope up)
    x_tip_right = cycle_start_x + (0.75 * pitch) - dx_addendum
    
    # Point B: Left Tip (start of slope down)
    # 0.25*pitch is the center of the left flank at the pitch line
    x_tip_left = cycle_start_x + (0.25 * pitch) + dx_addendum
    
    # Point A: Left Root (end of slope down)
    x_root_left = cycle_start_x + (0.25 * pitch) - dx_dedendum
    
    # Append points for this tooth
    points.append((x_root_right, base_height)) # Bottom of right flank
    points.append((x_tip_right, total_height)) # Top of right flank
    points.append((x_tip_left, total_height))  # Top of left flank
    points.append((x_root_left, base_height))  # Bottom of left flank

# Close the loop back to the left edge
points.append((0.0, base_height))
points.append((0.0, 0.0)) # Closing point (explicitly or implicitly via close())

# --- Solid Creation ---
# Create the 2D profile on the XZ plane and extrude along Y to create width
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .extrude(rack_width)
)