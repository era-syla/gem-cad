import cadquery as cq

# --- Parametric Dimensions ---
# Diameters
dia_main = 12.0     # Head and Main Shaft
dia_groove1 = 8.5   # First groove (neck)
dia_step = 10.0     # Stepped down section
dia_groove2 = 7.0   # Second groove
dia_hole = 4.0      # Cross hole

# Lengths along Z-axis
len_head = 14.0
len_groove1 = 5.0
len_shaft = 45.0
len_step = 10.0
len_groove2 = 4.0
len_end = 4.0

# --- 3D Modeling ---

# 1. Construct the main body by stacking cylinders (extrusions)
# Start with the Head section at the origin
result = cq.Workplane("XY").circle(dia_main / 2.0).extrude(len_head)

# Add First Groove
result = result.faces(">Z").workplane().circle(dia_groove1 / 2.0).extrude(len_groove1)

# Add Main Shaft section
result = result.faces(">Z").workplane().circle(dia_main / 2.0).extrude(len_shaft)

# Add Stepped down section
result = result.faces(">Z").workplane().circle(dia_step / 2.0).extrude(len_step)

# Add Second Groove
result = result.faces(">Z").workplane().circle(dia_groove2 / 2.0).extrude(len_groove2)

# Add End Cap
result = result.faces(">Z").workplane().circle(dia_step / 2.0).extrude(len_end)

# 2. Cut the transverse hole in the Head section
# We reference the bottom face (<Z), offset to the middle of the head,
# and rotate the workplane 90 degrees to cut perpendicular to the Z-axis.
result = (
    result.faces("<Z")
    .workplane()
    .transformed(
        offset=cq.Vector(0, 0, len_head / 2.0),
        rotate=cq.Vector(90, 0, 0)
    )
    .circle(dia_hole / 2.0)
    .cutThruAll()
)

# 3. Add Chamfer to the final end face for a finished look
result = result.faces(">Z").edges().chamfer(0.5)

# 4. Optional: Add fillets to groove transitions for realism
# Selecting edges based on Z-height to apply fillets to the neck groove
z_groove1_start = len_head
z_groove1_end = len_head + len_groove1
try:
    result = result.edges(
        f"(>Z[{z_groove1_start-0.1}] and <Z[{z_groove1_start+0.1}]) or "
        f"(>Z[{z_groove1_end-0.1}] and <Z[{z_groove1_end+0.1}])"
    ).fillet(0.5)
except Exception:
    # Fallback if edge selection fails due to tolerance issues
    pass