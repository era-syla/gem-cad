import cadquery as cq

# Parametric dimensions
knob_diameter = 40.0      # Main diameter of the knob head
knob_height = 12.0        # Height of the cylindrical part of the head
top_flat_diameter = 30.0  # Diameter of the flat top surface
chamfer_height = 4.0      # Vertical height of the angled top section
stem_diameter = 18.0      # Diameter of the base stem
stem_height = 10.0        # Height of the base stem

# Create the main body of the knob
# We'll construct this by revolving a profile or stacking cylinders/cones.
# Stacking primitives is often simpler and more readable.

# 1. The stem (base cylinder)
stem = cq.Workplane("XY").circle(stem_diameter / 2).extrude(stem_height)

# 2. The main cylindrical part of the head
# We start this on top of the stem
head_base = (
    stem.faces(">Z")
    .workplane()
    .circle(knob_diameter / 2)
    .extrude(knob_height - chamfer_height)
)

# 3. The top chamfered/conical section
# This is a loft or a cone frustum on top of the head base
# We want to go from knob_diameter to top_flat_diameter over chamfer_height
head_top = (
    head_base.faces(">Z")
    .workplane()
    .circle(knob_diameter / 2)  # Base circle of the cone
    .workplane(offset=chamfer_height)
    .circle(top_flat_diameter / 2)  # Top circle of the cone
    .loft(combine=True)
)

# Combine into final result
result = head_top

# Alternatively, a more robust way using a revolution profile
# This handles the geometry more cleanly as a single operation
def knob_profile():
    # Define points for the cross-section
    # (r, z) coordinates
    pts = [
        (0, 0),
        (stem_diameter / 2, 0),
        (stem_diameter / 2, stem_height),
        (knob_diameter / 2, stem_height),
        (knob_diameter / 2, stem_height + (knob_height - chamfer_height)),
        (top_flat_diameter / 2, stem_height + knob_height),
        (0, stem_height + knob_height)
    ]
    return pts

# Re-creating using the revolve method for a cleaner topology
result = (
    cq.Workplane("XZ")
    .polyline(knob_profile())
    .close()
    .revolve()
)