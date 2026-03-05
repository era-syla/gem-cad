import cadquery as cq

# Parameters
wing_thickness = 4
dihedral_angle = 5
# Create wing outline
wing2d = cq.Workplane("XY").polyline([(-20, -10), (0, 50), (80, 0), (0, -50)]).close()
# Extrude to wing plate
wing = wing2d.extrude(wing_thickness)
# Split into right and left wing halves with dihedral
right_wing = wing.rotate((0, 0, 0), (1, 0, 0), dihedral_angle)
left_wing = wing.mirror("XZ").rotate((0, 0, 0), (1, 0, 0), -dihedral_angle)
# Fuse wings
wing_assembly = right_wing.union(left_wing)
# Fuselage block mounted on top of wing
# Block is 20×8×20 mm, top of wing is at z=wing_thickness, so center at z=wing_thickness + 20/2
block = cq.Workplane("XY").box(20, 8, 20).translate((0, 0, wing_thickness + 10))
# Vertical fin under wing
# Fin is 4 mm thick (x), 20 mm span (y), 30 mm height (z)
# Bottom of wing is at z=0, so fin center at z = -30/2 = -15
# Attach at x = block's rear face x = -10, minus fin half-thickness 2 = -12
fin = cq.Workplane("XY").box(4, 20, 30).translate((-12, 0, -15))
# Combine all parts
result = wing_assembly.union(block).union(fin)