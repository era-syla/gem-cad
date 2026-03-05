import cadquery as cq

# Parameters for the drone arm / plate
total_length = 320.0
center_width = 40.0
thickness = 3.0
straight_section_half_length = 100.0  # Distance from center to the step
step_indent = 2.0  # Size of the notch/step on the side
tip_radius = 12.0  # Radius of the rounded ends

# Calculated Dimensions
tip_center_dist = (total_length / 2.0) - tip_radius
outer_y = center_width / 2.0
inner_y = outer_y - step_indent

# Define the base shape using a wire on the XY plane
# Starting from top-left, going clockwise
result = (
    cq.Workplane("XY")
    .moveTo(-straight_section_half_length, outer_y)
    .lineTo(straight_section_half_length, outer_y)       # Top straight edge
    .lineTo(straight_section_half_length, inner_y)       # Step in
    .lineTo(tip_center_dist, tip_radius)                 # Taper to right tip
    .threePointArc(                                      # Right tip semi-circle
        (tip_center_dist + tip_radius, 0),
        (tip_center_dist, -tip_radius)
    )
    .lineTo(straight_section_half_length, -inner_y)      # Taper back
    .lineTo(straight_section_half_length, -outer_y)      # Step out
    .lineTo(-straight_section_half_length, -outer_y)     # Bottom straight edge
    .lineTo(-straight_section_half_length, -inner_y)     # Step in
    .lineTo(-tip_center_dist, -tip_radius)               # Taper to left tip
    .threePointArc(                                      # Left tip semi-circle
        (-tip_center_dist - tip_radius, 0),
        (-tip_center_dist, tip_radius)
    )
    .lineTo(-straight_section_half_length, inner_y)      # Taper back
    .close()
    .extrude(thickness)
)

# --- Add Holes ---

# Left End: Motor Mount Pattern (Standard 4-hole + Center Shaft)
# Assumed M3 mounting holes and ~9mm shaft hole
motor_center_x = -tip_center_dist
result = (
    result.faces(">Z").workplane()
    .moveTo(motor_center_x, 0)
    .circle(4.5)  # 9mm center hole
    .cutThruAll()
    
    # 4 Screw holes in rectangular pattern (e.g. 16x19mm or similar)
    .moveTo(motor_center_x, 0)
    .rect(16.0, 19.0, forConstruction=True)
    .vertices()
    .circle(1.6)  # 3.2mm diameter holes
    .cutThruAll()
)

# Right End: Frame Mounting Pattern (Triangular configuration)
mount_center_x = tip_center_dist
result = (
    result.faces(">Z").workplane()
    .pushPoints([
        (mount_center_x + 5, 7),   # Top hole near tip
        (mount_center_x + 5, -7),  # Bottom hole near tip
        (mount_center_x - 8, 0)    # Central hole further in
    ])
    .circle(1.6) # 3.2mm diameter holes
    .cutThruAll()
)