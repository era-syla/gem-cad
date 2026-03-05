import cadquery as cq

# Parametric dimensions for the rectangular board
height = 200.0  # Total height of the board
width = 60.0    # Width of the board
thickness = 10.0 # Thickness of the board

# Create the rectangular box
result = cq.Workplane("XY").box(width, thickness, height)

# Alternatively, if you want it standing up on the XY plane:
# result = cq.Workplane("XY").box(width, thickness, height)