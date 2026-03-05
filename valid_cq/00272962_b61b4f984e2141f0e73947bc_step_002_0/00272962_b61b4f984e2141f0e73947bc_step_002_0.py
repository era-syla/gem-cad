import cadquery as cq

# --- Model Parameters ---

# Body dimensions
body_length = 30.0
body_width = 12.0
body_height = 12.0
chamfer_size = 3.5  # Size of the 45-degree chamfer at the front

# Plunger (top button) dimensions
plunger_diam = 5.0
plunger_height = 1.2
plunger_pos_offset = 5.0  # Distance from the front face center

# Terminal dimensions
term_length = 9.0
term_width = 4.0
term_thick = 0.6
term_spacing = 6.5  # Vertical distance between terminals
notch_width = 2.0   # Width of the U-cutout
notch_depth = 2.5   # Depth of the U-cutout from the tip

# --- Geometry Generation ---

# 1. Create the main body
# We create a box centered at the origin
main_body = cq.Workplane("XY").box(body_length, body_width, body_height)

# Chamfer the front vertical edges
# Select edges parallel to Z axis (|Z) and at the maximum X direction (>X)
main_body = main_body.edges("|Z and >X").chamfer(chamfer_size)

# 2. Add the Plunger (Top Button)
# Calculate position relative to center: Move to front (+X), then back by offset
plunger_x = (body_length / 2) - plunger_pos_offset

# Select top face, create workplane, draw circle, and extrude
plunger = (main_body.faces(">Z").workplane()
           .center(plunger_x, 0)
           .circle(plunger_diam / 2)
           .extrude(plunger_height))

# Add a small nub on the bottom (detail often found on such solenoids)
result = (plunger.faces("<Z").workplane()
          .center(plunger_x, 0)
          .circle(plunger_diam / 2 - 1.0)
          .extrude(0.5))

# 3. Create and Place Terminals

def create_terminal():
    """Generates a single terminal with a U-shaped notch."""
    # Create the base strip. 
    # centered=(False, True, True) means X starts at 0, Y and Z are centered.
    lug = cq.Workplane("XY").box(term_length, term_width, term_thick, 
                                 centered=(False, True, True))
    
    # Add rounded corners to the tip of the terminal
    lug = lug.edges("|Z and >X").fillet(0.5)
    
    # Define the cutout geometry for the notch
    # Calculate center of the circular part of the notch
    notch_radius = notch_width / 2
    notch_center_x = term_length - notch_depth + notch_radius
    
    # Create a cutting tool that combines a circle and a rectangle (for the opening)
    cutter = (cq.Workplane("XY")
              .moveTo(notch_center_x, 0)
              .circle(notch_radius)  # The rounded base of the notch
              .moveTo(notch_center_x, -notch_radius)
              .rect(term_length - notch_center_x + 1.0, notch_width, centered=(False, False))
              .extrude(term_thick * 3, both=True)) # Ensure it cuts through
              
    return lug.cut(cutter)

# Generate the terminal geometry
term_geo = create_terminal()

# Position the terminals
# Rotate 180 degrees to face outwards from the back (-X) of the body
term_rotated = term_geo.rotate((0,0,0), (0,0,1), 180)

# Calculate placement coordinates
back_x = -body_length / 2
z_offset = term_spacing / 2

# Place Top Terminal
term_top = term_rotated.translate((back_x, 0, z_offset))

# Place Bottom Terminal
term_bot = term_rotated.translate((back_x, 0, -z_offset))

# Union everything into the final result
result = result.union(term_top).union(term_bot)