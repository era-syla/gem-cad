import cadquery as cq

# --- Parametric Dimensions ---
# Standard washer dimensions (e.g., roughly based on M10 or similar generic proportions)
outer_diameter = 20.0  # Outer diameter of the washer
inner_diameter = 10.5  # Inner diameter (hole size)
thickness = 2.0        # Thickness of the washer
chamfer_size = 0.2     # Small chamfer on the edges for a realistic look

# --- Modeling ---

# 1. Create the base disk
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)

# 2. Add chamfers to the top and bottom outer edges for a finished look
#    Note: Real washers are often stamped and might have a slight radius or shear/break edge.
#    A small chamfer is a good approximation for a CAD model.
try:
    result = result.edges("|Z").chamfer(chamfer_size)
    # Alternatively, if you only want outer edges chamfered:
    # result = result.edges(cq.selectors.RadiusNthSelector(1)).chamfer(chamfer_size)
except Exception:
    # Fallback in case chamfer fails (e.g. if too large), though unlikely here.
    pass

# Export or visualization line (optional but good practice to have 'result')
# if 'show_object' in globals():
#     show_object(result)