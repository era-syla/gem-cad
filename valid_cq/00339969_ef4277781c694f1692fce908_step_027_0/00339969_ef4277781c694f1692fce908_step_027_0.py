import cadquery as cq

# --- Dimensions and Parameters ---
thickness = 5.0
edge_fillet = 0.8          # Radius for chamfer/rounding of all edges
tri_outer_corner_r = 4.0   # Radius for the outer corners of the triangle

# Triangle parameters
tri_outer_dia = 65.0       # Circumscribed diameter of outer triangle
tri_inner_dia = 35.0       # Circumscribed diameter of inner triangle hole
tri_pos_y = 35.0           # Y Position of the triangle

# Circle parameters
circ_outer_r = 22.0
circ_inner_r = 13.0
circ_pos_y = -25.0         # Y Position of the circle

# --- Generate Triangle Component ---
# 1. Create the base outer triangle solid
# Use polygon(3) and rotate 90 deg so the vertex points up
tri_base = (cq.Workplane("XY")
            .polygon(3, tri_outer_dia)
            .extrude(thickness)
            .rotate((0, 0, 0), (0, 0, 1), 90))

# 2. Round the vertical outer corners
# Selecting edges parallel to Z axis (|Z)
tri_base = tri_base.edges("|Z").fillet(tri_outer_corner_r)

# 3. Create the inner triangle for the hole
tri_cutout = (cq.Workplane("XY")
              .polygon(3, tri_inner_dia)
              .extrude(thickness)
              .rotate((0, 0, 0), (0, 0, 1), 90))

# 4. Cut the inner shape from the outer base and position it
triangle_part = tri_base.cut(tri_cutout).translate((0, tri_pos_y, 0))

# --- Generate Circle Component ---
# Create a ring by defining outer and inner circles, then extruding
circle_part = (cq.Workplane("XY")
               .circle(circ_outer_r)
               .circle(circ_inner_r)
               .extrude(thickness)
               .translate((0, circ_pos_y, 0)))

# --- Assembly and Finishing ---
# Union the two distinct parts into one object
combined = triangle_part.union(circle_part)

# Apply a final small fillet to all edges to match the smooth, molded look
# This rounds the top/bottom faces and softens the inner cutout corners
result = combined.edges().fillet(edge_fillet)