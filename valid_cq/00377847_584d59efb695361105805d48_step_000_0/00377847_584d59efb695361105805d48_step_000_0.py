import cadquery as cq

# Parameters defining the pattern and geometry
num_columns = 20
num_rows = 2
pitch_x = 10.0       # Spacing along the length
pitch_y = 10.0       # Spacing between the rows
hex_diameter = 5.0   # Size of the hexagonal element
hole_diameter = 2.5  # Size of the inner hole
height = 2.0         # Thickness/Height of the elements

# Create the parametric model
# We use rarray to define a 2x20 grid of locations
# At each location, we draw a hexagon and a circle (for the hole), then extrude
result = (
    cq.Workplane("XY")
    .rarray(
        xSpacing=pitch_x, 
        ySpacing=pitch_y, 
        xCount=num_columns, 
        yCount=num_rows, 
        center=True
    )
    .polygon(nSides=6, diameter=hex_diameter)
    .circle(hole_diameter / 2.0)
    .extrude(height)
)