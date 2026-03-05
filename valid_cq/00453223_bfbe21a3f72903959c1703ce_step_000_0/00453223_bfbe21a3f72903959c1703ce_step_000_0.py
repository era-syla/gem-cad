import cadquery as cq

# --- Parameters ---
# Main body dimensions
body_width = 20.0     # X-axis length (rectangular part + rounded part)
body_depth = 10.0     # Y-axis thickness
body_height = 45.0    # Z-axis height
fillet_radius = body_depth / 2.0

# Top cap dimensions
cap_offset = 0.8      # Overhang relative to body
cap_height = 5.0

# Bottom boss dimensions
boss_dia = 9.0
boss_height = 10.0

# Worm gear dimensions
worm_dia = 7.5
worm_length = 22.0
worm_pitch = 2.5
# Position: Attached to the right side (+X), near top
worm_x_offset = (body_width / 2.0) + (worm_dia / 2.0) - 1.2
worm_z_top = body_height + cap_height - 2.0

# Rod dimensions
rod_dia = 2.0
rod_length = 35.0

# --- Geometry Construction ---

# 1. Main Body
# Profile: Rectangle centered at origin, then fillet the left side (-X)
# Width covers -10 to 10. Left side fillet r=5 at x=-10.
main_sketch = (
    cq.Sketch()
    .rect(body_width, body_depth)
    .vertices("<X")
    .fillet(fillet_radius)
)

main_body = (
    cq.Workplane("XY")
    .placeSketch(main_sketch)
    .extrude(body_height)
)

# 2. Top Cap
# Similar shape but slightly larger, sitting on top of the main body
cap_sketch = (
    cq.Sketch()
    .rect(body_width + (cap_offset*2), body_depth + (cap_offset*2))
    .vertices("<X")
    .fillet(fillet_radius + cap_offset)
)

top_cap = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .placeSketch(cap_sketch)
    .extrude(cap_height)
)

# 3. Bottom Boss
# Located under the rounded part of the main body.
# The center of the rounded part (fillet center) is at:
# x = -body_width/2 + fillet_radius
boss_center_x = -body_width/2 + fillet_radius

bottom_boss = (
    main_body.faces("<Z").workplane()
    .center(boss_center_x, 0)
    .circle(boss_dia / 2.0)
    .extrude(boss_height)
)

# 4. Worm Gear (Side Feature)
# A vertical cylinder with torus cuts to simulate the helical thread
worm_core = (
    cq.Workplane("XY")
    .workplane(offset=worm_z_top - worm_length)
    .center(worm_x_offset, 0)
    .circle(worm_dia / 2.0)
    .extrude(worm_length)
)

# Create grooves
# We iterate through the length and cut torus shapes
groove_tool = cq.Workplane("XY")
num_grooves = int(worm_length / worm_pitch)

for i in range(num_grooves + 2):
    # Z position for the cut
    z_pos = (worm_z_top - worm_length) + (i * worm_pitch)
    
    if z_pos > worm_z_top or z_pos < (worm_z_top - worm_length):
        continue
        
    # Create a torus solid for the cut
    # Major radius matches cylinder surface approximately
    # Minor radius defines the groove depth/width
    try:
        t = cq.Solid.makeTorus(worm_dia/2.0, worm_pitch/3.2)
        t = t.translate((worm_x_offset, 0, z_pos))
        worm_core = worm_core.cut(cq.Workplane(obj=t))
    except Exception:
        pass

# 5. Connecting Rod / Axle
# Extends horizontally from the side of the Top Cap
# Positioned on the flat face side (+X)
rod = (
    cq.Workplane("YZ")
    .workplane(offset=(body_width/2 + cap_offset)) # Start at the right face of the cap
    .center(0, body_height + cap_height/2.0)     # Vertically centered on cap
    .circle(rod_dia / 2.0)
    .extrude(rod_length)
)

# 6. Top Slot
# Indentation on the top face
top_slot_cut = (
    top_cap.faces(">Z").workplane()
    .center(boss_center_x, 0) # Align with the rounded back part
    .slot2D(6, 2)
    .cutBlind(-1.5)
)

# 7. Assembly
# Combine all parts
result = main_body.union(top_slot_cut).union(bottom_boss).union(worm_core).union(rod)

# Optional: Add fillets to vertical sharp edges on the right side
try:
    result = result.edges("|Z").filterByPosition(lambda p: p.x > 0).fillet(1.0)
except Exception:
    pass