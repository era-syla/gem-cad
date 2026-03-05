import cadquery as cq

# --- Parameter Definitions ---
# Main dimensions
outer_diameter = 100.0
part_height = 15.0

# Wall thicknesses for the split geometry
# The ring features a stepped inner diameter, resulting in two distinct wall thicknesses
# separated by a vertical step along the Y-axis.
wall_thickness_thick = 12.0  # Right side (thicker wall, smaller ID)
wall_thickness_thin = 5.0    # Left side (thinner wall, larger ID)

# Notch dimensions
notch_width = 8.0
# The radius to the back face of the rectangular notches
notch_back_radius = 46.0

# --- Derived Calculations ---
outer_radius = outer_diameter / 2.0
inner_radius_thick = outer_radius - wall_thickness_thick
inner_radius_thin = outer_radius - wall_thickness_thin

# --- 3D Modeling ---

# 1. Create the base outer cylinder
# This represents the full outer volume before cutting the interior
blank = cq.Workplane("XY").circle(outer_radius).extrude(part_height)

# 2. Create the inner void tool
# This shape represents the empty space in the center. It is defined by a profile 
# with two semi-circles of different radii connected by straight lines (steps).
inner_void_profile = (
    cq.Workplane("XY")
    # Start at the top transition point (Top, Small Radius)
    .moveTo(0, inner_radius_thick)
    # Create the right-side semi-circle (Clockwise)
    .threePointArc((inner_radius_thick, 0), (0, -inner_radius_thick))
    # Create the step transition at the bottom (Bottom, Large Radius)
    .lineTo(0, -inner_radius_thin)
    # Create the left-side semi-circle (Clockwise)
    .threePointArc((-inner_radius_thin, 0), (0, inner_radius_thin))
    # Close the profile back to the start point
    .close()
)

inner_void = inner_void_profile.extrude(part_height)

# 3. Create the notch cutters
# There are 4 rectangular cutouts located at 45 degree intervals relative to the axes.
notch_cutters = cq.Workplane("XY")
notch_cutter_length = 20.0  # Arbitrary length sufficient to cut through the inner wall material

for angle in [45, 135, 225, 315]:
    # Create a box to act as the cutting tool for one notch
    # Box is initially centered at origin
    single_notch = (
        cq.Workplane("XY")
        .box(notch_cutter_length, notch_width, part_height)
        # Position the box:
        # X: Shift so the "outer" face is at the defined notch_back_radius
        # Z: Shift up by half height since box is centered in Z, but extrude starts at 0
        .translate((notch_back_radius - notch_cutter_length/2.0, 0, part_height/2.0))
        # Rotate the tool to its angular position around the Z axis
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    # Combine all notch tools into a single compound object
    notch_cutters = notch_cutters.union(single_notch)

# 4. Apply Boolean operations
# Subtract the central void and the notches from the base cylinder
result = blank.cut(inner_void).cut(notch_cutters)