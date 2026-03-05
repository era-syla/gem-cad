import cadquery as cq

# Parameters
n_sides = 5
base_diameter = 40.0
height = 30.0
apex_scale = 0.01  # tiny top polygon to approximate a point
twist_angle = 72.0  # rotate top pyramid by one side angle

# Bottom pyramid: base at Z=0, apex at Z=-height
bottom_pyramid = (
    cq.Workplane("XY")
      .polygon(n_sides, base_diameter)
      .workplane(offset=-height)
      .polygon(n_sides, base_diameter * apex_scale)
      .loft(combine=True)
)

# Top pyramid: base at Z=0, apex at Z=+height, rotated by twist_angle
top_pyramid = (
    cq.Workplane("XY")
      .rotate((0, 0, 0), (0, 0, 1), twist_angle)
      .polygon(n_sides, base_diameter)
      .workplane(offset= height)
      .polygon(n_sides, base_diameter * apex_scale)
      .loft(combine=True)
)

# Union the two pyramids into one solid
result = bottom_pyramid.union(top_pyramid)