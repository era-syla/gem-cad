import cadquery as cq

# Dimensions
thickness = 3.0
handle_length = 60.0    # Length from center of hole to the neck
handle_width_end = 12.0 # Width at the rounded end
handle_width_neck = 20.0 # Width at the connection to head
hole_diameter = 6.0

# Head dimensions
# Modeled as a crescent shape formed by two eccentric circles
head_outer_radius = 30.0
head_inner_radius = 20.0
head_outer_center_x = handle_length + 8.0
head_inner_center_x = handle_length - 2.0

# 1. Create the Handle
# Consists of a circle at the origin and a trapezoid tapering outwards
handle_base = (
    cq.Workplane("XY")
    .circle(handle_width_end / 2.0)
    .extrude(thickness)
)

handle_body = (
    cq.Workplane("XY")
    .polyline([
        (0, -handle_width_end / 2.0),
        (handle_length, -handle_width_neck / 2.0),
        (handle_length, handle_width_neck / 2.0),
        (0, handle_width_end / 2.0)
    ])
    .close()
    .extrude(thickness)
)

# 2. Create the Head
# Outer disk minus Inner disk to form a crescent
head_outer = (
    cq.Workplane("XY")
    .moveTo(head_outer_center_x, 0)
    .circle(head_outer_radius)
    .extrude(thickness)
)

head_inner = (
    cq.Workplane("XY")
    .moveTo(head_inner_center_x, 0)
    .circle(head_inner_radius)
    .extrude(thickness)
)

# Create crescent
head = head_outer.cut(head_inner)

# 3. Combine parts
# Union handle parts and the head
# We extend the handle slightly into the head to ensure a clean union if there's a gap
handle_extension = (
    cq.Workplane("XY")
    .moveTo(handle_length, 0)
    .rect(10, handle_width_neck) # Small overlap block
    .extrude(thickness)
    .translate((5, 0, 0)) # Shift to center at handle end
)

part = handle_base.union(handle_body).union(handle_extension).union(head)

# 4. Cut the hole
result = (
    part.faces("<Z")
    .workplane()
    .moveTo(0, 0)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)