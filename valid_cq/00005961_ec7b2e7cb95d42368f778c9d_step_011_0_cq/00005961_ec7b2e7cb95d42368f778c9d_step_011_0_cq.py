import cadquery as cq

# Parametric dimensions for the rectangular plate
length = 100.0  # Length of the plate (x-axis)
width = 80.0    # Width of the plate (y-axis)
thickness = 2.0 # Thickness of the plate (z-axis)

# Create the rectangular plate
# We center it on the XY plane for better default positioning
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, if you prefer it sitting on top of the Z=0 plane instead of centered:
# result = cq.Workplane("XY").box(length, width, thickness, centered=(True, True, False))