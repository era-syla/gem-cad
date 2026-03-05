import cadquery as cq

# Parametric dimensions defined to match the visual proportions of the image
width = 100.0          # Overall width of the part
depth = 60.0           # Depth of the top horizontal plate
plate_thickness = 12.0 # Thickness of the top plate
leg_thickness = 12.0   # Thickness of the vertical front wall/leg
total_height = 35.0    # Total height (top surface to bottom of leg)
cutout_radius = 25.0   # Radius of the semi-circular cutout
corner_radius = 10.0   # Fillet radius for the front corners

# 1. Create the base geometry (L-shaped profile extruded)
# The profile is sketched on the YZ plane to create the side view
# Coordinates are arranged so the origin (0,0,0) is at the center of the top front edge
# Y-axis is negative towards the back, Z-axis is negative downwards
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                                 # Top-Front
        (-depth, 0),                            # Top-Back
        (-depth, -plate_thickness),             # Bottom-Back of Plate
        (-leg_thickness, -plate_thickness),     # Inner Corner between plate and leg
        (-leg_thickness, -total_height),        # Bottom-Back of Leg
        (0, -total_height),                     # Bottom-Front of Leg
        (0, 0)                                  # Close loop
    ])
    .close()
    .extrude(width / 2.0, both=True)            # Extrude symmetrically along X-axis
)

# 2. Create the U-shaped/Semi-circular cutout
# The cutout is centered on the front edge (Origin)
result = (
    result
    .faces(">Z")                                # Select Top face
    .workplane()
    .circle(cutout_radius)                      # Draw circle at (0,0)
    .cutThruAll()                               # Cut through the entire solid
)

# 3. Apply fillets to the front vertical corners
# Selects vertical edges (|Z) that are at the extreme front (>Y)
result = (
    result
    .edges("|Z and >Y")
    .fillet(corner_radius)
)