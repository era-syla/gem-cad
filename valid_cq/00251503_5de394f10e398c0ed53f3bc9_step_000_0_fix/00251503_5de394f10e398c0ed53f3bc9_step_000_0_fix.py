import cadquery as cq

# Parameters (modify as needed)
outer_dia = 20.0       # Outer diameter of the tube
thickness = 1.5        # Wall thickness
length = 150.0         # Total length of the tube
hole_dia = 2.0         # Diameter of the axial holes

inner_dia = outer_dia - 2.0 * thickness

# Create the solid outer tube
outer = cq.Workplane("XY").circle(outer_dia / 2.0).extrude(length)

# Subtract the inner cylinder to make it hollow, leaving a bottom cap of thickness
inner = (
    cq.Workplane("XY")
    .circle(inner_dia / 2.0)
    .extrude(length - thickness)
    .translate((0, 0, thickness))
)
result = outer.cut(inner)

# Add two axial holes on the open end face
# Position them at the mid‐thickness of the wall, on opposite sides
hole_radius = outer_dia / 2.0 - thickness / 2.0
points = [( hole_radius, 0), (-hole_radius, 0)]
result = result.faces(">Z").workplane().pushPoints(points).hole(hole_dia)

# 'result' now contains the final solid
print(result)  # optional, to confirm creation in a script environment