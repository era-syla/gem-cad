import cadquery as cq

# --- Parametric Dimensions ---
# General dimensions for the main rectangular shape (shared by both parts)
box_length = 80.0
box_width = 30.0
box_height = 15.0
wall_thickness = 3.0

# Dimensions specific to the right part (Tray)
tray_floor_thickness = 2.0
fillet_radius = 2.0  # For the corners of the tray

# Dimensions for the tab/handle on the right part
tab_length = 15.0  # Protrusion length
tab_width = 20.0   # Width of the tab along the box side
tab_thickness = 2.0
tab_position_z = 0.0 # Relative to the bottom of the tray

# Position offset to separate the two parts
part_spacing = 50.0

# --- Part 1: Left Frame (Hollow Rectangular Tube) ---
# Create a solid box
frame_outer = cq.Workplane("XY").box(box_length, box_width, box_height)

# Create a smaller box to subtract (making it hollow through-and-through)
frame_inner = (
    cq.Workplane("XY")
    .box(box_length - 2 * wall_thickness, 
         box_width - 2 * wall_thickness, 
         box_height)
)

# Cut the inner from the outer to make the frame
frame = frame_outer.cut(frame_inner)

# Move the frame to the left
left_part = frame.translate((-part_spacing / 2, 0, 0))


# --- Part 2: Right Tray with Tab ---
# Start with the outer shell
tray_outer = cq.Workplane("XY").box(box_length, box_width, box_height)

# Apply fillets to vertical edges of the outer shell
tray_outer = tray_outer.edges("|Z").fillet(fillet_radius)

# Shell the solid to create the tray (open top)
# We select the top face (+Z) and shell inwards
tray = tray_outer.faces("+Z").shell(-wall_thickness)

# Create the Tab
# We position a workplane on the side face of the tray
# Since the tray is centered at origin, the side face is at y = -box_width/2
tab = (
    cq.Workplane("XY")
    .workplane(offset=-box_height/2 + tab_thickness/2) # Align with bottom
    .center(0, -box_width/2) # Move to the edge
    .box(tab_width, tab_length * 2, tab_thickness) # Create box, length doubled to intersect well
    .cut(cq.Workplane("XY").box(box_length, box_width, 100)) # Cut away part inside the main box footprint if needed, but a simple union works better visually
)

# Re-approach for the tab: explicit placement relative to the tray
# Create the tab as a separate solid and unite it.
# Position: Centered on X, protruding from -Y face, aligned with bottom Z
tab_geo = (
    cq.Workplane("XY")
    .box(tab_width, tab_length, tab_thickness)
    .translate((0, -(box_width/2 + tab_length/2), -(box_height/2 - tab_thickness/2)))
)

# Combine tray and tab
right_part_combined = tray.union(tab_geo)

# Move the tray to the right
right_part = right_part_combined.translate((part_spacing / 2, 0, 0))

# --- Final Assembly ---
result = left_part.union(right_part)