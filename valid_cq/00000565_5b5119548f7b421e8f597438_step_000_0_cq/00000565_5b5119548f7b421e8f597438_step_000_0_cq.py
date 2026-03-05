import cadquery as cq

# Parametric definitions for the spring
wire_diameter = 2.0      # Diameter of the wire cross-section
coil_diameter_outer = 20.0 # Outer diameter of the coil
coil_diameter_center = coil_diameter_outer - wire_diameter # Centerline diameter
pitch = 6.0              # Distance between coils
turns = 8                # Number of full rotations
height = pitch * turns   # Total height of the spring

# Helper function to create a helix path
def helix(r, h, p):
    """
    Create a helix wire.
    r: radius
    h: height
    p: pitch
    """
    # Calculate the number of turns based on height and pitch
    num_turns = h / p
    
    # Create the helix path
    path = cq.Wire.makeHelix(pitch=p, height=h, radius=r)
    return path

# 1. Create the path (the helix)
# Using radius = center diameter / 2
helix_radius = coil_diameter_center / 2.0
path = helix(helix_radius, height, pitch)

# 2. Create the cross-section (circle for the wire)
# We need to position a sketch at the start of the helix path
# to sweep it along the path.
result = (
    cq.Workplane("XY")
    .center(helix_radius, 0) # Position at the start radius
    .workplane(offset=0)      # Establish workplane
    .transformed(rotate=(0, 0, 0)) # Ensure orientation is correct relative to global
    .circle(wire_diameter / 2.0) # Draw the wire cross-section
    .sweep(path, isFrenet=True) # Sweep along the helical path
)

# Export or display is usually handled outside, but 'result' holds the object.