import cadquery as cq

# Parameters
length = 100.0      # Total length of the rack
width = 15.0        # Width (thickness) of the rack
height = 25.0       # Total height of the rack
num_teeth = 20      # Number of serrated teeth
tooth_depth = 5.0   # Vertical depth of the teeth

# Derived parameters
pitch = length / num_teeth

# Generate the profile points for the side view
# Sketching on the X-Z plane, so Y coordinate in the points list represents Z (height)
pts = []

# Start at Top-Left corner
pts.append((0, height))

# Top-Right corner
pts.append((length, height))

# Right edge down to the start of the teeth (root level)
pts.append((length, tooth_depth))

# Generate the zigzag pattern for the teeth, moving from right to left
for i in range(num_teeth):
    current_x = length - (i * pitch)
    
    # Point at the tip of the tooth (at the bottom, height=0)
    pts.append((current_x - (pitch / 2.0), 0))
    
    # Point at the root of the next tooth (back at tooth_depth)
    pts.append((current_x - pitch, tooth_depth))

# The shape is automatically closed by the .close() method back to (0, height)

# Create the 3D model
result = (
    cq.Workplane("XZ")  # Create a workplane on the Front face
    .polyline(pts)      # Draw the profile defined by the points
    .close()            # Close the wire to form a face
    .extrude(width)     # Extrude along the Y axis to create depth
)