import cadquery as cq

R = 5.0
handle_length = 20.0
blade_length = 200.0
thickness_base = 2.0
width_base = 40.0
thickness_tip = 0.5
width_tip = 5.0

# Create the cylindrical handle along the Z axis
handle = cq.Workplane("XY").circle(R).extrude(handle_length)

# Create the tapering blade by lofting between two rectangles
blade = (
    cq.Workplane("XY")
    .workplane(offset=handle_length)
    .rect(thickness_base, width_base)
    .workplane(offset=blade_length)
    .rect(thickness_tip, width_tip)
    .loft()
)

result = handle.union(blade)