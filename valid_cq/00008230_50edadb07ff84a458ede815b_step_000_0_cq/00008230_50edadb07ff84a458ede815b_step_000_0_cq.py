import cadquery as cq

# Parametric dimensions
disk_radius = 50.0  # Radius of the large base disk
disk_thickness = 2.0  # Thickness of the base disk
post_radius = 5.0   # Radius of the central post
post_height = 15.0  # Height of the post from the top of the disk

# Create the base disk
# We start by drawing a circle on the XY plane and extruding it
base = cq.Workplane("XY").circle(disk_radius).extrude(disk_thickness)

# Create the central post
# We select the top face of the base and draw a circle for the post
# Then extrude it upwards
post = (
    base.faces(">Z")
    .workplane()
    .circle(post_radius)
    .extrude(post_height)
)

# Combine into the final result
# Note: The extrude operation on the workplane already combines the new solid 
# with the base object by default (combine=True), so 'post' contains the full union.
result = post

# Optional: Add the slit seen in the image
# It looks like a simple cut running from the center to the edge.
# Let's assume a thin slit width.
slit_width = 0.5
slit = (
    result.faces(">Z")
    .workplane()
    .rect(disk_radius, slit_width, centered=False) # Draw a rectangle starting from origin
    .cutThruAll()
)

# Based on the image, the slit is very thin, essentially a line. 
# However, in CAD, a zero-width cut is usually not a feature unless it's a split.
# The image shows a visible seam line. Let's create the geometry without the slit cut
# if it's meant to be a solid piece, or with a very thin cut if it represents a split washer.
# Given the prompt asks for the model based on the image, and the line is quite distinct
# like a join or a split, but the object looks monolithic otherwise.
# Let's stick to the primary geometry which is the disk and the pin.
# The line could be a rendering artifact of a revolve operation or a seam. 
# I will provide the solid geometry without the cut, as that is the safer assumption for a general "pin on disk" part.
# If I look closer, it's just a line. It might just be the seam edge from a REVOLVE operation in the original CAD software.
# I will output the clean geometry.

result = post