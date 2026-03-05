import cadquery as cq

# Parameters for the model
# Dimensions estimated based on typical proportions seen in the image
width = 50.0       # Total width of the tab
height = 50.0      # Total height of the tab
thickness = 10.0   # Thickness of the plate
hole_diameter = 15.0 # Diameter of the central hole
fillet_radius = 10.0 # Radius for the top corners

# Create the base rectangular plate
# We start with a centered box, then move it so the bottom is at Z=0 and centered on Y
result = (
    cq.Workplane("XY")
    .box(width, height, thickness)
    # Fillet the top two corners
    # We select edges that are vertical (Z-parallel) and pick the ones with higher Y coordinates
    .edges("|Z and >Y")
    .fillet(fillet_radius)
    # Create the hole
    # We select the front face, then create a hole through the entire part
    .faces(">Z")
    .workplane()
    # Position the hole relative to the top edge or center.
    # Based on the image, the hole looks somewhat centered in the upper portion.
    # Let's shift it up from the center slightly.
    .center(0, height * 0.15) 
    .hole(hole_diameter)
)

# Alternative approach (often more robust for precise placement relative to edges):
# Sketching the profile on a plane and extruding
"""
result = (
    cq.Workplane("XY")
    .rect(width, height)
    .extrude(thickness)
    .edges("|Z and >Y")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .center(0, height/4) # Adjust hole vertical position
    .hole(hole_diameter)
)
"""

# Final adjustment to ensure orientation matches the isometric view generally expected
# The initial code creates it flat on XY. The image shows it standing up.
# Let's rotate it to stand up for better viewing if exported.
result = result.rotate((0, 0, 0), (1, 0, 0), 90)