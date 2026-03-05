import cadquery as cq

# --- Parametric Dimensions ---
# Dimensions estimated from the visual proportions of the image

# Large circle (base)
large_radius = 20.0
large_height = 10.0

# Middle circle
mid_radius = 12.0
mid_height = 8.0
mid_offset = 25.0  # Center-to-center distance from the large circle

# Small circle (end)
small_radius = 8.0
small_height = 6.0
small_offset = 16.0 # Center-to-center distance from the middle circle

# Fillet radius for top edges
fillet_radius = 1.5

# --- Modeling ---

# 1. Create the largest cylinder at the origin
part = cq.Workplane("XY").circle(large_radius).extrude(large_height)

# 2. Create the middle cylinder
# We move the workplane center to the right and extrude
mid_cylinder = (
    cq.Workplane("XY")
    .center(mid_offset, 0)
    .circle(mid_radius)
    .extrude(mid_height)
)

# 3. Create the smallest cylinder
# We move the workplane center further to the right relative to the middle one
small_cylinder = (
    cq.Workplane("XY")
    .center(mid_offset + small_offset, 0)
    .circle(small_radius)
    .extrude(small_height)
)

# 4. Union (fuse) the shapes together
result = part.union(mid_cylinder).union(small_cylinder)

# 5. Apply fillets
# The image shows rounded top edges on all cylinders.
# We select edges that are at the top (Z max) for each "level" or simply all top edges.
# A robust way is to select edges belonging to the top face.
result = result.faces(">Z").edges().fillet(fillet_radius)

# Optional: Fillet the vertical intersection edges if desired, but the image mainly highlights top edge fillets.
# The intersections look fairly sharp or naturally blended in the render, 
# but adding a small fillet at the "neck" between circles makes it more realistic.
# Let's add a small fillet to vertical edges to smooth the transition.
result = result.edges("|Z").fillet(1.0)

# Return the final result
if "show_object" in locals():
    show_object(result)