import cadquery as cq

# --- Parameters ---
length = 150.0       # Total length of the device
width = 75.0         # Total width
thickness = 9.0      # Total thickness

corner_radius = 5.0  # Radius of the main vertical corners
edge_fillet = 0.8    # Radius of the top and bottom edge chamfer/fillet

# Feature positions and sizes
button_pos_x = -35.0 # Position of circular button relative to center
button_r = 2.4       # Radius of button
button_gap = 0.3     # Gap around button

slot_pos_x = -15.0   # Position of slot relative to center
slot_len = 16.0      # Length of the slot
slot_w = 2.8         # Width of the slot

jack_r = 1.8         # Radius of headphone jack
mic_r = 0.6          # Radius of mic hole
jack_pos_y = 0.0     # Vertical position on side face (0 is center)
mic_pos_offset = 6.0 # Horizontal offset from jack

# --- Modeling ---

# 1. Create the base block
# We start with a box centered at the origin
result = cq.Workplane("XY").box(length, width, thickness)

# 2. Apply main vertical corner fillets
# Select edges parallel to the Z axis
result = result.edges("|Z").fillet(corner_radius)

# 3. Apply top and bottom edge fillets
# Select edges on the top (>Z) and bottom (<Z) faces
result = result.faces(">Z or <Z").edges().fillet(edge_fillet)

# 4. Create Side Features (Long Edge)
# Assuming the visible long face is the Front (-Y) face
# We create a workplane on this face to cut features

# Feature 1: Circular Button (simulated with a ring cut)
# This creates a groove leaving a "button" island in the middle
result = (result.faces("<Y").workplane(centerOption="CenterOfMass")
          .center(button_pos_x, 0)
          .circle(button_r + button_gap)  # Outer ring radius
          .circle(button_r)               # Inner button radius
          .cutBlind(-0.6))                # Depth of the groove

# Feature 2: Rectangular Slot (Volume rocker or SIM tray)
# We use slot2D to get rounded ends
result = (result.faces("<Y").workplane(centerOption="CenterOfMass")
          .center(slot_pos_x, 0)
          .slot2D(slot_len, slot_w)
          .cutBlind(-0.6))                # Shallow recess

# 5. Create End Features (Short Edge)
# Assuming the visible short face is the Right (>X) face

# Feature 3: Headphone Jack
result = (result.faces(">X").workplane(centerOption="CenterOfMass")
          .center(0, 0)                   # Centered on the face
          .circle(jack_r)
          .cutBlind(-8.0))                # Deep cut for the port

# Feature 4: Microphone Hole
result = (result.faces(">X").workplane(centerOption="CenterOfMass")
          .center(mic_pos_offset, 0)      # Offset to the side
          .circle(mic_r)
          .cutBlind(-2.0))                # Small hole

# The 'result' variable now contains the final geometry