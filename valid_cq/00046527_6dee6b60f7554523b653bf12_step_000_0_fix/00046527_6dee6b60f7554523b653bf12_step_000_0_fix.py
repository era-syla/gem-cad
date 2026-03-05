import cadquery as cq

# Define the main fuselage
fuselage = cq.Workplane("XY").circle(5).extrude(45)

# Define the wings
wing = (cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(30, 5)
        .lineTo(30, -5)
        .close()
        .extrude(2))

# Position and mirror wings
wing_right = wing.translate((15, 0, 5))
wing_left = wing.mirror("YZ").translate((-15, 0, 5))

# Define the tail
tail = (cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(12, 3)
        .lineTo(12, -3)
        .close()
        .extrude(1.5))

# Position and mirror tail
v_tail_right = tail.translate((20, 0, 30))
v_tail_left = tail.mirror("YZ").translate((-20, 0, 30))

# Define horizontal stabilizer
h_stab = (cq.Workplane("XY")
          .moveTo(0, 0)
          .lineTo(8, 2)
          .lineTo(8, -2)
          .close()
          .extrude(1))
h_stab = h_stab.translate((0, 0, 28))

# Assemble the airplane
result = (fuselage
          .union(wing_right)
          .union(wing_left)
          .union(v_tail_right)
          .union(v_tail_left)
          .union(h_stab))