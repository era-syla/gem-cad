import cadquery as cq

# Define parametric dimensions for the shape
base_width_radius = 25.0   # Major radius of the base ellipse
base_thick_radius = 12.0   # Minor radius of the base ellipse

# Define the control points for the loft trajectory
# Format: (Z height, Y offset (backward curve), X rotation (degrees), Scale factor)
sections_data = [
    (0.0, 0.0, 0.0, 1.0),           # Base section at origin
    (30.0, 10.0, -15.0, 0.85),      # Lower-mid section starting the bend
    (60.0, 32.0, -35.0, 0.65),      # Upper-mid section continuing the curve
    (85.0, 60.0, -55.0, 0.45)       # Top section, tapered and angled
]

# Generate the wire profiles for the loft
wires = []
for z, y, rot_x, scale in sections_data:
    # Create a workplane transformed to the specific position and orientation
    # We construct each from global XY to ensure absolute positioning
    wp = cq.Workplane("XY").transformed(
        offset=cq.Vector(0, y, z),
        rotate=cq.Vector(rot_x, 0, 0)
    )
    
    # Create the elliptical profile
    # The profile scales down as it goes up
    profile = wp.ellipse(
        base_width_radius * scale, 
        base_thick_radius * scale
    ).wires().val()
    
    wires.append(profile)

# Create the solid geometry by lofting through the wires
# ruled=False creates a smooth, organic surface interpolation (spline-based)
loft_solid = cq.Solid.makeLoft(wires, ruled=False)

# Create the final result variable
result = cq.Workplane(obj=loft_solid)