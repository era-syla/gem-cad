import cadquery as cq

# Parametric dimensions for the wedge model
height = 200.0          # Total vertical length
top_width = 30.0        # Width of the top face
top_thickness = 10.0    # Thickness of the top face
bottom_width = 25.0     # Width of the bottom tip (slight taper in width)
bottom_thickness = 2.0  # Thickness of the bottom tip (significant taper/wedge)

hole_width = 8.0        # Width of the rectangular hole
hole_height = 12.0      # Height of the rectangular hole
hole_offset = 25.0      # Distance from the top face to the center of the hole

# 1. Create the main tapered body using a Loft operation
# We define the bottom profile, establish a new workplane at the top height,
# define the top profile, and loft between them.
# Orientation: Width along X, Thickness along Y, Height along Z.
wedge_body = (
    cq.Workplane("XY")
    .rect(bottom_width, bottom_thickness)       # Bottom profile
    .workplane(offset=height)                   # Move to top
    .rect(top_width, top_thickness)             # Top profile
    .loft()                                     # Create solid
)

# 2. Create the cutter for the rectangular hole
# We sketch on the XZ plane (front view) to define the hole shape
# and extrude it perpendicular to the plane to create a cutting tool.
hole_cutter = (
    cq.Workplane("XZ")
    .center(0, height - hole_offset)            # Position hole relative to top
    .rect(hole_width, hole_height)              # Hole profile
    .extrude(top_thickness * 2, both=True)      # Extrude through the part
)

# 3. Cut the hole from the main body
result = wedge_body.cut(hole_cutter)