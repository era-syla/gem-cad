import cadquery as cq

# Parameters
L = 120.0    # overall length of the plate
W = 10.0     # width of the plate
T = 5.0      # thickness of the plate
R = W / 2    # radius for the rounded ends
hole_d = 4.0 # diameter of the holes

# Compute hole X positions at the two ends and center
hole_positions = [
    (-L/2 + R, 0),
    (0, 0),
    ( L/2 - R, 0),
]

# Build center rectangular section
rect_section = cq.Workplane("XY").rect(L - 2*R, W).extrude(T)

# Build end caps as extruded half-cylinders
end1 = cq.Workplane("XY").center(-L/2 + R, 0).circle(R).extrude(T)
end2 = cq.Workplane("XY").center( L/2 - R, 0).circle(R).extrude(T)

# Combine all parts
plate = rect_section.union(end1).union(end2)

# Drill holes through the top face
result = plate.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_d)