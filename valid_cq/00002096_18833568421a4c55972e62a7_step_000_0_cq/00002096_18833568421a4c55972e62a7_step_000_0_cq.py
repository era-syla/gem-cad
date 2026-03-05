import cadquery as cq

# Parametric dimensions
width = 100.0   # Total width of the triangle base
height = 60.0   # Height of the triangle from base to apex
thickness = 15.0 # Thickness of the plate
fillet_radius = 5.0 # Radius for the corners

# Define the points of the triangle
# Centering the base on the X-axis for symmetry
p1 = (-width / 2, 0)
p2 = (width / 2, 0)
p3 = (0, height) # Apex point (offset in Y)

# Create the base sketch and extrude
# 1. Start a sketch
# 2. Draw a polygon using the defined points
# 3. Extrude to create the 3D solid
# 4. Apply fillets to vertical edges

result = (
    cq.Workplane("XY")
    .polyline([p1, p2, p3])
    .close()
    .extrude(thickness)
    .edges("|Z") # Select vertical edges
    .fillet(fillet_radius)
)