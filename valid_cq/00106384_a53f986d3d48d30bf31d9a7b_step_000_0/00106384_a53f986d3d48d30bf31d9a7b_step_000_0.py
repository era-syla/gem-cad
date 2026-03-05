import cadquery as cq

# --- Parametric Dimensions ---
height = 100.0        # Total height of the unit
width = 55.0          # Width of the unit
thickness = 10.0      # Thickness of the curved body
curve_radius = 120.0  # Radius of the front/back curvature
fillet_vert = 3.0     # Fillet radius for the vertical side corners
fillet_edge = 1.0     # Fillet radius for the top and bottom edges

# --- Modeling ---

# 1. Create the base curved shape (infinite width)
# We position the center of curvature such that the front face apex is at the origin (0,0) in XY.
center_y = -curve_radius

# Create the outer cylinder (defining the front convex face)
outer_cyl = (
    cq.Workplane("XY")
    .moveTo(0, center_y)
    .circle(curve_radius)
    .extrude(height)
)

# Create the inner cylinder (defining the back concave face)
inner_cyl = (
    cq.Workplane("XY")
    .moveTo(0, center_y)
    .circle(curve_radius - thickness)
    .extrude(height)
)

# Create the curved shell by subtracting the inner cylinder from the outer
shell = outer_cyl.cut(inner_cyl)

# 2. Define the rectangular footprint to trim the sides
# Use a box centered at origin with the target width. 
# Depth (Y) is large enough to ensure it fully intersects the shell.
trimmer_box = (
    cq.Workplane("XY")
    .rect(width, curve_radius * 2) 
    .extrude(height)
)

# Intersect the shell with the box to get the curved rectangular panel
body = shell.intersect(trimmer_box)

# 3. Apply detailed features
# Apply fillets to the four vertical corners
result = body.edges("|Z").fillet(fillet_vert)

# Apply fillets to the top and bottom loops (edges perpendicular to Z)
result = result.edges("#Z").fillet(fillet_edge)