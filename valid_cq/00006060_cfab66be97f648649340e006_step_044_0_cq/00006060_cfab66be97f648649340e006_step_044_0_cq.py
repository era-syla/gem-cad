import cadquery as cq

# --- Parametric Dimensions ---
# Dimensions are estimated based on visual proportions of a standard bolt shape
head_diameter = 16.0
head_height = 10.0
shaft_diameter = 8.0
shaft_length = 25.0

# Chamfer/Fillet dimensions
shaft_end_chamfer = 1.0
head_shaft_fillet = 1.0  # Fillet between the head and the shaft
head_top_chamfer = 0.5   # Small chamfer on the top edge of the head (optional but good practice)

# --- Modeling ---

# 1. Create the head
# We start with the larger cylinder
head = cq.Workplane("XY").circle(head_diameter / 2).extrude(head_height)

# 2. Create the shaft
# We extrude the shaft from the bottom face of the head
# Note: The direction is -Z if we built the head upwards, or we can build the shaft from the base
# Let's start a new sketch on the bottom face of the head
part = (
    head.faces("<Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# 3. Add details (Fillets and Chamfers)

# A. Chamfer at the end of the shaft
# Select the edge at the very bottom of the shaft
part = part.edges("<Z").chamfer(shaft_end_chamfer)

# B. Fillet between head and shaft
# This is the edge where the shaft meets the head. 
# It's located at Z = 0 if the head was extruded from XY plane up to +Z.
# However, since we extruded the shaft downwards from the head's bottom face,
# the transition is at the Z-level of the head's bottom face.
# We can select the edge belonging to the shaft base.
# A robust way is to select edges based on the shaft diameter at the specific Z level.
part = part.edges(cq.selectors.RadiusNthSelector(0)).fillet(head_shaft_fillet)

# C. Optional: Chamfer the top of the head
part = part.edges(">Z").chamfer(head_top_chamfer)

# --- Final Result ---
result = part