import cadquery as cq
import math

# --- Parameters ---
num_teeth = 20
outer_radius = 50.0   # Radius at the tip of the teeth
root_radius = 40.0    # Radius at the base of the teeth
bore_diameter = 10.0  # Diameter of the central hole
thickness = 15.0      # Thickness of the gear

# --- Geometry Calculations ---
# Calculate widths for a trapezoidal tooth profile
circumference = 2 * math.pi * root_radius
pitch = circumference / num_teeth

# Define tooth width at base and tip to match visual proportions
# Base width is roughly half the pitch (tooth matches gap)
tooth_width_base = pitch * 0.55
# Tip width is tapered
tooth_width_tip = tooth_width_base * 0.6

# --- Modeling ---

# 1. Create the central hub (root cylinder)
result = cq.Workplane("XY").circle(root_radius).extrude(thickness)

# 2. Define the shape of a single tooth
# We create the profile on the XY plane aligned with the X-axis
# Start slightly inside the root radius (-0.5) to ensure solid overlap for the boolean union
tooth_profile = (
    cq.Workplane("XY")
    .moveTo(root_radius - 0.5, -tooth_width_base / 2)
    .lineTo(root_radius - 0.5, tooth_width_base / 2)
    .lineTo(outer_radius, tooth_width_tip / 2)
    .lineTo(outer_radius, -tooth_width_tip / 2)
    .close()
)
tooth_solid = tooth_profile.extrude(thickness)

# 3. Create a circular array of teeth
# Using polarArray with radius=0 generates rotation locations at the origin
# We place the pre-calculated tooth_solid at each rotated location
teeth = (
    cq.Workplane("XY")
    .polarArray(0, 0, 360, num_teeth)
    .eachpoint(lambda loc: tooth_solid.val().located(loc))
)

# 4. Union the teeth with the hub
result = result.union(teeth)

# 5. Cut the central bore hole
result = result.faces(">Z").workplane().circle(bore_diameter / 2).cutThruAll()