import cadquery as cq

# Parameters for the geometry
thickness = 6.0
hole_spacing = 9.0
hole_size = 5.0
circle_radius = 2.5
gear_base_radius = 10.0
gear_tip_radius = 14.0
num_teeth = 5
tooth_angle_step = 18  # Degrees between teeth

# 1. Create the Main Body Profile
# We trace the perimeter of the lever arm, excluding the gear teeth details
# Coordinates are relative to the center of the circular hole (0,0)
main_body = (
    cq.Workplane("XY")
    .moveTo(24, 10)  # Top Right corner
    
    # Top Notch
    .lineTo(13, 10)
    .lineTo(13, 7.5)
    .lineTo(9, 7.5)
    .lineTo(9, 10)
    
    # Top Edge going left
    .lineTo(-20, 10)
    
    # Handle Curve (Top)
    # Using a spline to create a smooth transition to the foot
    .spline([(-65, -12)], tangents=[(-1, 0), (-1, -0.2)], includeCurrent=True)
    
    # Foot/Hook Detail
    .lineTo(-65, -9)   # Step up for the hook lip
    .lineTo(-70, -9)   # Top of the hook
    .lineTo(-75, -20)  # Slanted front face
    .lineTo(-60, -20)  # Bottom of the foot
    
    # Handle Curve (Bottom)
    # Curve back up to the gear base
    .spline([(-15, -10)], tangents=[(1, 0), (1, 0)], includeCurrent=True)
    
    # Gear Base Line
    .lineTo(24, -10)
    .close()
    .extrude(thickness)
)

# 2. Create and Union the Gear Teeth
# We generate teeth radially centered at (0,0) on the bottom edge
teeth_union = None

for i in range(num_teeth):
    # Calculate angle centered around -90 degrees (pointing down)
    angle_deg = (i - 2) * tooth_angle_step
    
    # Define a single tooth profile pointing downwards
    tooth = (
        cq.Workplane("XY")
        .moveTo(-1.8, -gear_base_radius)  # Base of tooth
        .lineTo(1.8, -gear_base_radius)
        .lineTo(1.2, -gear_tip_radius)    # Tip of tooth
        .lineTo(-1.2, -gear_tip_radius)
        .close()
        .extrude(thickness)
        .rotate((0, 0, 0), (0, 0, 1), angle_deg) # Rotate around Z axis at origin
    )
    
    if teeth_union is None:
        teeth_union = tooth
    else:
        teeth_union = teeth_union.union(tooth)

# Combine body and teeth
result = main_body.union(teeth_union)

# 3. Cut the Holes
# Central Circular Hole
result = result.cut(
    cq.Workplane("XY").circle(circle_radius).extrude(thickness)
)

# Left Square Hole
result = result.cut(
    cq.Workplane("XY")
    .moveTo(-hole_spacing, 0)
    .rect(hole_size, hole_size)
    .extrude(thickness)
)

# Right Square Hole
result = result.cut(
    cq.Workplane("XY")
    .moveTo(hole_spacing, 0)
    .rect(hole_size, hole_size)
    .extrude(thickness)
)