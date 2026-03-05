import cadquery as cq

# Parameters
base_width = 100
height = 150
thickness = 10

small_hole_dia = 5
big_hole_dia = 20
cbore_dia = 30
cbore_depth = 3

tri_small_w = 20
tri_small_h = 30
tri_large_w = 40
tri_large_h = 60

# Create main triangular plate
result = (
    cq.Workplane("XY")
      .polyline([(-base_width/2, 0), (base_width/2, 0), (0, -height)])
      .close()
      .extrude(thickness)
)

# Counterbored central big hole
result = (
    result
      .faces(">Z")
      .workplane()
      .center(0, -height/3)
      .cboreHole(big_hole_dia, cbore_dia, cbore_depth)
)

# Small mounting holes (3 on top edge, 2 near bottom)
small_holes = [
    (-base_width/2 + 15, 5),
    (0, 5),
    (base_width/2 - 15, 5),
    (-15, -height + 15),
    (15, -height + 15),
]
result = (
    result
      .faces(">Z")
      .workplane()
      .pushPoints(small_holes)
      .hole(small_hole_dia)
)

# Triangular cutouts near top
top_tri_centers = [
    (-base_width/4, -height * 0.2),
    (base_width/4, -height * 0.2),
]
for x, y in top_tri_centers:
    result = (
        result
          .faces(">Z")
          .workplane()
          .center(x, y)
          .polyline([
              (-tri_small_w/2, 0),
              ( tri_small_w/2, 0),
              (0, -tri_small_h),
          ])
          .close()
          .cutBlind(-thickness)
    )

# Large triangular cutout near bottom
result = (
    result
      .faces(">Z")
      .workplane()
      .center(0, -height * 0.6)
      .polyline([
          (-tri_large_w/2, 0),
          ( tri_large_w/2, 0),
          (0, -tri_large_h),
      ])
      .close()
      .cutBlind(-thickness)
)