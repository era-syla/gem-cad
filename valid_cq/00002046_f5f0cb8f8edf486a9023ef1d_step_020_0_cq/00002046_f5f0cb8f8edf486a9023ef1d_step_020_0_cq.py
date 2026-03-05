import cadquery as cq

# --- Parameter Definitions ---

# Housing Dimensions
housing_width = 30.0
housing_height = 14.0
housing_depth = 12.0
wall_thickness = 1.5
fillet_radius = 1.5

# Flange (Base) Dimensions
flange_extension = 1.5  # How much wider the flange is than the housing
flange_depth = 3.0
flange_width = housing_width + (2 * flange_extension)
flange_height = housing_height + (2 * flange_extension)

# Pin Configuration
num_cols = 4
num_rows = 2
pin_pitch_x = 6.0  # Horizontal spacing
pin_pitch_y = 6.0  # Vertical spacing

# Pin Dimensions
pin_size = 0.8  # Square pin side length
pin_back_length = 8.0  # Length sticking out the back
pin_tip_taper = 2.0 # Length of the pointed tip

# Keying/Polarization (The cutout at the bottom)
key_width = 18.0
key_depth = 1.0 # Depth of the cutout into the housing face

# --- Modeling ---

# 1. Create the main housing body
# We start with the main block that sticks out
housing = (
    cq.Workplane("XY")
    .rect(housing_width, housing_height)
    .extrude(housing_depth)
)

# Apply fillets to the housing corners
housing = housing.edges("|Z").fillet(fillet_radius)

# 2. Create the flange (base) at the back
# The flange is centered on the same XY plane but extruded "backwards" (negative Z) or attached
flange = (
    cq.Workplane("XY")
    .rect(flange_width, flange_height)
    .extrude(-flange_depth)
)

# Apply fillets to the flange corners
flange = flange.edges("|Z").fillet(fillet_radius)

# Combine housing and flange
body = housing.union(flange)

# 3. Create the interior cavity (hollow out the front)
# We subtract a slightly smaller shape from the front face
cavity = (
    housing.faces(">Z")
    .workplane()
    .rect(housing_width - 2*wall_thickness, housing_height - 2*wall_thickness)
    .extrude(-housing_depth, combine="cut") # Don't cut through the flange yet
)

# 4. Add the Keying Cutout
# There is a small indentation/cutout at the bottom center of the front face
cutout = (
    cq.Workplane("XZ")
    .workplane(offset=-housing_height/2) # Move to bottom edge
    .center(0, housing_depth) # Move to front face
    .rect(key_width, key_depth * 2) # Height is doubled to ensure cut through edge
    .extrude(-wall_thickness, combine=False) # Only cut the wall thickness
)
# Re-orient cut for Boolean operation if needed, or just do a cut directly on the body
body = cavity.cut(cutout)


# 5. Create the Pins
# We need to calculate the grid positions
x_offsets = [
    (i - (num_cols - 1) / 2) * pin_pitch_x 
    for i in range(num_cols)
]
y_offsets = [
    (i - (num_rows - 1) / 2) * pin_pitch_y 
    for i in range(num_rows)
]

# Generate a single pin
def create_pin(loc):
    # Basic square pin shaft
    p = (
        cq.Workplane("XY")
        .rect(pin_size, pin_size)
        .extrude(housing_depth - 2.0) # Stick partially into housing
    )
    
    # Back extension
    p_back = (
        cq.Workplane("XY")
        .rect(pin_size, pin_size)
        .extrude(-(flange_depth + pin_back_length))
    )
    
    # Tapered tip at the back
    # We define the tip starting at the end of the back extension
    tip_start_z = -(flange_depth + pin_back_length)
    p_tip = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, 0, tip_start_z))
        .rect(pin_size, pin_size)
        .workplane(offset=-pin_tip_taper)
        .rect(0.1, 0.1) # Taper to a point (small rectangle)
        .loft()
    )
    
    full_pin = p.union(p_back).union(p_tip)
    return full_pin.val().located(loc)

# Create all pins
pins = []
for x in x_offsets:
    for y in y_offsets:
        loc = cq.Location(cq.Vector(x, y, 0))
        pins.append(create_pin(loc))

# 6. Create the "+" shaped plastic supports around pins inside the housing
# Looking at the reference, the pins sit inside cross-shaped standoffs/guides inside the connector.

support_thickness = 0.8
support_length = 3.0 # Size of the cross arms

support_shape = (
    cq.Workplane("XY")
    .rect(support_length, support_thickness) # Horizontal bar
    .extrude(housing_depth/2) # Halfway up
)
support_shape_v = (
    cq.Workplane("XY")
    .rect(support_thickness, support_length) # Vertical bar
    .extrude(housing_depth/2)
)
single_cross = support_shape.union(support_shape_v)

# We need to subtract the pin hole from the cross
pin_hole = (
    cq.Workplane("XY")
    .rect(pin_size, pin_size)
    .extrude(housing_depth)
)
single_socket_feature = single_cross.cut(pin_hole)

# Place the plastic supports
socket_features = []
for x in x_offsets:
    for y in y_offsets:
        loc = cq.Location(cq.Vector(x, y, -flange_depth)) # Start from back wall
        # We need to shift Z up because extrude goes positive Z
        # The supports sit on the "floor" of the inside of the connector (top of flange)
        socket_features.append(single_socket_feature.val().located(cq.Location(cq.Vector(x, y, 0))))

# Combine everything
result = body

# Add pins
for pin in pins:
    result = result.union(cq.Workplane(obj=pin))

# Add internal plastic supports
for feat in socket_features:
    result = result.union(cq.Workplane(obj=feat))
    
# Clean up the back face where pins exit (optional, adds holes to flange)
# The boolean union of pins usually handles this visually, but for a true manifold 
# part where pins are separate materials, you'd cut holes. 
# Here we assume it's a single solid or insert-molded part.

# Final Fillet on the front face edges for a polished look
result = result.faces(">Z").edges().fillet(0.5)

# Export or Render
# show_object(result)