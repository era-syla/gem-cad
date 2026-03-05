import cadquery as cq

# Parametric dimensions
main_radius = 20.0
height = 35.0
wall_thickness = 4.0
bottom_round_radius = 10.0
top_round_radius = 3.0  # Just for the outer edge
handle_radius = 4.0
handle_length = 8.0
handle_z_offset = 15.0  # Height of handle center from bottom

# 1. Create the main body
# We start with a cylinder
body = cq.Workplane("XY").circle(main_radius).extrude(height)

# 2. Round the bottom
# The image shows a very rounded bottom, almost like a sphere cut off.
# We apply a large fillet to the bottom edge.
body = body.edges("<Z").fillet(bottom_round_radius)

# 3. Round the top outer edge
# The top edge has a distinct rounded profile.
body = body.edges(">Z").fillet(top_round_radius)

# 4. Hollow out the inside to make it a cup/container
# We can use the shell command to hollow it out, leaving the top face open.
# A negative thickness hollows inwards.
body = body.faces(">Z").shell(-wall_thickness)

# 5. Add the small protrusion/handle on the side
# It looks like a simple cylinder sticking out from the side.
# We need to position a workplane on the side of the object.
# Since it's a cylinder, we can create a plane offset from the center.

# Calculate the distance to the outer surface roughly. 
# It's better to start from the center and extrude outwards, then union.
handle = (
    cq.Workplane("XZ")
    .center(0, handle_z_offset)
    .circle(handle_radius)
    .extrude(-main_radius - handle_length) # Extrude in negative Y direction
)

# Move the handle so its "base" is inside the cup and tip sticks out
# The current extrusion goes from Y=0 to Y=-(main_radius + handle_length).
# We want it sticking out of the side (e.g., negative Y side).
# Actually, let's just rotate/move it or construct it relative to the main body easier.

# Alternative handle construction:
# Define a workplane tangent to the cylinder or just offset.
handle = (
    cq.Workplane("XZ")
    .workplane(offset=-main_radius * 0.8) # Start slightly inside the wall
    .center(0, handle_z_offset)
    .circle(handle_radius)
    .extrude(-handle_length - (main_radius*0.2)) # Extrude outwards
)

# Combine the body and the handle
result = body.union(handle)

# Optional: Fillet the intersection of the handle and body for a smoother look
# (The image is a bit low-res on that joint, but usually these are filleted)
try:
    result = result.edges(cq.nearest((0, -main_radius, handle_z_offset))).fillet(1.0)
except:
    # If selection fails due to geometry complexity, we skip the aesthetic fillet
    pass

# Export or visualization
if 'show_object' in globals():
    show_object(result)