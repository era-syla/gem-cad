import cadquery as cq

# Parametric dimensions
length = 100.0      # Length of the angle bar
leg_width = 10.0    # Width of the horizontal leg
leg_height = 10.0   # Height of the vertical leg
thickness = 1.5     # Wall thickness

# Create the sketch for the L-profile cross-section
# We draw the "L" shape on the YZ plane and extrude along X
# The origin will be at the outer corner of the L-shape

# Method 1: Drawing points and creating a polyline
pts = [
    (0, 0),                       # Outer corner
    (leg_width, 0),               # End of horizontal leg (outer)
    (leg_width, thickness),       # End of horizontal leg (inner)
    (thickness, thickness),       # Inner corner
    (thickness, leg_height),      # End of vertical leg (inner)
    (0, leg_height),              # End of vertical leg (outer)
    (0, 0)                        # Close loop
]

# Create the profile and extrude
result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# Optional: Add small fillets to represent a realistic extrusion, if desired, 
# but the image shows sharp edges so we will keep it simple.
# result = result.edges("|X").fillet(0.2) 

# Export for visualization (if run locally)
# show_object(result)