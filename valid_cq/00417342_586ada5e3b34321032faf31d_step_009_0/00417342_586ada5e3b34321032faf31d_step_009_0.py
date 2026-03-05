import cadquery as cq

# --- Parameter Definitions ---
height = 90.0           # Total height of the plate
top_width = 100.0       # Width of the upper rectangular section
leg_extension = 20.0    # Width of the side tabs/legs extending beyond main width
leg_height = 18.0       # Height of the side tabs/legs
thickness = 4.0         # Plate thickness
fillet_radius = 4.0     # Radius for top corner fillets
hole_diameter = 5.5     # Diameter of mounting holes
arch_height = 12.0      # Height of the bottom center cut-out arch
flat_foot_width = 15.0  # Width of the flat section at the bottom of legs before arch
hole_margin_top = 8.0   # Distance of top holes from top/side edges

# --- Derived Dimensions ---
total_width = top_width + 2 * leg_extension

# Calculate center positions for holes
# Top holes
top_hole_x = top_width / 2 - hole_margin_top
top_hole_y = height - hole_margin_top

# Bottom holes (centered within the leg extension area)
leg_hole_x = top_width / 2 + leg_extension / 2
leg_hole_y = leg_height / 2

# --- Modeling Process ---

# 1. Create the base profile sketch
# We trace the perimeter starting from the top-left corner
result = (
    cq.Workplane("XY")
    .moveTo(-top_width / 2, height)
    .lineTo(top_width / 2, height)
    .lineTo(top_width / 2, leg_height)
    .lineTo(total_width / 2, leg_height)
    .lineTo(total_width / 2, 0)
    .lineTo(total_width / 2 - flat_foot_width, 0)
    # Create the bottom arch: from current point, through (0, arch_height), to symmetric point on left
    .threePointArc((0, arch_height), (-(total_width / 2 - flat_foot_width), 0))
    .lineTo(-total_width / 2, 0)
    .lineTo(-total_width / 2, leg_height)
    .lineTo(-top_width / 2, leg_height)
    .close()
    .extrude(thickness)
)

# 2. Add Fillets to the top corners
# Select edges that are parallel to Z (|Z) and located at the maximum Y position (>Y)
result = result.edges("|Z and >Y").fillet(fillet_radius)

# 3. Create Mounting Holes
# Select the top face (>Z) to establish a workplane for drilling
result = (
    result.faces(">Z")
    .workplane()
    # Add top corner holes
    .pushPoints([
        (-top_hole_x, top_hole_y),
        (top_hole_x, top_hole_y)
    ])
    .hole(hole_diameter)
    # Add bottom leg holes
    .pushPoints([
        (-leg_hole_x, leg_hole_y),
        (leg_hole_x, leg_hole_y)
    ])
    .hole(hole_diameter)
)