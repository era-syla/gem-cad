import cadquery as cq

# Parameters defining the dimensions and spacing of the bars
bar_length = 60.0       # Total length of each rectangular bar
bar_thickness = 3.0     # Cross-section dimension (assumed square)
horizontal_gap = 30.0   # Spacing between the two bars in each pair (X-axis)
vertical_gap = 50.0     # Spacing between the vertical layers (Z-axis)

# Define the center points for the bar cross-sections on the XZ plane
# The layout consists of 3 layers (vertical) of 2 bars (horizontal)
points = [
    # Bottom Pair
    (-horizontal_gap / 2, -vertical_gap), 
    (horizontal_gap / 2, -vertical_gap),
    
    # Middle Pair
    (-horizontal_gap / 2, 0), 
    (horizontal_gap / 2, 0),
    
    # Top Pair
    (-horizontal_gap / 2, vertical_gap), 
    (horizontal_gap / 2, vertical_gap),
]

# Create the geometry
# 1. Select the XZ plane to draw the cross-sections
# 2. Push the grid points onto the stack
# 3. Draw rectangles at all points
# 4. Extrude symmetrically along the Y-axis to form the bars
result = (
    cq.Workplane("XZ")
    .pushPoints(points)
    .rect(bar_thickness, bar_thickness)
    .extrude(bar_length / 2.0, both=True)
)