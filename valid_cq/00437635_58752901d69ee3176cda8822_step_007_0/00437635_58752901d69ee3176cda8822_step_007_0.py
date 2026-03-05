import cadquery as cq

# Parameters for the model
height = 100.0       # Total height of the bar
diameter = 12.0      # Diameter of the circumscribed circle for the octagon
num_sides = 8        # Number of sides for the octagon

# Create the octagonal prism
# We rotate the polygon by 22.5 degrees so that the faces are aligned 
# with the X and Y axes (flats on top/sides), matching the image style.
result = (
    cq.Workplane("XY")
    .polygon(nSides=num_sides, diameter=diameter)
    .rotate((0, 0, 0), (0, 0, 1), 22.5)
    .extrude(height)
)