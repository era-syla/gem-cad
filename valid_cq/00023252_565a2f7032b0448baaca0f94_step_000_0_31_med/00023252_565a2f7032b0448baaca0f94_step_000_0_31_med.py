import cadquery as cq
import math

# Parameters for the structural metal strip
P = 16.0          # Pitch between large holes
W = 24.0          # Width of the strip
thickness = 2.0   # Thickness of the strip
D_large = 8.0     # Diameter of the large holes
D_small = 3.0     # Diameter of the small holes
R_cluster = P / 2.0 # Radius of the 8-hole cluster around specific large holes
L_centers = 12 * P  # Distance between the centers of the outermost large holes

# Create the base strip with rounded ends
result = (cq.Workplane("XY")
          .slot2D(L_centers, W)
          .extrude(thickness))

# Drill the large holes along the center line
# There are 13 large holes in total, centered at the origin
large_hole_xs = [i * P for i in range(-6, 7)]
result = (result.faces(">Z").workplane()
          .pushPoints([(x, 0) for x in large_hole_xs])
          .hole(D_large))

# Drill the small holes along the center line
# These are located exactly halfway between every large hole, plus the ends
small_hole_xs = [(i + 0.5) * P for i in range(-7, 7)]
result = (result.faces(">Z").workplane()
          .pushPoints([(x, 0) for x in small_hole_xs])
          .hole(D_small))

# Drill the remaining small holes for the 8-hole clusters
# The clusters are located at indices 0, 3, 6, 9, 12 (every 3rd hole)
cluster_xs = [-6 * P, -3 * P, 0, 3 * P, 6 * P]
cluster_pts = []

# For each cluster, the left and right holes (0 and 180 deg) are already
# created by the center-line small holes. We only need the remaining 6 holes.
for cx in cluster_xs:
    for angle_deg in [45, 90, 135, 225, 270, 315]:
        angle_rad = math.radians(angle_deg)
        x = cx + R_cluster * math.cos(angle_rad)
        y = R_cluster * math.sin(angle_rad)
        cluster_pts.append((x, y))

result = (result.faces(">Z").workplane()
          .pushPoints(cluster_pts)
          .hole(D_small))