import cadquery as cq

# Parametric dimensions
width = 50.0       # Total width of the U-shape
depth = 50.0       # Depth of the U-shape
height = 50.0      # Height of the walls
thickness = 5.0    # Thickness of the walls

# Create the U-shaped profile
# We start with a base rectangle representing the overall footprint
# Then we cut out the center to leave the U-shape walls
# Method: Sketch a U-shape on the XY plane and extrude it upwards

result = (
    cq.Workplane("XY")
    .rect(width, depth)
    .extrude(height)
    # Select the face that corresponds to the open side (let's assume "front" or -Y direction based on standard views, 
    # but for a symmetric U-shape relative to the center, it's easier to just shell or cut)
    # However, the image shows a U-channel with a bottom. Let's look closer.
    # Actually, the image looks like three walls standing on a plane, open at the top and open at one side.
    # Or it could be a simple U-channel extrusion.
    # Let's create a U-profile sketch and extrude it.
)

# Alternative, more robust construction method for a U-channel:
# 1. Create outer box
# 2. Cut inner box from the top, leaving walls and bottom?
# No, looking at the image, there is no bottom visible in the sense of a floor. It looks like an extrusion of a U-shape.
# Let's assume it's a U-profile extruded vertically.

# Re-evaluating based on "U-channel" typically being a uniform cross-section.
# The image shows a vertical U-shape.
# Let's define the cross section on the XY plane.

result = (
    cq.Workplane("XY")
    # Create the outer rectangle
    .rect(width, depth)
    # Create the inner rectangle to subtract
    # We shift the inner rectangle so one side remains open.
    # If we want the opening on the "front" (negative Y), we shift the cut towards negative Y.
    # Actually, let's just draw the U-shape with a polyline to be precise.
    
    .moveTo(-width/2, -depth/2)
    .lineTo(-width/2, depth/2)   # Left wall outer edge
    .lineTo(width/2, depth/2)    # Back wall outer edge
    .lineTo(width/2, -depth/2)   # Right wall outer edge
    .lineTo(width/2 - thickness, -depth/2) # Right wall inner start
    .lineTo(width/2 - thickness, depth/2 - thickness) # Right wall inner corner
    .lineTo(-width/2 + thickness, depth/2 - thickness) # Left wall inner corner
    .lineTo(-width/2 + thickness, -depth/2) # Left wall inner end
    .close()
    .extrude(height)
)

# NOTE: The above creates a "wall" U-shape standing up.
# Let's verify the orientation against the image.
# Image shows:
# - Left wall
# - Back wall
# - Right wall
# - Open front
# - Open top
# - Open bottom? The bottom is obscured, but usually these are extrusions. 
# The shading suggests it's a solid extrusion of that U-profile.

# Let's clean up the code to be simple and parametric.

result = (
    cq.Workplane("XY")
    # Draw outer rectangle
    .rect(width, depth)
    # Draw inner rectangle for the cut. 
    # To make a U-shape open at the "front" (Y-), we position the inner rect 
    # such that it overlaps the front edge.
    # Inner width = width - 2*thickness
    # Inner depth = depth - thickness
    # Center Y of inner rect needs to be shifted by -thickness/2 to align the back wall thickness
    .rect(width - 2*thickness, depth - thickness)
    # Now we have two concentric rectangles. CadQuery's extude with multiple wires 
    # will naturally create a hollow tube if they are nested.
    # But we want an open side. The inner rectangle needs to be shifted so it breaks the outer wall.
    # Let's shift the inner rectangle towards the front (negative Y).
    # The back wall is at +depth/2. The inner back wall should be at +depth/2 - thickness.
    # The center of the outer box is (0,0).
    # The center of the inner cutout needs to be calculated.
    # Inner cutout size: (width - 2*thickness) x (depth - thickness + extra_for_cut)
    # It's easier to just use the `cut` operation on a solid block.
)

# Solid Block Method (Easier to read and parameterize)
result = (
    cq.Workplane("XY")
    .box(width, depth, height)
    # Select the top face to define the cut profile
    .faces(">Z")
    .workplane()
    # Create a rectangle for the cutout
    # We want to remove the center, leaving 'thickness' on left, right, and back.
    # Opening is at the front (let's say -y direction).
    # Center of the box is (0,0).
    # Cutout width = width - 2*thickness
    # Cutout depth = depth - thickness (plus a bit to ensure clean cut through front)
    # The back of the cutout should be at y = depth/2 - thickness.
    # The front of the cutout should extend past -depth/2.
    # Center Y of cutout = (Back + Front) / 2
    # Let's position the cutout explicitly.
    .center(0, -thickness/2 - 0.001) # Shift center slightly forward to ensure cut breaks the face
    .rect(width - 2*thickness, depth - thickness + 0.002)
    .cutBlind(-height) # Cut all the way down
)

# Wait, looking at the image again, is there a floor?
# It looks like a U-channel extrusion, meaning it's open at the top AND bottom.
# If I use `cutBlind(-height)`, it cuts all the way through, making it a tube/extrusion.
# The previous polyline method produces exactly this.
# Let's stick to the polyline method or a specific subtraction that guarantees an extrusion shape.
# The "Solid Block Method" above creates a U-shaped extrusion if cutBlind goes all the way through.

# Let's refine the Polyline/Sketch method as it's cleaner for profiles.
# Center the U-shape at origin.
# Opening towards -Y.

result = (
    cq.Workplane("XY")
    .moveTo(-width/2, -depth/2)
    .lineTo(-width/2, depth/2)
    .lineTo(width/2, depth/2)
    .lineTo(width/2, -depth/2)
    .lineTo(width/2 - thickness, -depth/2)
    .lineTo(width/2 - thickness, depth/2 - thickness)
    .lineTo(-width/2 + thickness, depth/2 - thickness)
    .lineTo(-width/2 + thickness, -depth/2)
    .close()
    .extrude(height)
)