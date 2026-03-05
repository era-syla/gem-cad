import cadquery as cq

# --- Parametric Dimensions ---
disk_diameter = 100.0    # Diameter of the main disk
disk_thickness = 2.5     # Thickness of the disk
center_hole_dia = 2.0    # Diameter of the small central hole

# --- 3D Modeling ---
# 1. Start a workplane on the XY plane
# 2. Draw the outer circle using the radius (diameter / 2)
# 3. Draw the inner circle for the hole (CadQuery handles nested wires as cuts during extrusion)
# 4. Extrude the sketch to create the solid geometry
result = (
    cq.Workplane("XY")
    .circle(disk_diameter / 2.0)
    .circle(center_hole_dia / 2.0)
    .extrude(disk_thickness)
)