import cadquery as cq

# Define parametric dimensions for the plate
length = 100.0  # Length of the plate
width = 40.0    # Width of the plate
thickness = 5.0 # Thickness of the plate

# Create the rectangular plate
# We center it on the XY plane for convenience
result = cq.Workplane("XY").box(length, width, thickness)

# Alternatively, if you prefer starting from a sketch and extruding:
# result = cq.Workplane("XY").rect(length, width).extrude(thickness)