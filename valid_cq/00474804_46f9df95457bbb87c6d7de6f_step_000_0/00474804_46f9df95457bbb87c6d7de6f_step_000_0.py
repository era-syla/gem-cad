import cadquery as cq

# Geometric Parameters
shaft_radius = 8.0       # Radius of the main cylindrical shaft
total_length = 65.0      # Total length of the part
head_length = 20.0       # Length of the cross-shaped section
shaft_length = total_length - head_length
fin_thickness = 7.0      # Thickness of the cross arms (fins)
fin_span = 28.0          # Total span of the cross arms (tip to tip)

# 1. Create the base shaft
# This creates a cylinder representing the core of the entire part
shaft = cq.Workplane("XY").circle(shaft_radius).extrude(total_length)

# 2. Create the cross/fin features
# We define a workplane at the transition point between the plain shaft and the head
# We sketch two orthogonal rectangles to form the cross shape
fins = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .rect(fin_thickness, fin_span)  # First arm of the cross
    .rect(fin_span, fin_thickness)  # Second arm of the cross
    .extrude(head_length)
)

# 3. Combine the shaft and the fins into the final solid
result = shaft.union(fins)