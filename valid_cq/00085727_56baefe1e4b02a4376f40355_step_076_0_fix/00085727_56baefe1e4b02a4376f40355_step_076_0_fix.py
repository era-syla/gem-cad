import cadquery as cq

# Parameters
num_bars = 8
bar_radius = 10
bar_width = 5
bar_depth = 3
bar_height = 50
stem_radius = 0.5
stem_height = 150

# Create central stem
stem = cq.Workplane("XY").circle(stem_radius).extrude(stem_height)

# Create surrounding bars
bars = cq.Workplane("XY")
for i in range(num_bars):
    angle = 360.0 * i / num_bars
    bars = bars.union(
        cq.Workplane("XY")
          .transformed(offset=(bar_radius, 0, 0), rotate=(0, 0, angle))
          .rect(bar_width, bar_depth)
          .extrude(bar_height)
    )

# Combine stem and bars
result = stem.union(bars)