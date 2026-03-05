import cadquery as cq

# Parameters
length = 120.0
flange_width = 20.0
flange_thickness = 3.0
web_thickness = 2.0
total_height = 12.0

# Derived
web_height = total_height - 2 * flange_thickness

# Top flange
top = cq.Workplane("XY") \
    .box(length, flange_width, flange_thickness) \
    .translate((0, 0, web_height/2 + flange_thickness/2))

# Bottom flange
bottom = cq.Workplane("XY") \
    .box(length, flange_width, flange_thickness) \
    .translate((0, 0, -web_height/2 - flange_thickness/2))

# Web
web = cq.Workplane("XY") \
    .box(length, web_thickness, web_height)

# Combine
result = top.union(bottom).union(web)