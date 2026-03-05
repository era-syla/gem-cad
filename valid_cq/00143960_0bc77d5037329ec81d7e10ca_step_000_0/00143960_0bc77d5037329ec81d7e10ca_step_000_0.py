import cadquery as cq

# --- Parameters ---
# Head (Block) Dimensions
head_width = 22.0
head_height = 22.0
head_length = 26.0
head_fillet = 4.0
bore_diameter = 10.0
pin_hole_diameter = 2.5

# Joint (Sphere & Neck) Dimensions
neck_radius = 6.0
sphere_radius = 9.5
neck_visible_length = 10.0

# Handle Dimensions
handle_length = 75.0

# --- Geometry Construction ---

# 1. Create the Head (Mounting Block)
# Initial box centered
head = cq.Workplane("XY").box(head_width, head_length, head_height)

# Fillet the longitudinal edges (aligned with Y axis) for the rounded look
head = head.edges("|Y").fillet(head_fillet)

# Slightly fillet the front and back faces to soften edges
head = head.faces("|Y").edges().fillet(1.0)

# Create the main bore hole through the length (Y axis)
head = head.faces(">Y").workplane().hole(bore_diameter)

# Create the small pin hole on the side (X axis)
head = head.faces(">X").workplane().hole(pin_hole_diameter)

# Translate head so its back face is roughly at Y=0 to act as the anchor point
# Box is centered at origin, Y extent is +/- head_length/2
head = head.translate((0, head_length / 2.0, 0))

# 2. Create the Neck (Cylinder connecting head to sphere)
# Determine Y position for the sphere center
sphere_center_y = neck_visible_length + sphere_radius

# Cylinder starts inside the head geometry to ensure solid union
neck = (
    cq.Workplane("XZ", origin=(0, 0, 0))
    .circle(neck_radius)
    .extrude(sphere_center_y)  # Extrude along +Y to sphere center
)

# 3. Create the Ball Joint (Sphere)
sphere = (
    cq.Workplane("XY")
    .transformed(offset=(0, sphere_center_y, 0))
    .sphere(sphere_radius)
)

# 4. Create the Handle (Aerodynamic Loft)
# Use a series of profiles defined on planes perpendicular to the Y axis (XZ planes)
# The loft starts inside the sphere and tapers to a point
handle = (
    cq.Workplane("XZ", origin=(0, sphere_center_y, 0))
    .workplane(offset=2.0).ellipse(7.5, 7.5)          # Profile 1: Inside sphere
    .workplane(offset=10.0).ellipse(10.0, 7.0)        # Profile 2: Transition out of sphere
    .workplane(offset=30.0).ellipse(13.0, 5.5)        # Profile 3: Widest part of handle
    .workplane(offset=handle_length - 42.0).circle(1.0) # Profile 4: Tip
    .loft()
)

# 5. Combine Components
# Union the parts into a single solid
result = head.union(neck).union(sphere).union(handle)

# 6. Apply Fillets to Junctions
# Smooth the transition between Head and Neck
# Select edges near Y=0 (Interface of Head/Neck)
try:
    result = result.edges(cq.selectors.BoxSelector(
        (-15, -2, -15), (15, 5, 15)
    )).fillet(3.0)
except Exception:
    pass

# Smooth the transition around the Sphere (Neck->Sphere and Sphere->Handle)
# Select edges in the bounding box of the sphere intersection
try:
    result = result.edges(cq.selectors.BoxSelector(
        (-15, sphere_center_y - sphere_radius - 2, -15), 
        (15, sphere_center_y + sphere_radius + 2, 15)
    )).fillet(2.0)
except Exception:
    pass

# Export or display result
# show_object(result)