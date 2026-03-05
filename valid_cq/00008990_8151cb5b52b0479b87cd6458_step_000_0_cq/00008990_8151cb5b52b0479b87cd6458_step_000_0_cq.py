import cadquery as cq

# Parametric dimensions
length = 50.0  # The long dimension of the top face
width = 40.0   # The short dimension (between the curved sides)
height = 10.0  # The thickness of the block
bulge_radius = 30.0 # Radius of the curved sides (must be > height/2)

# Create the base sketch on the front plane (XZ plane relative to a typical extrusion)
# We will draw the profile of the curved side and extrude it along the length.
# This approach ensures the "bulge" is consistent along the length.

# Method 1: Extruding a sketch with arcs
# We sketch on the YZ plane to define the cross-section (a rectangle with curved vertical sides)
# and then extrude along the X-axis.

# Let's adjust orientation to match the image:
# Top face is XY plane.
# Long edge runs along X (or Y).
# The curved faces are the "ends".

# Let's assume:
# - Length is along Y
# - Width is along X
# - Thickness is along Z

# Sketch the profile on the XZ plane (width x height)
# The profile consists of two straight horizontal lines (top/bottom) and two arcs (sides).

result = (
    cq.Workplane("XZ")
    .moveTo(-width / 2, height / 2)  # Top Left
    .lineTo(width / 2, height / 2)   # Top Right
    .radiusArc((width / 2, -height / 2), bulge_radius) # Arc down to Bottom Right
    .lineTo(-width / 2, -height / 2) # Bottom Left
    .radiusArc((-width / 2, height / 2), bulge_radius) # Arc up to start
    .close()
    .extrude(length)
)

# Since we extruded along the normal of XZ (which is Y), the object is centered on XZ but starts at Y=0.
# Let's center it completely for good practice.
result = result.translate((0, -length / 2, 0))

# Alternatively, to match the specific perspective of the image where the long side is facing front-ish:
# Rotate result to lay flat.
result = result.rotate((0, 0, 0), (1, 0, 0), -90)

# Final adjustment: The prompt image shows the long faces are flat, and the SHORT faces are curved.
# My current code makes the SIDES curved.
# Let's re-read the geometry.
# The image shows a block where two opposing faces are curved outward (convex).
# The other two side faces are flat.
# The top and bottom are flat.

# Let's rebuild more explicitly.
# Length: 80
# Width: 60
# Thickness: 20

L = 80.0
W = 60.0
T = 20.0
R = T * 1.5 # Radius of the curve

# Profile on the YZ plane (Side view)
# Straight vertical lines, Curved horizontal lines? No.
# Let's look at the cross section.
# If we slice it vertically, the cross section is a rectangle with curved sides.
# Let's draw that cross-section on the plane perpendicular to the flat long faces.

result = (
    cq.Workplane("YZ")
    .moveTo(-W/2, T/2)
    .lineTo(W/2, T/2)
    # Create the curved side. 
    # To make it convex outward, the midpoint of the arc needs to be further out than W/2.
    .radiusArc((W/2, -T/2), -R) 
    .lineTo(-W/2, -T/2)
    .radiusArc((-W/2, T/2), -R)
    .close()
    .extrude(L)
    .translate((L/2, 0, 0)) # Center the extrusion
    .rotate((0,0,0), (0,1,0), -90) # Rotate to make Z up
    .rotate((0,0,0), (0,0,1), 90)  # Rotate to match image orientation
)

# Refined attempt for simpler code logic matching the image directly
# We draw the profile of the "end cap" (the curved shape) and extrude it.
# The curved shape is defined by Width and Thickness.
# Extrusion length is Length.

length = 60.0
width = 40.0
thickness = 15.0
curve_radius = 25.0 # Controls how round the side is

result = (
    cq.Workplane("YZ") # Draw on the side plane
    .moveTo(-width/2, thickness/2)      # Top-Left of profile
    .lineTo(width/2, thickness/2)       # Top-Right of profile
    .radiusArc((width/2, -thickness/2), -curve_radius) # Right curve (convex)
    .lineTo(-width/2, -thickness/2)     # Bottom-Left of profile
    .radiusArc((-width/2, thickness/2), -curve_radius) # Left curve (convex)
    .close()
    .extrude(length) # Extrude along X axis
    .translate((-length/2, 0, 0)) # Center it
)

# Rotate to match the isometric view usually expected (Z-up)
# Currently extrusion is along X. Profile is in YZ.
# Top face is at Y = thickness/2 (which is vertical in YZ).
# Let's orient it so Thickness is Z, Width is Y, Length is X.

result = (
    cq.Workplane("XY") # This works better for standard orientation
    .moveTo(-length/2, -width/2)
    .lineTo(length/2, -width/2) # Front straight edge
    
    # Right side curve
    .radiusArc((length/2, width/2), -curve_radius) 
    
    .lineTo(-length/2, width/2) # Back straight edge
    
    # Left side curve
    .radiusArc((-length/2, -width/2), -curve_radius)
    .close()
    .extrude(thickness)
)

# Wait, looking at the image again carefully.
# The CURVED face is the vertical thickness.
# It is NOT the plan view that is curved. The top face is rectangular.
# The side wall bulges out.
# So the cross-section perpendicular to the long axis is a rectangle with two curved vertical sides.

L = 50.0  # Length (Long side)
W = 40.0  # Width (Short side)
H = 15.0  # Height/Thickness
R = 20.0  # Radius of the bulge

result = (
    cq.Workplane("XZ") # Draw the cross-section on the side
    .moveTo(-W/2, H/2)       # Top Left
    .lineTo(W/2, H/2)        # Top Right
    # Create arc for the right side (Convex)
    .radiusArc((W/2, -H/2), -R) 
    .lineTo(-W/2, -H/2)      # Bottom Left
    # Create arc for the left side (Convex)
    .radiusArc((-W/2, H/2), -R)
    .close()
    .extrude(L)              # Extrude along Y (Length)
    # Reorient to match standard Z-up view
    .rotate((0,0,0), (1,0,0), -90) 
    .rotate((0,0,0), (0,0,1), 90)
)