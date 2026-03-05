import cadquery as cq

# Parametric dimensions
bar_length = 60.0       # Long dimension of the bar
bar_width = 8.0         # Short dimension of the bar
bar_thickness = 3.0     # Z-height of the bar
num_bars = 10           # Number of bars in the array
spacing = 16.0          # Center-to-center distance (pitch)

# Create the model
# We create a workplane, establish a 1D rectangular array of points,
# draw a rectangle at each point, and extrude them all simultaneously.
result = (
    cq.Workplane("XY")
    .rarray(
        xSpacing=1,            # Dummy value since xCount is 1
        ySpacing=spacing,      # Distance between centers along Y axis
        xCount=1,              # 1 column of bars
        yCount=num_bars,       # 10 rows of bars
        center=True            # Center the whole array pattern at origin
    )
    .rect(bar_length, bar_width)
    .extrude(bar_thickness)
)