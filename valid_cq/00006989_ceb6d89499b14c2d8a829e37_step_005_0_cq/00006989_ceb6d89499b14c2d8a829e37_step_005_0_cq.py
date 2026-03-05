import cadquery as cq

# Parameters for the geometry
height = 100.0          # Total height of the main conical section
base_radius = 60.0      # Radius of the arc at the bottom
top_radius = 40.0       # Radius of the arc at the top of the main section
wall_thickness = 10.0   # Thickness of the wall
arc_angle = 120.0       # Angle of the arc segment (degrees)
lip_height = 5.0        # Height of the small lip at the top
lip_thickness = 5.0     # Thickness of the lip (offset from inner edge)

# Create the main tapered body (conical section)
# We loft two wires: one at the bottom and one at the top.
# Since it's an arc, we create a 2D profile and revolve/extrude or use lofting.
# A loft between two arc-shaped faces is a robust way to handle the taper.

def create_arc_face(radius, thickness, angle, z_pos):
    """Creates a planar face representing a thickened arc at a specific Z height."""
    
    # Calculate outer radius based on thickness
    outer_radius = radius + thickness
    
    # We construct the face by moving to the plane, creating edges, and making a face
    face = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .moveTo(radius, 0)
        .lineTo(outer_radius, 0) # Start line
        .threepointArc((0, outer_radius), (-outer_radius, 0)) # Outer arc (simplified for 180, usually need precise coords)
        # However, threepointArc is tricky for specific angles.
        # Better approach: parametric line creation or using polar line commands if simple.
        # Let's use the polyline/arc approach for robustness with generic angles.
    )
    
    # Alternative approach for Arc Face: 
    # Create a solid wedge/cylinder segment and cut it, but lofting wires is cleaner for the taper.
    # Let's define the wires explicitly using parametric curves.
    
    return face

# Strategy Revision:
# The shape is essentially a "Revolve" operation of a trapezoidal profile around the Z axis,
# but limited to a specific angle.
# CadQuery's `revolve` allows an `angleDegrees` argument.

# 1. Define the 2D cross-section profile.
# The profile is located on the XZ plane (or YZ).
# It looks like a trapezoid with a small rectangle on top (the lip).

# Cross-section points (assuming Inner surface is the reference for radius):
# Point 1: (base_radius, 0)
# Point 2: (base_radius + wall_thickness, 0)
# Point 3: (top_radius + wall_thickness, height)
# Point 4: (top_radius + lip_thickness, height)  -- This creates the step
# Point 5: (top_radius + lip_thickness, height + lip_height)
# Point 6: (top_radius, height + lip_height)
# Point 7: (top_radius, height) -- Back to top of main wall
# Point 8: (top_radius, height) ... actually we connect straight to (base_radius, 0) for the inner face?
# Let's look closer at the image. The inner face also tapers.

# Refined Cross-section (XZ plane):
p1 = (base_radius, 0)
p2 = (base_radius + wall_thickness, 0)

# Calculate the slope for the outer wall
# The outer wall goes from base_radius+thick to top_radius+thick?
# Or does the thickness stay constant perpendicular to the surface? 
# For simplicity in CAD, usually horizontal thickness is defined or normal thickness.
# Let's assume the wall thickness tapers or the radii are just defined.
p3 = (top_radius + wall_thickness, height)

# The lip starts here. It seems thinner than the main wall.
p4 = (top_radius + lip_thickness, height) 
p5 = (top_radius + lip_thickness, height + lip_height)
p6 = (top_radius, height + lip_height)
p7 = (top_radius, height)
p8 = (base_radius, 0) # Closing the loop

# Create the profile wire
profile = (
    cq.Workplane("XZ")
    .polyline([p1, p2, p3, p4, p5, p6, p7, p8])
    .close()
)

# 2. Revolve the profile to create the curved segment.
# The image shows a segment, not a full ring.
result = profile.revolve(angleDegrees=arc_angle)

# Center geometry (optional, purely for aesthetics if needed, but centering on origin is standard)
# The current code starts the revolve at angle 0. 
# To make it symmetrical like the image often implies, we might rotate it.
# The default revolve starts at the X-axis and goes counter-clockwise.
# To center it on the Y-axis (or X-axis), we rotate the solid.
result = result.rotate((0, 0, 0), (0, 0, 1), -arc_angle / 2)