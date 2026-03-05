import cadquery as cq

# Parametric dimensions
length = 140.0       # Total length along the X-axis
width = 35.0         # Width of the top flat surface along the Y-axis
center_depth = 25.0  # Maximum depth of the curve at the center
end_depth = 2.0      # Depth of the profile at the ends

# Create the model using a Loft operation
# We define 3 cross-sections on the YZ plane spaced along the X-axis
result = (
    cq.Workplane("YZ")
    
    # Section 1: Left End Profile (at X = -length/2)
    .workplane(offset=-length/2.0)
    .moveTo(-width/2.0, 0)
    .lineTo(width/2.0, 0)
    # Create a smooth bottom curve using a spline from the current point
    # passing through the bottom-center and returning to the start side
    .spline([(0, -end_depth), (-width/2.0, 0)], includeCurrent=True)
    .close()
    
    # Section 2: Center Profile (at X = 0)
    # Note: workplane offset is relative to the previous plane
    .workplane(offset=length/2.0)
    .moveTo(-width/2.0, 0)
    .lineTo(width/2.0, 0)
    # The center section is much deeper, creating the "belly" shape
    .spline([(0, -center_depth), (-width/2.0, 0)], includeCurrent=True)
    .close()
    
    # Section 3: Right End Profile (at X = length/2)
    .workplane(offset=length/2.0)
    .moveTo(-width/2.0, 0)
    .lineTo(width/2.0, 0)
    .spline([(0, -end_depth), (-width/2.0, 0)], includeCurrent=True)
    .close()
    
    # Generate the solid body by interpolating between the profiles
    .loft()
)