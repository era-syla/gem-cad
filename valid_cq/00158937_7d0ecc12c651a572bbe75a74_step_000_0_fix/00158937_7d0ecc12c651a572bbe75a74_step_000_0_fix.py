import cadquery as cq

# Parameters
L = 40            # distance from center to pillar center
w = 20            # arm width
t = 5             # plate thickness
pillar_d = 8      # pillar diameter
pillar_h = 15     # pillar height
hole_d = 5        # hole diameter
hole_pos = [(10, 0), (0, 10), (-10, 0), (0, -10)]

# Create two perpendicular extruded rectangles and fuse into a cross-shaped plate
rect1 = cq.Workplane("XY").rect(2 * L + w, w).extrude(t)
rect2 = cq.Workplane("XY").rect(w, 2 * L + w).extrude(t)
base = rect1.union(rect2)

# Fillet the vertical edges of the plate for a smooth transition
base = base.edges("|Z").fillet(3)

# Drill holes through the center of the plate
plate_with_holes = base.faces(">Z").workplane().pushPoints(hole_pos).hole(hole_d)

# Add pillars at the ends of each arm
result = plate_with_holes.faces(">Z").workplane().pushPoints(
    [( L,  0), (0,  L), (-L,  0), (0, -L)]
).circle(pillar_d / 2).extrude(pillar_h)