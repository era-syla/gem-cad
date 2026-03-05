import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 90.0       # Total width of the plate
height = 50.0       # Total height of the plate
thickness = 5.0     # Thickness of the plate
fillet_radius = 6.0 # Radius of the rounded corner

# Create the 3D model
result = (
    cq.Workplane("XY")
    # Create a centered rectangular box
    .box(length, height, thickness)
    # Select the vertical edge at the top-left corner
    # |Z : Selects edges parallel to the Z axis
    # <X : Selects the edge on the negative X side (Left)
    # >Y : Selects the edge on the positive Y side (Top)
    .edges("|Z and <X and >Y")
    # Apply the fillet to the selected edge
    .fillet(fillet_radius)
)