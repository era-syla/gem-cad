import cadquery as cq
from math import pi, cos, sin, radians

# --- Parametric Variables ---
num_teeth = 16          # Number of teeth
outer_diameter = 100.0  # Diameter at the tips of the teeth
root_diameter = 80.0    # Diameter at the base of the teeth
thickness = 10.0        # Thickness of the gear
bore_diameter = 10.0    # Diameter of the center hole
tooth_width_top = 8.0   # Width of the tooth at the outer diameter (approx)
tooth_width_base = 10.0 # Width of the tooth at the root diameter (approx)

# --- Calculated Values ---
outer_radius = outer_diameter / 2.0
root_radius = root_diameter / 2.0
bore_radius = bore_diameter / 2.0

# --- Geometry Construction ---

# 1. Create the base disk (the root circle)
base_gear = cq.Workplane("XY").circle(root_radius).extrude(thickness)

# 2. Create a single tooth profile
# We'll sketch the tooth on the XY plane and extrude it
# A tooth is roughly a trapezoid
tooth_height = outer_radius - root_radius

# Calculate points for a symmetrical trapezoidal tooth centered on the Y-axis
# This makes rotation easier later
t_half_top = tooth_width_top / 2.0
t_half_base = tooth_width_base / 2.0

# Define vertices for the tooth shape relative to the root radius
# Order: Bottom-Right, Top-Right, Top-Left, Bottom-Left
tooth_pts = [
    (t_half_base, root_radius),
    (t_half_top, outer_radius),
    (-t_half_top, outer_radius),
    (-t_half_base, root_radius)
]

# Create one tooth solid
single_tooth = (
    cq.Workplane("XY")
    .polyline(tooth_pts)
    .close()
    .extrude(thickness)
)

# 3. Create all teeth using a polar pattern
# We unite the base cylinder with the pattern of teeth
teeth = (
    single_tooth
    .rotate((0, 0, 0), (0, 0, 1), 360/num_teeth/2) # Initial adjustment if needed
    .polarArray(root_radius, 0, 360, num_teeth) # Just creates locations
)

# CadQuery's polarArray creates a location stack. We need to instantiate the geometry.
# However, a cleaner way in CQ for complex additions is often to make one and rotate/union it.
# Let's use a loop or the union capability with rotation.

# Alternative approach using a single sketch for the whole profile is often cleaner,
# but building additively is very intuitive for this shape.

gear_solid = base_gear

for i in range(num_teeth):
    angle = i * (360.0 / num_teeth)
    rotated_tooth = single_tooth.rotate((0,0,0), (0,0,1), angle)
    gear_solid = gear_solid.union(rotated_tooth)

# 4. Create the center bore
result = gear_solid.faces("<Z").workplane().circle(bore_radius).cutThruAll()

# Export is not requested, just the 'result' variable.