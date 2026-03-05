import cadquery as cq
import math

# --- Parameters ---
hub_diameter = 20.0
hub_height = 10.0
shaft_diameter = 6.0
keyway_width = 2.0
keyway_depth = 1.0  # Depth into the hub from the hole wall

blade_outer_diameter = 80.0
num_blades = 6
blade_thickness = 1.5
blade_pitch_angle = 30.0  # Degrees
blade_coverage_angle = 35.0  # Angular width of the blade

# --- Derived Geometry ---
hub_radius = hub_diameter / 2.0
shaft_radius = shaft_diameter / 2.0
blade_outer_radius = blade_outer_diameter / 2.0
# Slightly embed blade into hub to ensure boolean union works
blade_inner_radius = hub_radius - 0.5

# --- 1. Create the Central Hub ---
# Basic cylinder
hub = cq.Workplane("XY").circle(hub_radius).extrude(hub_height)

# Cut the shaft hole
hub = hub.faces(">Z").workplane().hole(shaft_diameter)

# Cut the keyway
# We create a cutting tool that overlaps the edge of the hole
keyway_cutter = (
    cq.Workplane("XY")
    .moveTo(0, shaft_radius)  # Position at the edge of the hole
    .rect(keyway_width, keyway_depth * 2, centered=True) # Overlap the edge
    .extrude(hub_height)
)
hub = hub.cut(keyway_cutter)

# --- 2. Construct a Single Blade ---
# We calculate the 4 corners of the blade sector on the XY plane.
# The blade is centered along the X-axis (Angle = 0).

half_angle = math.radians(blade_coverage_angle / 2.0)

# Calculate coordinates for the sector
# p1: Inner Start (Bottom)
p1 = (blade_inner_radius * math.cos(-half_angle), blade_inner_radius * math.sin(-half_angle))
# p2: Outer Start (Bottom)
p2 = (blade_outer_radius * math.cos(-half_angle), blade_outer_radius * math.sin(-half_angle))
# p3: Outer End (Top)
p3 = (blade_outer_radius * math.cos(half_angle), blade_outer_radius * math.sin(half_angle))
# p4: Inner End (Top)
p4 = (blade_inner_radius * math.cos(half_angle), blade_inner_radius * math.sin(half_angle))

# Midpoints for defining the arcs (at angle 0)
p_mid_inner = (blade_inner_radius, 0)
p_mid_outer = (blade_outer_radius, 0)

# Draw the blade profile and extrude
blade_raw = (
    cq.Workplane("XY")
    .moveTo(*p1)
    .lineTo(*p2)
    .threePointArc(p_mid_outer, p3)  # Outer arc
    .lineTo(*p4)
    .threePointArc(p_mid_inner, p1)  # Inner arc
    .close()
    .extrude(blade_thickness)
)

# --- 3. Orient and Position the Blade ---
# Center the blade geometry vertically relative to its own thickness
blade = blade_raw.translate((0, 0, -blade_thickness / 2.0))

# Apply Pitch: Rotate around the radial axis (X-axis)
blade = blade.rotate((0, 0, 0), (1, 0, 0), blade_pitch_angle)

# Move blade to the middle of the hub height
blade = blade.translate((0, 0, hub_height / 2.0))

# --- 4. Array and Combine ---
# Create the circular array of blades by rotating and unioning
fan_blades = blade
for i in range(1, num_blades):
    angle = i * (360.0 / num_blades)
    fan_blades = fan_blades.union(blade.rotate((0, 0, 0), (0, 0, 1), angle))

# Union blades with the hub
result = hub.union(fan_blades)