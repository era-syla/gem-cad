import cadquery as cq

# Parametric dimensions
length = 100.0  # Length of the plate
width = 80.0    # Width of the plate
thickness = 10.0 # Thickness of the plate
fillet_radius = 5.0 # Radius for the corner fillets

# Create the base rectangular plate
# We center it on the XY plane for easier symmetry handling
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .edges("|Z") # Select edges parallel to the Z axis (vertical edges)
    .fillet(fillet_radius) # Apply fillet to the selected edges
)

# If centering is not desired, one could use .rect(length, width, centered=False).extrude(thickness) instead
# but box() creates a centered solid by default which is generally good practice.