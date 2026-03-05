import cadquery as cq

# Parameters
length = 100
width = 20
base_height = 5
rib_height = 10
rib_count = 10

# Calculate pitch for ribs
pitch = length / rib_count

# Build 2D profile in the XZ plane
points = [(0, 0), (0, base_height)]
for i in range(rib_count):
    peak_x = (i + 0.5) * pitch
    points.append((peak_x, base_height + rib_height))
    points.append(((i + 1) * pitch, base_height))
points.append((length, 0))

# Create the solid by extruding the profile in Y
result = (
    cq.Workplane("XZ")
      .polyline(points)
      .close()
      .extrude(width)
)