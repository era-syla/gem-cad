import cadquery as cq

# Parametric dimensions based on visual approximation
total_length = 120.0     # Total length along the X-axis
narrow_width = 40.0      # Width of the longer strip along the Y-axis
center_length = 40.0     # Length of the wider center section along the X-axis
center_width = 80.0      # Width of the wider center section along the Y-axis
thickness = 5.0          # Thickness of the plate along the Z-axis

# Create the main long, narrow strip centered at the origin
main_strip = cq.Workplane("XY").box(total_length, narrow_width, thickness)

# Create the wider center section centered at the origin
center_section = cq.Workplane("XY").box(center_length, center_width, thickness)

# Combine the two shapes to create the final geometry
result = main_strip.union(center_section)