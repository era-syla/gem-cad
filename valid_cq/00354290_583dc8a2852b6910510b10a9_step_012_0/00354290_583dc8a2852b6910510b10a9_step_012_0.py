import cadquery as cq

# --- Parametric Dimensions ---
# Cable Geometry
cable_diameter = 5.0
bend_radius = 20.0       # Radius of the U-turn
straight_length = 20.0   # Length of the straight vertical sections of the cable

# Left Connector (Square-ish profile, e.g., USB-B style)
conn1_width = 12.0
conn1_thick = 12.0
conn1_length = 32.0
plug1_width = 8.0
plug1_thick = 8.0
plug1_length = 10.0

# Right Connector (Wide/Flat profile, e.g., USB-A/C style)
conn2_width = 14.0
conn2_thick = 8.0
conn2_length = 36.0
plug2_width = 10.0
plug2_thick = 4.0
plug2_length = 10.0

# --- Helper Function for Connector Construction ---
def create_connector(body_w, body_t, body_l, plug_w, plug_t, plug_l):
    """Creates a generic USB-style connector with a body and a plug."""
    
    # Main plastic housing
    housing = (
        cq.Workplane("XY")
        .box(body_w, body_t, body_l, centered=(True, True, False))
        .edges("|Z").fillet(1.5)  # Round the vertical corners
        .edges("<Z").fillet(0.5)  # Slight round at the cable entry
    )
    
    # Metal plug connector on top
    plug = (
        cq.Workplane("XY")
        .workplane(offset=body_l)
        .box(plug_w, plug_t, plug_l, centered=(True, True, False))
        .edges(">Z").chamfer(0.5) # Bevel the tip of the plug
    )
    
    return housing.union(plug)

# --- Build Geometry ---

# 1. Generate the Cable
# Path defined in the Front (XZ) plane: Down -> Arc -> Up
cable_path = (
    cq.Workplane("XZ")
    .moveTo(-bend_radius, straight_length)      # Start at top of left leg
    .lineTo(-bend_radius, 0)                    # Down to start of bend
    .threePointArc((0, -bend_radius), (bend_radius, 0)) # U-turn
    .lineTo(bend_radius, straight_length)       # Up to top of right leg
)

# Sweep a circular profile along the path
cable = (
    cq.Workplane("XY")
    .circle(cable_diameter / 2.0)
    .sweep(cable_path)
)

# 2. Generate and Position Connector 1 (Left)
connector1 = create_connector(conn1_width, conn1_thick, conn1_length, 
                              plug1_width, plug1_thick, plug1_length)
# Move connector to the top of the left cable leg
connector1 = connector1.translate((-bend_radius, 0, straight_length))

# 3. Generate and Position Connector 2 (Right)
connector2 = create_connector(conn2_width, conn2_thick, conn2_length, 
                              plug2_width, plug2_thick, plug2_length)
# Move connector to the top of the right cable leg
connector2 = connector2.translate((bend_radius, 0, straight_length))

# --- Combine Assembly ---
result = cable.union(connector1).union(connector2)