import cadquery as cq

# Parametric dimensions
plate_thickness = 5.0
side_length = 80.0
side_width = 80.0
vertical_height = 60.0

bridge_width = 10.0
bridge_thickness = 5.0
center_tab_height = 20.0
center_tab_width = 5.0
center_tab_thickness = 5.0

gap_between_sides = 30.0

# Create the left L-bracket
# We'll create a profile on the XZ plane and extrude it
L_profile_pts = [
    (0, 0),
    (side_length, 0),
    (side_length, -plate_thickness),
    (plate_thickness, -plate_thickness),
    (plate_thickness, -vertical_height),
    (0, -vertical_height),
    (0, 0)
]

left_bracket = (
    cq.Workplane("XZ")
    .polyline(L_profile_pts)
    .close()
    .extrude(side_width / 2.0) # Extrude symmetrically? Or just one way. Let's do one way for now
)

# Move the left bracket into position relative to origin (center of gap)
left_bracket = left_bracket.translate((-side_length - gap_between_sides/2, -side_width/2, 0))

# Create the right L-bracket (mirror of the left)
right_bracket = left_bracket.mirror("YZ")

# Create the bridge connecting them
# The bridge sits on top of the surface (Z=0) and spans the gap
bridge_length = gap_between_sides + 2 * plate_thickness # Overlap slightly onto the plates
bridge = (
    cq.Workplane("XY")
    .rect(bridge_length + 40, bridge_width) # Make it longer to span well into the plates as shown
    .extrude(bridge_thickness)
    .translate((0, 0, 0)) # Centered on origin
)

# Create the central vertical tab on the bridge
center_tab = (
    cq.Workplane("XY")
    .workplane(offset=bridge_thickness)
    .rect(center_tab_thickness, bridge_width)
    .extrude(center_tab_height)
)

# Combine all parts
result = left_bracket.union(right_bracket).union(bridge).union(center_tab)