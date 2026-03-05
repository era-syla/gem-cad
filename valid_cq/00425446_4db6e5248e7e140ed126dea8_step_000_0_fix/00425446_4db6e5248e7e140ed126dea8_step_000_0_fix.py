import cadquery as cq

v_leg_base_width = 20
v_leg_height = 60
v_leg_thickness = 10

result = (cq.Workplane("XY")
          .moveTo(0, 0)
          .vLine(v_leg_height)
          .hLine(v_leg_base_width)
          .vLine(-v_leg_height / 2)
          .close()
          .extrude(v_leg_thickness)
          .edges("|Z")
          .fillet(3))