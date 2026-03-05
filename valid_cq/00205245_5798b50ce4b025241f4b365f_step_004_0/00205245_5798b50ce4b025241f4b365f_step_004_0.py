import cadquery as cq

# Parameters for the geometry
shaft_diameter = 6.0
shaft_radius = shaft_diameter / 2.0
vertical_length = 70.0
horizontal_length = 25.0
head_diameter = 11.0
head_radius = head_diameter / 2.0
head_thickness = 3.0

# 1. Create the Vertical Shaft (Long arm)
# Aligned along the Z-axis, starting from the origin
vertical_shaft = cq.Workplane("XY").circle(shaft_radius).extrude(vertical_length)

# Create the hemispherical dome at the top
# We fillet the top edge with a radius slightly smaller than the shaft radius 
# to avoid geometric kernel singularities, creating a dome shape.
vertical_shaft = vertical_shaft.faces(">Z").edges().fillet(shaft_radius - 0.01)

# 2. Create the Horizontal Shaft (Short arm)
# Aligned along the X-axis, extruding from the vertical shaft's center
horizontal_shaft = cq.Workplane("YZ").circle(shaft_radius).extrude(horizontal_length)

# 3. Create the Head/Flange
# Located at the end of the horizontal shaft
head = (
    cq.Workplane("YZ")
    .workplane(offset=horizontal_length)
    .circle(head_radius)
    .extrude(head_thickness)
)

# Combine the components into a single solid
result = vertical_shaft.union(horizontal_shaft).union(head)

# 4. Create the "D" cut on the Head
# The image shows a flat spot on the bottom of the head, likely so the pin 
# can lie flat on a surface. This aligns the head's bottom with the shaft's bottom.
# We create a large cutting tool positioned below the tangent of the shaft (Z = -radius).
cutter = (
    cq.Workplane("XY")
    .workplane(offset=-shaft_radius)
    .rect(200, 200)  # Large area to ensure it intersects the head
    .extrude(-50)    # Extrude downwards to remove material
)

# Apply the cut
result = result.cut(cutter)