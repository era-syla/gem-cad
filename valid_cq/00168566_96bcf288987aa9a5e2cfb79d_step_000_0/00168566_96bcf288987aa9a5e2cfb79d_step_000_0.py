import cadquery as cq
import math

# Parameters for the parametric model
length = 60.0          # Total length of the pin
diameter = 12.0        # Outer diameter
groove_radius = 2.0    # Radius of the longitudinal cutouts
num_grooves = 4        # Number of grooves (cruciform pattern)
chamfer_size = 0.75    # Size of the chamfer at the ends

# Derived calculation
radius = diameter / 2.0

# Calculate center positions for the groove cutters
# We place the centers on the perimeter of the main cylinder to create the notches
groove_centers = []
for i in range(num_grooves):
    angle = math.radians(i * (360.0 / num_grooves))
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    groove_centers.append((x, y))

# Create the 3D model
result = (
    cq.Workplane("XY")
    # 1. Create the base cylinder
    .circle(radius)
    .extrude(length)
    
    # 2. Cut the longitudinal grooves
    .faces(">Z")
    .workplane()
    .pushPoints(groove_centers)
    .circle(groove_radius)
    .cutThruAll()
    
    # 3. Chamfer the top and bottom edges
    # Applying chamfer after the cut ensures the profile is chamfered correctly
    .edges(">Z or <Z")
    .chamfer(chamfer_size)
)