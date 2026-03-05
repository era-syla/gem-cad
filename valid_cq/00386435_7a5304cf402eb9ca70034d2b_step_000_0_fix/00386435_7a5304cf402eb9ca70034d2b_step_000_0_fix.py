import cadquery as cq

# Parameters
outer_r = 10      # Outer radius of the boss
inner_r = 5       # Radius of the through hole
center_dist = 60  # Distance between boss centers
thickness = 8     # Thickness of the part

# Create the central body
body = cq.Workplane("XY").rect(center_dist, 2*outer_r).extrude(thickness)

# Create the left and right bosses
boss1 = cq.Workplane("XY").center(center_dist/2, 0).circle(outer_r).extrude(thickness)
boss2 = cq.Workplane("XY").center(-center_dist/2, 0).circle(outer_r).extrude(thickness)

# Combine body and bosses
result = body.union(boss1).union(boss2)

# Drill through-holes in the bosses
result = result.faces(">Z").workplane().pushPoints([
    ( center_dist/2, 0),
    (-center_dist/2, 0)
]).hole(inner_r * 2)

# Final result
result