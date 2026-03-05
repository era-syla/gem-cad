import cadquery as cq

# Parameters for the ring geometry
outer_diameter = 60.0   # Outer diameter of the ring
height = 20.0           # Height of the ring
wall_thickness = 3.0    # Thickness of the wall
fillet_radius = 1.0     # Radius for the top and bottom edge fillets

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .circle(outer_radius)       # Outer profile
    .circle(inner_radius)       # Inner profile (creates the hole)
    .extrude(height)            # Create the solid tube
    .faces("+Z or -Z")          # Select the top and bottom faces
    .edges()                    # Select the edges of those faces (inner and outer loops)
    .fillet(fillet_radius)      # Apply rounding to the edges
)