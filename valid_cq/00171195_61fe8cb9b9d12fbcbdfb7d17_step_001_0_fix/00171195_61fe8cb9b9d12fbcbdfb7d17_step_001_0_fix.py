import cadquery as cq

# Parameters
length = 100.0  # overall length
width = 20.0    # overall width (diameter of end circles)
height = 8.0    # overall thickness
wall = 3.0      # side wall thickness
hole_dia = 8.0  # diameter of through holes
pocket_depth = 5.0  # depth of central pocket

# Build the base: rectangle plus two end-caps
rect = cq.Workplane("XY").rect(length - width, width).extrude(height)
left_cap = cq.Workplane("XY").center((length - width) / 2, 0).circle(width / 2).extrude(height)
right_cap = cq.Workplane("XY").center(-(length - width) / 2, 0).circle(width / 2).extrude(height)
base = rect.union(left_cap).union(right_cap)

# Subtract the central pocket
pocket_length = (length - width) - 2 * wall
pocket_width = width - 2 * wall
pocket = (
    cq.Workplane("XY", origin=(0, 0, height))
      .rect(pocket_length, pocket_width)
      .extrude(-pocket_depth)
)
result = base.cut(pocket)

# Drill the two through holes at the ends
hole_centers = [((length - width) / 2, 0), (-(length - width) / 2, 0)]
result = (
    result.faces(">Z")
          .workplane()
          .pushPoints(hole_centers)
          .hole(hole_dia)
)