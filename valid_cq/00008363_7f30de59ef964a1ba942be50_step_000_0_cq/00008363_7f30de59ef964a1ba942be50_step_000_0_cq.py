import cadquery as cq

# Parametric Dimensions
mug_height = 95.0
mug_radius = 40.0
wall_thickness = 4.0
bottom_thickness = 5.0

# Handle dimensions
handle_height = 60.0
handle_width = 30.0  # Extension from the mug
handle_thickness = 10.0
handle_vertical_offset = 15.0 # From the bottom

# Derived dimensions
inner_radius = mug_radius - wall_thickness
inner_height = mug_height - bottom_thickness

# Create the main mug body
# 1. Create a cylinder
body = cq.Workplane("XY").circle(mug_radius).extrude(mug_height)

# 2. Hollow it out
# We cut a smaller cylinder from the top
body = body.faces(">Z").workplane().hole(2 * inner_radius, inner_height)

# 3. Round the top rim
body = body.edges(">Z").fillet(wall_thickness / 2.1)

# Create the Handle
# The handle looks like a rectangular loop attached to the side.
# We will create a sketch on a plane perpendicular to the mug wall (e.g., XZ plane).

# We need to center the handle sketch vertically relative to the handle's position
handle_center_z = handle_vertical_offset + (handle_height / 2.0)

# Create a path for the handle shape
handle_path = (
    cq.Workplane("XZ")
    .center(mug_radius, handle_center_z)
    .rect(handle_width * 2, handle_height)
)

# Create the handle profile
# The handle has a rectangular cross-section with rounded edges in the image.
# We'll make a solid block first, cut out the middle, and fillet it.

# Alternative approach: Draw the side profile and extrude
handle = (
    cq.Workplane("YZ")
    .center(0, handle_center_z)
    .workplane(offset=mug_radius) # Move to the surface of the mug
    .rect(handle_thickness, handle_height)
    .extrude(handle_width)
)

# Now we have a solid block sticking out. We need to cut the hole in the handle.
# The hole is rectangular.
hole_height = handle_height - (2 * handle_thickness)
hole_width = handle_width - handle_thickness # Leave thickness at the end

# Cut the hole through the handle (Y-axis direction)
handle = (
    handle.faces(">X")
    .workplane()
    .center(0, 0)
    .rect(hole_width, hole_height) # Dimensions on the face
    .cutBlind(-handle_thickness * 2) # Cut through
)

# Fillet the handle edges to match the smooth look in the image
# It looks like the outer edges are rounded significantly
handle = handle.edges("|X").fillet(2.0)
handle = handle.edges("|Z").fillet(2.0)
handle = handle.edges("|Y").fillet(1.0)


# Combine the mug body and the handle
result = body.union(handle)

# Optional: Add a small fillet at the join if needed, though simple union is usually sufficient
# for this style. To make it robust, we often just leave the union.

# Export or display (not strictly required by prompt but good for testing)
# show_object(result)