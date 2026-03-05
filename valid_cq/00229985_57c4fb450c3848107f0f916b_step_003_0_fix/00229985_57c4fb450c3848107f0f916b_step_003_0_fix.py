import cadquery as cq

# Parameters
thickness = 10.0     # depth of the part (Y direction)
base_r = 8.0         # radius of the bottom boss
top_w = 5.0          # width of the lever at the top
height = 100.0       # length of the lever (Z direction)
fillet_radius = 2.0  # fillet radius on lever edges

# Create the bottom cylindrical boss
boss = (
    cq.Workplane("XZ")
      .circle(base_r)
      .extrude(thickness)
)

# Create the tapered lever
lever_profile = [
    (-top_w/2, height),
    ( top_w/2, height),
    ( base_r,   0   ),
    (-base_r,   0   )
]
lever = (
    cq.Workplane("XZ")
      .polyline(lever_profile)
      .close()
      .extrude(thickness)
      .edges("|Y")
      .fillet(fillet_radius)
)

# Combine boss and lever
result = boss.union(lever)