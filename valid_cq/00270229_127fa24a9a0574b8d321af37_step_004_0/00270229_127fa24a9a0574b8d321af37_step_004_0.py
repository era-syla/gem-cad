import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the visual proportions of the image
width = 60.0                # Total width of the plate
straight_height = 35.0      # Height of the vertical straight sides
thickness = 2.0             # Thickness of the plate

# Margins defining the hole size
margin_top = 4.0            # Gap between hole and top edge
margin_side = 9.0           # Gap between hole and side edges
margin_bottom = 12.0        # Gap between hole and bottom edge

# --- Derived Dimensions ---
outer_radius = width / 2.0
total_height = straight_height + outer_radius

# Ellipse Hole Calculations
hole_top_y = total_height - margin_top
hole_bottom_y = margin_bottom
hole_height = hole_top_y - hole_bottom_y
hole_ry = hole_height / 2.0  # Y radius (major axis usually)

hole_width = width - (2 * margin_side)
hole_rx = hole_width / 2.0   # X radius (minor axis)

hole_center_y = hole_bottom_y + hole_ry

# --- Modeling ---

# 1. Create the base outer shape
# Path: Bottom-Left -> Bottom-Right -> Up -> Semicircle Arc -> Down -> Close
result = (
    cq.Workplane("XY")
    .moveTo(-width / 2.0, 0)
    .lineTo(width / 2.0, 0)
    .lineTo(width / 2.0, straight_height)
    .threePointArc(
        (0, total_height),                  # Point on arc (top apex)
        (-width / 2.0, straight_height)     # End point of arc
    )
    .close()
    .extrude(thickness)
)

# 2. Cut the elliptical hole
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(0, hole_center_y)
    .ellipse(hole_rx, hole_ry)
    .cutThruAll()
)