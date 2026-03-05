import cadquery as cq
import math

# --- Parameters ---
cylinder_radius = 20.0  # Radius of the main cylinder
cylinder_height = 40.0  # Length of the cylinder
num_grooves = 12        # Number of helical grooves
groove_depth = 2.0      # Depth of the V-groove
groove_width = 4.0      # Width of the groove at the surface
twist_angle = 60.0      # Total rotation of the helix over the height (degrees)

# --- Geometry Construction ---

# 1. Create the base cylinder
base = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)

# 2. Define the cross-section of a single groove cutter
# We will sweep this shape along a helical path to remove material.
# The shape is a triangle (V-cutter) positioned at the edge of the cylinder.
cutter_profile = (
    cq.Workplane("XZ")
    .center(cylinder_radius, 0) # Move to the edge of the cylinder
    .moveTo(0, groove_width / 2)
    .lineTo(-groove_depth, 0)
    .lineTo(0, -groove_width / 2)
    .close()
)

# 3. Create the helical path for the sweep
# The path needs to spiral upwards.
helix_path = cq.Workplane("XY").parametricCurve(
    lambda t: (
        cylinder_radius * math.cos(t * math.radians(twist_angle)),
        cylinder_radius * math.sin(t * math.radians(twist_angle)),
        t * cylinder_height
    )
)

# 4. Create one groove by sweeping the profile along the path
# Note: In recent CadQuery versions, sweeping a solid or face along a helix
# can be complex. A boolean subtraction approach works reliably.
# We create a solid representing the "negative" space of the groove.

# We define the helix by pitch and height
helix_pitch = (cylinder_height * 360.0) / twist_angle

cutter_solid = (
    cq.Workplane("XY")
    .center(cylinder_radius, 0) # Start at cylinder edge
    # Draw the triangle profile on the bottom plane (XY), oriented correctly
    # X corresponds to radial direction, Y to tangential
    .polyline([(0, groove_width/2), (-groove_depth, 0), (0, -groove_width/2)])
    .close()
    # Sweep along a helix
    # pitch is height of one full turn
    .twistExtrude(cylinder_height, twist_angle)
)

# 5. Create the pattern of grooves and subtract them
# We rotate the single cutter solid around the Z-axis to create the pattern
cutters = cutter_solid
for i in range(1, num_grooves):
    angle = (360.0 / num_grooves) * i
    cutters = cutters.union(cutter_solid.rotate((0, 0, 0), (0, 0, 1), angle))

# 6. Subtract all cutters from the base cylinder
result = base.cut(cutters)

# Optional: Add small chamfers to the ends for a polished look like the image
result = result.faces("<Z or >Z").chamfer(0.5)