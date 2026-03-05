import cadquery as cq

# Parameters
pitch = 40
base_h = 12
r = 6
thickness = 5
n = 4

# Build and union the repeated module bodies
modules = []
for i in range(n):
    mod = (
        cq.Workplane("XY")
        .transformed(offset=(i * pitch, 0, 0))
        .polyline([
            (0, 0),
            (pitch, 0),
            (pitch, base_h),
            (pitch/2 + r, base_h),
        ])
        .radiusArc((pitch/2, base_h + r), r)
        .radiusArc((pitch/2 - r, base_h), r)
        .lineTo(0, base_h)
        .close()
        .extrude(thickness)
    )
    modules.append(mod)

result = modules[0]
for m in modules[1:]:
    result = result.union(m)

# Prepare hole and slot centers
large_hole_centers = [(i * pitch + pitch/2, base_h/2) for i in range(n)]
small_slot_centers = [(i * pitch + pitch/2, base_h/4) for i in range(n)]
top_hole_centers = []
offset_x = r - 2
y_top = base_h + r - 2
for i in range(n):
    x0 = i * pitch + pitch/2
    top_hole_centers.append((x0 - offset_x, y_top))
    top_hole_centers.append((x0 + offset_x, y_top))
bottom_hole_centers = [(i * pitch + pitch/2, 0) for i in range(n)]

# Cut out holes and slots
result = (
    result
    .faces(">Z").workplane()
    .pushPoints(large_hole_centers).hole(15)
    .pushPoints(bottom_hole_centers).hole(5)
    .pushPoints(top_hole_centers).hole(4)
    .pushPoints(small_slot_centers).rect(8, 4).cutThruAll()
)

# 'result' now contains the final geometry.