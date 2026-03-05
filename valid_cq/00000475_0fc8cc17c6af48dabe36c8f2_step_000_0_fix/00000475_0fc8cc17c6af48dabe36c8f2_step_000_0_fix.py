import cadquery as cq

# Main hydraulic cylinder / actuator assembly
# Built from bottom to top

# === BOTTOM SECTION (cylinder body with port block) ===

# Main cylinder body
cylinder_body = (
    cq.Workplane("XY")
    .cylinder(120, 8)
)

# Bottom port block (rectangular block around cylinder)
bottom_block = (
    cq.Workplane("XY")
    .box(22, 18, 16)
    .translate((0, 0, -52))
)

# Port fittings on bottom block
port_fitting1 = (
    cq.Workplane("XY")
    .cylinder(8, 3)
    .translate((11, 0, -52))
)

port_fitting2 = (
    cq.Workplane("XY")
    .cylinder(8, 3)
    .translate((-11, 0, -52))
)

# === TOP SECTION (rod and collar) ===

# Rod (smaller diameter extends from top of cylinder)
rod = (
    cq.Workplane("XY")
    .cylinder(40, 5)
    .translate((0, 0, 80))
)

# Top collar/nut (hexagonal or cylindrical collar)
top_collar = (
    cq.Workplane("XY")
    .cylinder(8, 9)
    .translate((0, 0, 62))
)

# Collar detail ring
collar_ring = (
    cq.Workplane("XY")
    .cylinder(6, 12)
    .translate((0, 0, 70))
)

# Top port block
top_block = (
    cq.Workplane("XY")
    .box(20, 16, 12)
    .translate((0, 0, 58))
)

# === CLEVIS / ROD END (top) ===

# Clevis base cylinder
clevis_base = (
    cq.Workplane("XY")
    .cylinder(6, 5)
    .translate((0, 0, 102))
)

# Clevis fork - left arm
clevis_left = (
    cq.Workplane("XZ")
    .box(3, 12, 6)
    .translate((-5, 0, 108))
)

# Clevis fork - right arm  
clevis_right = (
    cq.Workplane("XZ")
    .box(3, 12, 6)
    .translate((5, 0, 108))
)

# Clevis pin hole (cylinder going through)
clevis_pin = (
    cq.Workplane("XZ")
    .cylinder(5, 14)
    .translate((0, 0, 108))
)

# Eye/ring at top of clevis
clevis_eye = (
    cq.Workplane("XZ")
    .cylinder(7, 4)
    .translate((0, 0, 114))
)

# Eye inner hole
eye_hole = (
    cq.Workplane("XZ")
    .cylinder(4, 5)
    .translate((0, 0, 114))
)

# Neck connecting clevis to rod
neck = (
    cq.Workplane("XY")
    .cylinder(8, 3.5)
    .translate((0, 0, 99))
)

# === ASSEMBLE ===

# Combine all positive volumes
result = (
    cylinder_body
    .union(bottom_block)
    .union(port_fitting1)
    .union(port_fitting2)
    .union(rod)
    .union(top_collar)
    .union(collar_ring)
    .union(top_block)
    .union(clevis_base)
    .union(clevis_left)
    .union(clevis_right)
    .union(clevis_pin)
    .union(clevis_eye)
    .union(neck)
    .cut(eye_hole)
)