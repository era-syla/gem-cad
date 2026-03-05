import cadquery as cq

# --- Parameters ---
length = 50.0       # Total length of the tube
width = 15.0        # Outer width of the square profile
height = 15.0       # Outer height of the square profile
wall_thickness = 1.5 # Thickness of the tube walls
corner_radius = 2.0  # Radius of the outer corners
slot_width = 8.0    # Width of the top opening
slot_length = 15.0  # Length of the cutout from the front face

# --- Modeling ---

# 1. Create the main outer profile (Square with rounded corners)
# We start with a solid block
main_body = (
    cq.Workplane("XY")
    .rect(width, height)
    .extrude(length)
)

# 2. Add fillets to the four long edges of the outer body
main_body = main_body.edges("|Z").fillet(corner_radius)

# 3. Create the hollow interior (shelling the solid)
# We select the faces at both ends (Z-min and Z-max) to remain open,
# creating a tube. Alternatively, we can just cut a smaller profile.
# A robust way for a simple tube is to cut a rectangle.

inner_width = width - (2 * wall_thickness)
inner_height = height - (2 * wall_thickness)
inner_radius = max(0.1, corner_radius - wall_thickness) # Ensure valid radius

# Create the hollow cut
hollow_cut = (
    cq.Workplane("XY")
    .rect(inner_width, inner_height)
    .extrude(length)
    .edges("|Z").fillet(inner_radius)
)

# Subtract the inner core from the main body to make it a tube
tube = main_body.cut(hollow_cut)

# 4. Create the slot cut on the top face
# We need to cut away a portion of the top wall starting from one end.
# Let's orient on the top face (XZ plane relative to default if extruded in Z, 
# but based on standard orientation, let's assume the tube runs along Z).

# Positioning for the cut:
# The tube is centered on X, Y. It runs from Z=0 to Z=length.
# We want to cut into the top face (Y+) from Z=0 inwards.

slot_cut = (
    cq.Workplane("XZ")
    .workplane(offset=height/2) # Move to the top surface
    .center(0, length/2)        # Move origin relative to face center if needed, 
                                # but usually easier to specify coordinates directly.
    # Let's use absolute coordinates for clarity.
    # We want a rectangle centered on X=0, starting at Z=0, going to Z=slot_length.
    # The depth of the cut needs to go through the top wall.
)

# Alternative approach for the slot: simpler boolean cut.
# Create a block representing the volume to remove.
cutter_box = (
    cq.Workplane("XY")
    .rect(slot_width, height) # Width is slot_width, Height is arbitrary large enough
    .extrude(slot_length)     # Length along Z
    .translate((0, height/2, 0)) # Move up so it intersects the top wall
)

# Apply the cut
result = tube.cut(cutter_box)

# Export the result (optional, but good for verification if running locally)
# cq.exporters.export(result, "result.step")