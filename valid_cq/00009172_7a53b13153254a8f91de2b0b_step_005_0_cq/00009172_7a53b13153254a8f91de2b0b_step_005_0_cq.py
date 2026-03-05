import cadquery as cq

# --- Parametric Dimensions ---
door_height = 2100.0  # Total height of the door
door_width = 900.0    # Total width of the door
door_thickness = 40.0 # Thickness of the door panel

# Handle parameters
handle_height_from_bottom = 1050.0  # Height of the handle center from the bottom
handle_offset_from_edge = 60.0      # Distance from the edge of the door
handle_base_radius = 25.0           # Radius of the circular base plate (rosette)
handle_base_thickness = 5.0         # Thickness of the base plate
handle_shaft_length = 60.0          # Length of the shaft extending from door
handle_shaft_diameter = 15.0        # Diameter of the shaft
handle_grip_length = 120.0          # Length of the horizontal grip part
handle_grip_width = 20.0            # Width/Height of the grip cross-section
handle_grip_thickness = 10.0        # Thickness of the grip handle

# --- Construction ---

# 1. Create the main door panel
door_panel = cq.Workplane("XY").box(door_width, door_thickness, door_height)

# 2. Create the door handle assembly
# We will position the handle on the +Y face of the door (front face)

# Create a workplane on the front face, shifted to the handle location
handle_center_z = -(door_height / 2) + handle_height_from_bottom
handle_center_x = (door_width / 2) - handle_offset_from_edge
handle_plane = (
    door_panel.faces(">Y")
    .workplane(centerOption="CenterOfMass")
    .center(handle_center_x, handle_center_z)
)

# 2a. Base Plate (Rosette) - Simple cylinder
base_plate = handle_plane.circle(handle_base_radius).extrude(handle_base_thickness)

# 2b. Handle Shaft - Cylinder extending out
shaft = (
    handle_plane.workplane(offset=handle_base_thickness)
    .circle(handle_shaft_diameter / 2)
    .extrude(handle_shaft_length - handle_base_thickness)
)

# 2c. Handle Grip - Rectangular bar extending sideways
# We need to position this at the end of the shaft
grip_plane = shaft.faces(">Y").workplane()

# Draw the rectangle for the grip. The grip usually points away from the edge (towards center) 
# or towards the edge. In the image, it looks like a simple lever.
# Let's make a simple rectangular lever.
grip = (
    grip_plane
    .center(-handle_grip_length / 2 + handle_shaft_diameter/2, 0) # Offset to make it a lever
    .rect(handle_grip_length, handle_grip_width)
    .extrude(handle_grip_thickness)
)

# Combine handle parts into one object for cleaner code, though strictly not necessary if unioning later
handle_assembly = base_plate.union(shaft).union(grip)

# 3. Combine Door and Handle
result = door_panel.union(handle_assembly)

# Optional: Add fillets to the door edges for realism? The image is quite sharp.
# Let's keep it simple as per the low-poly look of the reference.

# Export or visualization
if 'show_object' in globals():
    show_object(result)