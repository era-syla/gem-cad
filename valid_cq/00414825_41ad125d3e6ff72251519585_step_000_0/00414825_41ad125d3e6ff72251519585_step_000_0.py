import cadquery as cq

# -- Parametric Dimensions --
base_diameter = 20.0
base_height = 25.0

top_diameter = 14.0
top_height = 35.0

# Transition (chamfer) dimension
transition_height = 2.0

# Groove (thread/ribs) dimensions
groove_pitch = 1.5   # Vertical distance between grooves
groove_depth = 0.5   # Depth of the cut

# -- Derived Values --
base_radius = base_diameter / 2.0
top_radius = top_diameter / 2.0
total_height = base_height + transition_height + top_height
start_groove_z = base_height + transition_height

# -- Profile Construction --
# We build the cross-section profile in the XZ plane to revolve around Z.
points = []

# 1. Start at the bottom center
points.append((0, 0))

# 2. Base cylinder profile
points.append((base_radius, 0))
points.append((base_radius, base_height))

# 3. Transition (Chamfer)
# Connects the wider base to the narrower top section
points.append((top_radius, start_groove_z))

# 4. Grooved Top Section
# Generate a zig-zag profile for the ridges
current_z = start_groove_z
limit_z = total_height

# Note: The last point added was (top_radius, current_z)
while (current_z + groove_pitch) <= limit_z:
    # Inner point (Valley of the groove)
    points.append((top_radius - groove_depth, current_z + groove_pitch / 2.0))
    
    # Outer point (Peak of the groove)
    points.append((top_radius, current_z + groove_pitch))
    
    current_z += groove_pitch

# 5. Top cap
# Extend to full height (if loop ended slightly early)
if current_z < total_height:
    points.append((top_radius, total_height))

# Close to the center axis at the top
points.append((0, total_height))

# -- Solid Generation --
# Create the result by revolving the defined profile 360 degrees
result = cq.Workplane("XZ").polyline(points).close().revolve()