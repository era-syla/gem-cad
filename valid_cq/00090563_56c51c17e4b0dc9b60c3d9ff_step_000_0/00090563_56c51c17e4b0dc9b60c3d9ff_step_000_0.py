import cadquery as cq

# --- Parametric Dimensions ---
width = 42.0           # Overall width of the bracket (NEMA 17 standard)
height = 55.0          # Overall height
base_length = 55.0     # Length of the horizontal base leg
top_length = 48.0      # Length of the top motor mount leg
wall_thickness = 8.0   # Thickness of the structural walls
fillet_radius = 45.0   # Radius of the large structural curve

# Feature Dimensions
motor_bore_dia = 22.1       # Center hole for motor boss
motor_hole_spacing = 31.0   # Mounting hole pattern spacing
motor_hole_dia = 3.4        # Mounting hole diameter (M3 clearance)
base_hole_dia = 4.5         # Base mounting hole diameter
base_cbore_dia = 9.0        # Base counterbore diameter
base_cbore_depth = 3.0      # Base counterbore depth
side_hole_dia = 3.0         # Small holes on the side face

# --- Modeling ---

# 1. Generate the Main Body Profile
# Sketch on XZ plane, extrude along Y
# Profile is defined starting from bottom-rear (0,0)
main_body = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_length, 0)                   # Bottom edge
    .lineTo(base_length, wall_thickness)      # Front face of base
    # Large curve connecting the base lip to the top lip
    # A negative radius in radiusArc typically creates a concave solution depending on direction
    .radiusArc((top_length, height - wall_thickness), -fillet_radius)
    .lineTo(top_length, height)               # Front face of top
    .lineTo(0, height)                        # Top edge
    .close()
    .extrude(width)
)

# 2. Motor Mount Features (Top Face)
# Calculate center of the motor pattern
# Center X is relative to the top leg length
motor_center_x = top_length / 2.0
# Center Y is the middle of the extrusion width
motor_center_y = width / 2.0

main_body = (
    main_body
    .faces(">Z")
    .workplane()
    # Main center bore
    .moveTo(motor_center_x, motor_center_y)
    .circle(motor_bore_dia / 2.0)
    .cutThruAll()
    # 4x Mounting screw holes
    .moveTo(motor_center_x, motor_center_y)
    .rect(motor_hole_spacing, motor_hole_spacing, forConstruction=True)
    .vertices()
    .circle(motor_hole_dia / 2.0)
    .cutThruAll()
)

# 3. Base Mounting Holes (Bottom Face)
# Positioned on the base flange
base_hole_x = base_length - 8.0  # Set back from the tip
base_hole_y_offset = width / 2.0 - 8.0 # Offset from sides

main_body = (
    main_body
    .faces("<Z")
    .workplane(invert=True) # Invert to machine from bottom up (for counterbore)
    # Left Hole
    .moveTo(base_hole_x, width/2.0 + base_hole_y_offset)
    .cboreHole(base_hole_dia, base_cbore_dia, base_cbore_depth)
    # Right Hole
    .moveTo(base_hole_x, width/2.0 - base_hole_y_offset)
    .cboreHole(base_hole_dia, base_cbore_dia, base_cbore_depth)
)

# 4. Side Holes
# Small holes on the large flat side face
# Coordinates estimated from visual
side_hole_z = 15.0
side_hole_x1 = 15.0
side_hole_x2 = 35.0

result = (
    main_body
    .faces(">Y") # Select the 'front' flat face of the profile extrusion
    .workplane()
    .moveTo(side_hole_x1, side_hole_z)
    .circle(side_hole_dia / 2.0)
    .moveTo(side_hole_x2, side_hole_z)
    .circle(side_hole_dia / 2.0)
    .cutBlind(-10.0) # Shallow cut
)