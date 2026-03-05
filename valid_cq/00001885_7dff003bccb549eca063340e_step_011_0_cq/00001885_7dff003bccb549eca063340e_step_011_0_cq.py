import cadquery as cq

# Parametric dimensions
outer_diameter = 50.0  # Overall diameter of the circle
thickness = 5.0        # Thickness of the ring wall and the crossbar
height = 5.0           # Extrusion height (depth) of the entire object

# Calculate the inner diameter based on thickness
inner_diameter = outer_diameter - (2 * thickness)

# 1. Create the base Ring
# We create a circle of the outer diameter and cut a circle of the inner diameter
ring = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(height)
)

# 2. Create the crossbar
# The bar spans the diameter. Its width matches the ring thickness.
# We create a rectangle and extrude it.
# The length needs to be at least the outer diameter to fully connect.
bar = (
    cq.Workplane("XY")
    .rect(outer_diameter, thickness)
    .extrude(height)
)

# 3. Combine the geometries
# Union the ring and the bar.
# Then intersect with the outer circle to trim any bar excess (though logically the bar length matches, 
# an intersection ensures the bar ends curve perfectly with the outer diameter).
# However, a simpler boolean union is sufficient if the bar is constrained properly, 
# but to be perfectly clean with the outer curvature, we can union them and then intersect with a cylinder.

# Method A: Union Ring + Bar
combined = ring.union(bar)

# Method B: To ensure the bar ends are perfectly flush with the circular profile (cleaner CAD):
# Create a solid cylinder representing the total outer volume
outer_cylinder = cq.Workplane("XY").circle(outer_diameter / 2).extrude(height)

# Intersect the combined shape with the outer cylinder to trim any potential overhangs of the rectangular bar
result = combined.intersect(outer_cylinder)

# Alternative (Simpler) construction in one chain:
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)       # Outer circle
    .circle(inner_diameter / 2)       # Inner circle (creates the ring profile)
    .rect(outer_diameter, thickness)  # Add the crossbar rectangle to the sketch
    .extrude(height)                  # Extrude the combined sketch regions
    .intersect(                       # Clean up the outer edges of the bar
        cq.Workplane("XY").circle(outer_diameter / 2).extrude(height)
    )
)

# Final clean version focusing on boolean operations for robustness:
# Create the ring
r = cq.Workplane("XY").circle(outer_diameter/2).circle(inner_diameter/2).extrude(height)
# Create the bar
b = cq.Workplane("XY").rect(outer_diameter, thickness).extrude(height)
# Union them
union_shape = r.union(b)
# Cut everything outside the main diameter to round off the bar ends perfectly
result = union_shape.intersect(cq.Workplane("XY").circle(outer_diameter/2).extrude(height))