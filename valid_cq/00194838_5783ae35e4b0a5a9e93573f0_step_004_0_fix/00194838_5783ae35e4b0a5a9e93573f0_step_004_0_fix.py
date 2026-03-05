import cadquery as cq

# Define fork end profile
fork_end_profile = cq.Workplane("XY").polygon(6, 20).extrude(5)

# Define upper arm
upper_arm = cq.Workplane("YZ").move(5, 0).lineTo(100, 0).lineTo(100, 5).lineTo(5, 5).close().extrude(50)

# Define lower arm
lower_arm = cq.Workplane("YZ").move(5, 0).lineTo(150, 0).lineTo(150, 5).lineTo(5, 5).close().extrude(50)

# Assemble the frame by positioning the components
result = (fork_end_profile.faces(">Z").workplane()
          .transformed(offset=(10, 0, 0))
          .union(upper_arm)
          .faces(">Z").workplane()
          .transformed(offset=(0, 0, 20))
          .union(lower_arm))

# Add additional details or fillets as needed
result = result.edges("|Z").fillet(2)