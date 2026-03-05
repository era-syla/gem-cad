import cadquery as cq

# Parametric dimensions based on the visual estimation of the image
length_total = 130.0   # Total length of the part
width_body = 80.0      # Width of the wider curved section
width_tab = 50.0       # Width of the rectangular tab
length_tab = 25.0      # Length of the rectangular tab section
thickness = 6.0        # Thickness of the plate
hole_diameter = 5.0    # Diameter of the mounting holes
hole_spacing = 30.0    # Distance between hole centers

# Derived parameters
radius_nose = width_body / 2.0
length_straight_body = length_total - length_tab - radius_nose

# Create the main body geometry
# We define the profile on the XY plane starting from the tab end
result = (
    cq.Workplane("XY")
    .moveTo(0, width_tab / 2)
    .lineTo(length_tab, width_tab / 2)                 # Tab straight edge
    .lineTo(length_tab, width_body / 2)                # Step out
    .lineTo(length_tab + length_straight_body, width_body / 2) # Body straight edge
    .threePointArc(                                    # Rounded nose
        (length_total, 0),                             # Arc midpoint (tip)
        (length_tab + length_straight_body, -width_body / 2) # Arc endpoint
    )
    .lineTo(length_tab, -width_body / 2)               # Body straight edge return
    .lineTo(length_tab, -width_tab / 2)                # Step in
    .lineTo(0, -width_tab / 2)                         # Tab straight edge return
    .close()
    .extrude(thickness)
)

# Create the two countersunk/simple holes on the tab
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (length_tab / 2, hole_spacing / 2),
        (length_tab / 2, -hole_spacing / 2)
    ])
    .hole(hole_diameter)
)