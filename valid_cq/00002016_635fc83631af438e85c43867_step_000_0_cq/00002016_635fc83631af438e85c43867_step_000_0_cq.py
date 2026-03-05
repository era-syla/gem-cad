import cadquery as cq

# --- Parameters ---
outer_diameter = 100.0   # Overall diameter of the part
outer_rim_height = 10.0  # Height of the thin outer wall
rim_thickness = 2.0      # Thickness of the outer wall

base_thickness = 8.0     # Thickness of the main solid disc
central_recess_dia = 50.0 # Diameter of the central depression
central_recess_depth = 4.0 # Depth of the central depression
center_hole_dia = 10.0   # Diameter of the through-hole

# --- Modeling ---

# 1. Create the main solid disc body
# We start with a cylinder representing the bulk of the material.
main_body = cq.Workplane("XY").circle(outer_diameter / 2 - rim_thickness).extrude(base_thickness)

# 2. Create the outer rim
# This is a thin cylindrical shell on the outside.
# We create a solid cylinder and cut out the inside, or extrude a ring.
# Let's extrude a ring from the bottom plane.
outer_rim = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(outer_diameter / 2 - rim_thickness)
    .extrude(outer_rim_height)
)

# 3. Create the central recess
# We cut a circular pocket into the top of the main body.
# Note: The main body height is 'base_thickness'.
recess_cut = (
    main_body.faces(">Z")
    .workplane()
    .circle(central_recess_dia / 2)
    .cutBlind(-central_recess_depth)
)

# 4. Create the center through-hole
# This goes through the entire part.
final_shape = (
    recess_cut
    .faces(">Z")
    .workplane()
    .circle(center_hole_dia / 2)
    .cutThruAll()
)

# 5. Combine the rim and the modified body
# If the rim is taller than the body, we need to union them.
result = final_shape.union(outer_rim)

# Optional: Add a small chamfer or fillet to the recess edge for a more realistic look
# visible in the render (the edge of the recess looks soft)
# result = result.edges(cq.selectors.RadiusNthSelector(2)).fillet(1.0) # Selecting edges can be tricky without tags

# For robustness, let's just stick to the primary geometry which is cleaner.
# The image shows a very distinct "lip" or separation between the outer rim and the inner disc,
# suggesting they might be connected at the bottom or the rim stands proud.
# The union operation handles the connection.

# Export the result
if __name__ == "__main__":
    try:
        from cadquery import exporters
        exporters.export(result, "result.step")
    except ImportError:
        pass