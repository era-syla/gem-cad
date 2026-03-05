import cadquery as cq

# Parameters
Lcc = 60      # center-to-center distance of end circles
D_end = 15    # diameter of end circles
D_arm = 6     # width of the rectangular arm
H = 4         # thickness in Z-direction
hole_d = 6    # diameter of the through holes
r_fillet = 2  # fillet radius on vertical edges

# Compute the length of the rectangular arm between the circles
link_length = Lcc - D_end

# Create the rectangular arm
body = cq.Workplane("XY").rect(link_length, D_arm).extrude(H)

# Create the two end lobes
end1 = cq.Workplane("XY").center(-Lcc/2, 0).circle(D_end/2).extrude(H)
end2 = cq.Workplane("XY").center( Lcc/2, 0).circle(D_end/2).extrude(H)

# Combine the arm and the lobes
result = body.union(end1).union(end2)

# Fillet all vertical external edges
result = result.edges("|Z").fillet(r_fillet)

# Drill the through holes at the center of each lobe
result = (
    result
      .faces(">Z")
      .workplane()
      .pushPoints([(-Lcc/2, 0), (Lcc/2, 0)])
      .hole(hole_d)
)