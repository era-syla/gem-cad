import cadquery as cq

# Parametric Dimensions
plate_width = 100.0   # Assumed X dimension
plate_length = 100.0  # Assumed Y dimension
plate_thickness = 5.0 # Assumed Z dimension

# Hole definitions (approximate coordinates based on visual estimation)
# The pattern seems to have some symmetry, possibly for mounting specific components like PCBs or motors.
# Coordinate system: Center of the plate is (0,0)

large_hole_diameter = 4.0
small_hole_diameter = 2.0

# Grouping holes by visual clusters for easier management
# Coordinates are (x, y) relative to center

# Cluster 1 (Bottom Left)
holes_cluster_1 = [
    (-35, -20),
    (-30, -30),
    (-25, -35),
    (-15, -40),
]

# Cluster 2 (Top Left / Center Left)
holes_cluster_2 = [
    (-25, -10),
    (-20, -20),
    (-15, -25),
    (-10, -30),
    (-5, -20),
    (-15, -10),
]

# Cluster 3 (Bottom Right / Center Right)
holes_cluster_3 = [
    (5, 10),
    (15, 20),
    (20, 10),
    (25, 30),
    (30, 20),
    (10, 0),
]

# Cluster 4 (Top Right)
holes_cluster_4 = [
    (15, 30),
    (25, 35),
    (35, 40),
    (40, 20), # Outlier on the right edge
]

# Small mounting holes (corners/periphery)
small_holes = [
    (-40, -10),
    (0, -45),
    (40, 10),
    (0, 45),
]

# Combine large hole lists
large_holes = holes_cluster_1 + holes_cluster_2 + holes_cluster_3 + holes_cluster_4

# Create the base plate
plate = cq.Workplane("XY").box(plate_width, plate_length, plate_thickness)

# Cut the large holes
result = (plate
          .faces(">Z")
          .workplane()
          .pushPoints(large_holes)
          .hole(large_hole_diameter)
          )

# Cut the small holes
result = (result
          .faces(">Z")
          .workplane()
          .pushPoints(small_holes)
          .hole(small_hole_diameter)
          )