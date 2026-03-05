import cadquery as cq
import math

# --- Parameters ---
outer_diameter = 50.0
total_thickness = 5.0
rim_width = 5.0
recess_depth = 2.0
hole_count = 6
hole_diameter = 8.0
hole_pattern_radius = 12.0
fillet_radius = 0.5  # Small chamfer/fillet on the holes and edges

# --- Derived Dimensions ---
inner_recess_diameter = outer_diameter - (2 * rim_width)
base_thickness = total_thickness - recess_depth

# --- Modeling ---

# 1. Create the main disk
# Start with the full cylinder
main_body = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(total_thickness)

# 2. Create the recess (top indentation)
# Cut away the inner circle from the top face down to the base thickness
recess = (
    cq.Workplane("XY")
    .workplane(offset=total_thickness)
    .circle(inner_recess_diameter / 2.0)
    .extrude(-recess_depth, combine=False)
)
main_body = main_body.cut(recess)

# 3. Create the circular hole pattern
# Select the bottom face of the recess (or just project from XY plane at base_thickness)
# We will cut through the remaining material
holes = (
    cq.Workplane("XY")
    .polarArray(hole_pattern_radius, 0, 360, hole_count)
    .circle(hole_diameter / 2.0)
    .extrude(total_thickness, combine=False) # Extrude high enough to cut through
)
main_body = main_body.cut(holes)

# 4. Add fillets/Chamfers
# Looking at the image, the top edges of the holes seem to have a small chamfer or fillet.
# The outer top edge and inner recess edge also look slightly softened.

# Fillet the hole edges on the recessed surface
# We select the face at height 'base_thickness' (Z = 3.0) and then its inner wires (the holes)
try:
    # Select edges of the holes on the recessed face
    # The recessed face is at Z = total_thickness - recess_depth
    recessed_face_z = total_thickness - recess_depth
    
    # We select edges at that specific Z height that belong to the holes
    # A robust way is to select the face, then inner loops
    result = main_body.faces(f"<Z[{total_thickness}]").faces(f">Z[{recessed_face_z-0.1}]").edges("%CIRCLE")
    
    # Apply fillet to the hole edges. Note: selecting specific edges can be tricky in CQ selectors.
    # Let's try a geometric selection based on radius.
    # The hole radius is 4.0. The outer rim inner radius is 20.0.
    result = result.edges(cq.selectors.RadiusNthSelector(0)) # Selects the smallest radius circles (holes)
    result = result.fillet(fillet_radius)
    
    # Optional: Fillet the inner rim edge
    # result = result.edges(cq.selectors.RadiusNthSelector(1)).fillet(fillet_radius)
    
except Exception as e:
    # Fallback if complex selection fails, just return the body with holes
    result = main_body

# If the fillet step above didn't reassign result correctly due to selection logic, ensure result is set
if 'result' not in locals():
    result = main_body
else:
    # If the previous step succeeded, 'result' is the workplane.
    # If the try/except block just assigned result = main_body, we are good.
    pass

# Refine selection for the specific look in the image (chamfer on hole tops)
# Let's do it explicitly on the main_body variable to be safe
final_body = main_body

# Chamfer the top edge of the holes
final_body = (
    final_body.faces(cq.NearestToPointSelector((0, 0, base_thickness)))
    .edges(cq.selectors.RadiusNthSelector(0)) # Smallest radius edges on this face are the holes
    .chamfer(0.5)
)

# Chamfer the inner vertical wall top edge
final_body = (
    final_body.faces(cq.NearestToPointSelector((0, 0, total_thickness))) # Top rim face
    .edges(cq.selectors.RadiusNthSelector(0)) # Inner circle of the rim
    .chamfer(0.5)
)

result = final_body