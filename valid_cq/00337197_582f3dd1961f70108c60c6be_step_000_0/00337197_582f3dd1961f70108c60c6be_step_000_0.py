import cadquery as cq

# --- Parameters ---
length_solid = 50.0     # Length of the front solid section
length_shell = 50.0     # Length of the back shell section
base_width = 30.0       # Width of the base
base_height = 5.0       # Thickness of the base plate
groove_radius = 10.0    # Radius of the inner channel
shell_thickness = 2.0   # Wall thickness of the shell section
axis_height = 15.0      # Height of the channel center axis from bottom

# Calculate derived dimension
shell_outer_radius = groove_radius + shell_thickness

# --- 1. Front Solid Section ---
# A solid block with chamfered sides and a semi-circular groove on top.
# Defined on the YZ plane and extruded along X.
front_profile = (
    cq.Workplane("YZ")
    .moveTo(-base_width / 2, 0)
    .lineTo(base_width / 2, 0)
    .lineTo(shell_outer_radius, axis_height)       # Slanted side to outer lip
    .lineTo(groove_radius, axis_height)            # Flat shoulder
    .threePointArc(                                # Concave semi-circle groove
        (0, axis_height - groove_radius), 
        (-groove_radius, axis_height)
    )
    .lineTo(-shell_outer_radius, axis_height)      # Flat shoulder
    .close()
)

front_part = front_profile.extrude(length_solid)

# --- 2. Back Section (Base + Shell) ---

# Base Plate: A rectangular plate under the shell section
back_base = (
    cq.Workplane("XY")
    .moveTo(length_solid + length_shell / 2, 0)
    .rect(length_shell, base_width)
    .extrude(base_height)
)

# Shell: A semi-cylindrical guide rail
shell_profile = (
    cq.Workplane("YZ")
    .workplane(offset=length_solid)
    .moveTo(shell_outer_radius, axis_height)
    .threePointArc(                                # Outer convex arc
        (0, axis_height + shell_outer_radius), 
        (-shell_outer_radius, axis_height)
    )
    .lineTo(-groove_radius, axis_height)
    .threePointArc(                                # Inner concave arc
        (0, axis_height - groove_radius), 
        (groove_radius, axis_height)
    )
    .close()
)

back_shell = shell_profile.extrude(length_shell)

# --- Combine Geometry ---
result = front_part.union(back_base).union(back_shell)