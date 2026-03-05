import cadquery as cq

# -- Parametric Dimensions --
plate_width = 100.0   # Total width of the plate (x-axis)
plate_height = 80.0   # Total height of the plate (y-axis)
plate_thickness = 5.0 # Thickness of the plate (z-axis)

hole_diameter = 4.0   # Diameter of the through holes
hole_spacing_x = 70.0 # Distance between holes horizontally
hole_spacing_y = 50.0 # Distance between holes vertically

# -- Modeling --

# 1. Create the base rectangular plate
# We center it on the origin to make hole placement symmetric and easy
plate = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Create the pattern for the holes
# We use rect() to create a rectangular selection of points centered on the face
# These points will serve as the centers for our holes
result = (
    plate
    .faces(">Z")               # Select the top face
    .workplane()               # Create a new workplane on that face
    .rect(hole_spacing_x, hole_spacing_y, forConstruction=True) # Define a construction rectangle for positioning
    .vertices()                # Select the vertices of that construction rectangle
    .hole(hole_diameter)       # Cut holes at those vertices
)

# Optional: If countersunk holes were intended (hard to tell definitively from image, but common),
# one would use .cskHole(hole_diameter, csk_diameter, csk_angle) instead of .hole().
# Given the simple appearance, standard through holes are assumed.