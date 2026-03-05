import cadquery as cq

# Parameters for the ring
outer_diameter = 100.0  # Adjust the outer diameter as needed
height = 20.0           # Adjust the height (width) of the ring
thickness = 2.0         # Adjust the wall thickness

# Calculate inner diameter
inner_diameter = outer_diameter - (2 * thickness)

# Create the ring geometry
# Method 1: Create a solid cylinder and cut a smaller cylinder from it
# result = cq.Workplane("XY").cylinder(height, outer_diameter/2).cut(
#     cq.Workplane("XY").cylinder(height, inner_diameter/2)
# )

# Method 2: Sketch a circle and extrude as a thin-walled pipe (more idiomatic for rings)
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(height)
)

# Optional: If you prefer the 'tube' primitive which simplifies this
# result = cq.Workplane("XY").tube(length=height, outerRadius=outer_diameter/2, innerRadius=inner_diameter/2)