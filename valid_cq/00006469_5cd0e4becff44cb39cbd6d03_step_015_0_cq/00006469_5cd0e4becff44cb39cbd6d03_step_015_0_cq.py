import cadquery as cq

# -- Parametric Dimensions --
height = 60.0    # Overall height of the block
width = 30.0     # Overall width of the block
thickness = 15.0 # Thickness of the block

# Corner fillet radius
fillet_radius = 5.0

# Large holes (Threaded-look)
large_hole_diam = 12.0
large_hole_spacing = 30.0 # Distance between centers of large holes

# Small holes
small_hole_diam = 4.0
small_hole_spacing = 22.0 # Distance between centers of small holes

# -- Modeling Strategy --
# 1. Create the base rectangular block.
# 2. Apply fillets to the four corners perpendicular to the thickness.
# 3. Create the two large holes along the Y-axis.
# 4. Create the two small holes along the X-axis.
# Note: Since CadQuery doesn't render actual threads easily for visuals without heavy geometry, 
# standard cylindrical holes will represent the "threaded" holes shown in the image.

# 1. Base Block
result = cq.Workplane("XY").box(width, height, thickness)

# 2. Fillet Vertical Edges
# Select edges parallel to Z axis that are on the outer perimeter
result = result.edges("|Z").fillet(fillet_radius)

# 3. Large Holes (Top and Bottom)
# Locations: (0, large_hole_spacing/2) and (0, -large_hole_spacing/2)
result = result.faces(">Z").workplane().pushPoints([
    (0, large_hole_spacing / 2.0),
    (0, -large_hole_spacing / 2.0)
]).hole(large_hole_diam)

# 4. Small Holes (Left and Right)
# Locations: (small_hole_spacing/2, 0) and (-small_hole_spacing/2, 0)
result = result.faces(">Z").workplane().pushPoints([
    (small_hole_spacing / 2.0, 0),
    (-small_hole_spacing / 2.0, 0)
]).hole(small_hole_diam)

# Return the final result
# (The variable 'result' is already set)