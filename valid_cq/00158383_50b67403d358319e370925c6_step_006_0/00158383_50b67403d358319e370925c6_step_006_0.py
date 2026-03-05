import cadquery as cq
import math

# --- Parameters ---
length = 300.0        # Total length of the rack
width = 8.0           # Width (Y-axis)
height = 8.0          # Total height (Z-axis)
module = 0.8          # Gear module (controls tooth size)
pressure_angle = 20.0 # Pressure angle in degrees

# --- Derived Geometry Calculations ---
pitch = math.pi * module
tooth_depth = 2.25 * module
z_root = height - tooth_depth
z_tip = height
z_base = 0.0

# Tooth profile geometry
# We define a trapezoidal tooth profile based on standard rack dimensions
# Tip width roughly 0.3 * pitch, Root width roughly 0.7 * pitch for clearance
tip_width = 0.3 * pitch
root_width = 0.7 * pitch
slope_run = (root_width - tip_width) / 2.0

# Calculate number of teeth and centering margin
num_teeth = int((length - 2.0) / pitch) # Ensure teeth fit within length
total_teeth_span = num_teeth * pitch
margin = (length - total_teeth_span) / 2.0

# --- Profile Generation ---
# We will generate the 2D profile on the XZ plane
points = []
x_start = -length / 2.0
x_end = length / 2.0

# 1. Start at Bottom-Left corner
points.append((x_start, z_base))

# 2. Go up to the Root level on the left side
points.append((x_start, z_root))

# 3. Generate the teeth pattern
current_x = x_start + margin

for _ in range(num_teeth):
    # Start of tooth rise (at root level)
    points.append((current_x, z_root))
    
    # Tooth tip start (up slope)
    points.append((current_x + slope_run, z_tip))
    
    # Tooth tip end (flat top)
    points.append((current_x + slope_run + tip_width, z_tip))
    
    # End of tooth fall (down slope to root level)
    points.append((current_x + root_width, z_root))
    
    # Move x to the start of the next tooth (pitch distance)
    current_x += pitch

# 4. Finish the top line to the right edge
points.append((x_end, z_root))

# 5. Go down to Bottom-Right corner
points.append((x_end, z_base))

# 6. The close() method will connect back to Bottom-Left

# --- Model Creation ---
result = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .extrude(width)
    .translate((0, -width / 2.0, 0)) # Center on Y-axis
)