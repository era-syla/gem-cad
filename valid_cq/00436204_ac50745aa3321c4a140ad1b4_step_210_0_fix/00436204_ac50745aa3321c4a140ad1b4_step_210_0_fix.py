import cadquery as cq
from math import cos, sin, radians

# Parameters
plate_th = 3        # Plate thickness (X dimension)
plate_depth = 10    # Plate depth (Y dimension)
plate_height = 140  # Plate height (Z dimension)
gap = 30            # Gap between inner faces (Y dimension)

large_dia = 6       # Diameter of large holes
small_dia = 2       # Diameter of small holes in clusters
small_r = 5         # Radius of small-hole cluster around each large hole

# Create array of Z positions for hole rows
rows = 8
z_margin = 15
z_spacing = (plate_height - 2 * z_margin) / (rows - 1)
z_positions = [z_margin + i * z_spacing for i in range(rows)]

# Offsets for small-hole cluster (6 holes at 60° increments)
cluster_offsets = [(small_r * cos(radians(a)), small_r * sin(radians(a))) for a in range(0, 360, 60)]

# Build first plate (left)
plate1 = cq.Workplane("XY").box(plate_th, plate_depth, plate_height)
# Cut large holes on inner face
plate1 = plate1.faces(">Y").workplane().pushPoints([(0, z) for z in z_positions]).hole(large_dia)
# Cut small-hole clusters on same face
small_pts1 = []
for z in z_positions:
    for dx, dy in cluster_offsets:
        small_pts1.append((dx, z + dy))
plate1 = plate1.faces(">Y").workplane().pushPoints(small_pts1).hole(small_dia)

# Build second plate (right), shifted in Y
y_offset = gap + plate_depth
plate2 = cq.Workplane("XY").box(plate_th, plate_depth, plate_height).translate((0, y_offset, 0))
# Cut large holes on inner face of second plate
plate2 = plate2.faces("<Y").workplane().pushPoints([(0, z) for z in z_positions]).hole(large_dia)
# Cut small-hole clusters on inner face of second plate (invert cluster Y offsets)
small_pts2 = []
for z in z_positions:
    for dx, dy in cluster_offsets:
        small_pts2.append((dx, z - dy))
plate2 = plate2.faces("<Y").workplane().pushPoints(small_pts2).hole(small_dia)

# Combine and finalize
result = plate1.union(plate2)