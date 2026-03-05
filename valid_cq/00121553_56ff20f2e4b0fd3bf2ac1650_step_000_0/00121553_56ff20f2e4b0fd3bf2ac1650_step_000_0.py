import cadquery as cq

# -- Parametric Dimensions --
length = 100.0         # Distance between the centers of the two holes
head_diameter = 35.0   # Outer diameter of the cylindrical ends
hole_diameter = 18.0   # Diameter of the through-holes
bar_width = 20.0       # Width of the rectangular connecting section
thickness = 15.0       # Thickness (height) of the entire part

# -- Geometry Construction --

# 1. Create the first cylindrical end at the origin (0, 0)
# We extrude a circle centered at the origin
cylinder_1 = cq.Workplane("XY").circle(head_diameter / 2.0).extrude(thickness)

# 2. Create the second cylindrical end at (length, 0)
# We move the center to the specified length
cylinder_2 = cq.Workplane("XY").center(length, 0).circle(head_diameter / 2.0).extrude(thickness)

# 3. Create the connecting bar
# The bar is a rectangular prism connecting the two cylinders.
# We center the drawing plane at half the length (length / 2).
# The rectangle length is equal to 'length' so it extends from the center of cylinder 1 to cylinder 2.
# Since the cylinders are wider than the bar, this ensures a solid overlap without gaps.
bar = cq.Workplane("XY").center(length / 2.0, 0).rect(length, bar_width).extrude(thickness)

# 4. Combine parts into a single solid using Boolean Union
# We start with cylinder_1 and fuse the other components
main_body = cylinder_1.union(cylinder_2).union(bar)

# 5. Create the holes
# We select the top face of the main body, push points to the centers of the cylinders,
# draw circles, and cut through the entire part.
result = (
    main_body.faces(">Z")
    .workplane()
    .pushPoints([(0, 0), (length, 0)])
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# Optional: Add fillets to vertical edges for smoothness (commented out for strict robustness)
# result = result.edges("|Z").fillet(2.0)