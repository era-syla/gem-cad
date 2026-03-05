import cadquery as cq

# Parameters for dimensions
outer_diameter = 100.0  # Diameter of the entire cylinder
height = 30.0           # Total height of the object
wall_thickness = 3.0    # Thickness of the side walls
bottom_thickness = 3.0  # Thickness of the bottom floor

# Create the main solid cylinder
# We start by drawing a circle on the XY plane and extruding it
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(height)
)

# Create the hollow interior
# We select the top face and create a shell, or cut a pocket. 
# A shell operation with a negative thickness creates inward walls, 
# but simply cutting a pocket is often more explicit and easier to control parametrically for the bottom.

# Method: Cut a cylinder from the top
result = (
    result
    .faces(">Z")                   # Select the top face
    .workplane()                   # Create a new workplane on the top face
    .circle((outer_diameter / 2.0) - wall_thickness)  # Draw the inner circle
    .cutBlind(-(height - bottom_thickness))           # Cut down, leaving the bottom thickness
)

# Alternative "Shelling" approach (commented out, but valid):
# result = (
#     cq.Workplane("XY")
#     .circle(outer_diameter / 2.0)
#     .extrude(height)
#     .faces(">Z")
#     .shell(-wall_thickness)
# )
# Note: Shelling assumes uniform thickness for walls and bottom, which is likely for this shape. 
# The pocket method allows distinct wall and bottom thicknesses.