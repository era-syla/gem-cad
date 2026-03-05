import cadquery as cq

# Parameters for the geometry
length = 160.0          # Total length of the lever
rear_width = 60.0       # Width at the back (Y-shaped end)
tip_width = 8.0         # Width at the front tip
thickness = 6.0         # Thickness of the plate
arm_thickness = 9.0     # Thickness of the individual arms of the Y
split_pos = 70.0        # X position where the Y-split converges
hole_diam = 4.5         # Diameter of the mounting holes
hole_spacing = 15.0     # Spacing between holes
hook_radius = 3.0       # Radius of the hook feature at the tip

# Derived parameters
y_rear_outer = rear_width / 2.0
y_rear_inner = y_rear_outer - arm_thickness
y_tip = tip_width / 2.0
holes_start_x = split_pos + 15.0

# 1. Create the main body profile (Top Half)
# We work on the XY plane and draw half the profile to mirror later
# Points definition
p_tip = (length, y_tip)
p_tip_center = (length, 0)
p_rear_outer = (0, y_rear_outer)
p_rear_inner = (0, y_rear_inner)
p_crotch = (split_pos, 0)

# Control points for organic splines to match the aesthetic
# Outer curve controls: narrowing waist near the holes, flaring to rear
cp_outer_1 = (split_pos + (length - split_pos) * 0.3, y_tip + 2.0)
cp_outer_2 = (split_pos * 0.8, y_rear_outer * 0.8)

# Inner curve controls: smooth U-shape for the split
cp_inner_1 = (split_pos * 0.5, y_rear_inner - 2.0)
cp_inner_2 = (split_pos - 10, 2.0) 

# Construct the 2D Sketch
sketch_half = (
    cq.Workplane("XY")
    .moveTo(*p_crotch)
    # Inner curve of the Y-arm
    .spline([cp_inner_2, cp_inner_1, p_rear_inner], includeCurrent=True)
    # Rear flat end of the arm
    .lineTo(*p_rear_outer)
    # Outer curve of the body
    .spline([cp_outer_2, cp_outer_1, p_tip], includeCurrent=True)
    # Front tip flat face
    .lineTo(*p_tip_center)
    .close()
)

# Extrude the sketch to create the 3D solid (half)
half_body = sketch_half.extrude(thickness)

# Mirror to create the full body
full_body = half_body.union(half_body.mirror("XZ"))

# 2. Add the mounting holes
# Located in the solid section just after the split
main_body = (
    full_body
    .faces(">Z")
    .workplane()
    .pushPoints([(holes_start_x, 0), (holes_start_x + hole_spacing, 0)])
    .hole(hole_diam)
)

# 3. Add the Hook/Catch feature at the tip
# Modeled as a cylinder oriented transversely on the top face at the tip
hook = (
    cq.Workplane("XZ")
    .workplane(offset=-tip_width/2.0)  # Offset to the side of the tip
    .moveTo(length - hook_radius, thickness) # Position on top edge
    .circle(hook_radius)
    .extrude(tip_width)
)

# Combine main body and hook
result = main_body.union(hook)

# Optional: Add small fillets to vertical edges for realism (robustness dependent)
try:
    result = result.edges("|Z").fillet(0.5)
except Exception:
    pass # Skip fillets if geometry kernel fails on complex spline edges