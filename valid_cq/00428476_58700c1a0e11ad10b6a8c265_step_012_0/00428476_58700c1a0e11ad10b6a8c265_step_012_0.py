import cadquery as cq

# --- Parametric Dimensions ---
# Connector dimensions
housing_width = 12.0
housing_thickness = 6.5
housing_length = 26.0
housing_chamfer = 1.0

plug_width = 8.4
plug_thickness = 2.6
plug_length = 6.5
plug_fillet = 0.4

# Cable dimensions
cable_diameter = 4.0
cable_spacing = 35.0  # Distance between the centers of the two connectors
straight_section_len = 15.0 # Length of cable extending straight from housing

# Derived dimensions
bend_radius = cable_spacing / 2.0

# --- Helper Function: Create Connector ---
def create_connector():
    # 1. Main Housing Body
    # Create a box centered in X/Y, base at Z=0
    housing = (cq.Workplane("XY")
               .box(housing_width, housing_thickness, housing_length, centered=(True, True, False)))
    
    # Chamfer the vertical edges for style
    housing = housing.edges("|Z").chamfer(housing_chamfer)
    
    # 2. Metal Plug Tip
    # Create smaller box on top of housing
    plug = (cq.Workplane("XY")
            .workplane(offset=housing_length)
            .box(plug_width, plug_thickness, plug_length, centered=(True, True, False)))
    
    # Fillet plug edges
    plug = plug.edges("|Z").fillet(plug_fillet)
    
    return housing.union(plug)

# --- Part Generation ---

# 1. Generate single connector instance
connector_template = create_connector()

# 2. Generate Cable
# The cable follows a 'U' path. We define this path in the XZ plane.
# Path coordinates logic:
#   Start: Left side top (connection point)
#   Mid1: Left side bottom (start of bend)
#   Mid2: Bottom of arc
#   Mid3: Right side bottom (end of bend)
#   End: Right side top
path = (cq.Workplane("XZ")
        .moveTo(-cable_spacing/2, straight_section_len)
        .lineTo(-cable_spacing/2, 0)
        .threePointArc((0, -bend_radius), (cable_spacing/2, 0))
        .lineTo(cable_spacing/2, straight_section_len))

# Create the circular profile at the start of the path
# We place it on the XY plane, elevated to the start Z-height and shifted to start X-position
cable_profile = (cq.Workplane("XY")
                 .workplane(offset=straight_section_len)
                 .center(-cable_spacing/2, 0)
                 .circle(cable_diameter/2))

# Sweep the profile along the path
cable = cable_profile.sweep(path)

# 3. Assemble components
# Position the left connector
left_connector = connector_template.translate((-cable_spacing/2, 0, straight_section_len))

# Position the right connector
right_connector = connector_template.translate((cable_spacing/2, 0, straight_section_len))

# Combine all parts into final result
result = cable.union(left_connector).union(right_connector)