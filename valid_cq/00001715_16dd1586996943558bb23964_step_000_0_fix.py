import cadquery as cq
import math

# Radial aircraft engine with propeller
# Main engine crankcase (central body)
crankcase = (
    cq.Workplane("XY")
    .sphere(30)
)

# Flatten into oblate spheroid approximation using scaling
crankcase = (
    cq.Workplane("XY")
    .cylinder(25, 30)
)

# Add front nose cone
nose = (
    cq.Workplane("XY")
    .workplane(offset=25)
    .circle(15)
    .workplane(offset=20)
    .circle(5)
    .loft()
)

# Add rear section
rear = (
    cq.Workplane("XY")
    .workplane(offset=-25)
    .circle(20)
    .workplane(offset=-15)
    .circle(10)
    .loft()
)

# Combine main body
engine_body = crankcase.union(nose).union(rear)

# Add propeller spinner cap
spinner = (
    cq.Workplane("XY")
    .workplane(offset=45)
    .sphere(8)
)

engine_body = engine_body.union(spinner)

# Create cylinders arranged radially (7-cylinder radial engine)
num_cylinders = 7
cylinder_radius_offset = 35
cylinder_r = 7
cylinder_h = 30

cylinders = None
for i in range(num_cylinders):
    angle = (2 * math.pi / num_cylinders) * i
    x = cylinder_radius_offset * math.cos(angle)
    y = cylinder_radius_offset * math.sin(angle)
    
    # Cylinder body
    cyl = (
        cq.Workplane("XY")
        .center(x, y)
        .cylinder(cylinder_h, cylinder_r)
    )
    
    # Cooling fins on each cylinder
    for f in range(6):
        fin_z = -10 + f * 4
        fin = (
            cq.Workplane("XY")
            .workplane(offset=fin_z)
            .center(x, y)
            .circle(cylinder_r + 2)
            .extrude(1.5)
        )
        cyl = cyl.union(fin)
    
    # Cylinder head (rounded top)
    head = (
        cq.Workplane("XY")
        .workplane(offset=15)
        .center(x, y)
        .sphere(cylinder_r * 1.1)
    )
    cyl = cyl.union(head)
    
    if cylinders is None:
        cylinders = cyl
    else:
        cylinders = cylinders.union(cyl)

engine_body = engine_body.union(cylinders)

# Create propeller
# Two-blade propeller
blade_length = 130
blade_width = 12
blade_thickness = 3

blade1 = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(blade_length/2, 55)
    .box(blade_length, blade_thickness, blade_width)
)

blade2 = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(-blade_length/2, 55)
    .box(blade_length, blade_thickness, blade_width)
)

# Taper the blades by creating tapered shapes
blade1_tapered = (
    cq.Workplane("XY")
    .workplane(offset=53)
    .center(70, 0)
    .rect(blade_length * 0.8, blade_width * 0.5)
    .workplane(offset=blade_thickness)
    .center(70, 0)
    .rect(blade_length, blade_width)
    .loft()
)

# Use simple box blades with twist approximation
prop_hub = (
    cq.Workplane("XY")
    .workplane(offset=48)
    .cylinder(10, 8)
)

propeller = (
    cq.Workplane("YZ")
    .workplane(offset=52)
    .center(0, 0)
    .box(blade_length * 2, blade_width, blade_thickness)
)

# Add slight sweep to propeller by rotating
propeller = propeller.union(prop_hub)

# Mount frame / engine mount struts
for i in range(num_cylinders):
    angle = (2 * math.pi / num_cylinders) * i
    x1 = cylinder_radius_offset * math.cos(angle)
    y1 = cylinder_radius_offset * math.sin(angle)
    x2 = (cylinder_radius_offset + 5) * math.cos(angle)
    y2 = (cylinder_radius_offset + 5) * math.sin(angle)
    
    strut = (
        cq.Workplane("XY")
        .center(x1 * 0.6, y1 * 0.6)
        .cylinder(8, 2)
    )
    engine_body = engine_body.union(strut)

# Combine everything
result = engine_body.union(propeller)