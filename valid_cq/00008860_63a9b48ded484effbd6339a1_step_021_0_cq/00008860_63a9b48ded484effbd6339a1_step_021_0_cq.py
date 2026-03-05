import cadquery as cq

# Parametric dimensions
radius_outer = 50.0   # Outer radius of the arc
width = 5.0           # Width of the ring section (radial thickness)
height = 5.0          # Height of the ring section (extrusion depth)
angle = 180.0         # Angle of the arc in degrees

# Derived dimensions
radius_inner = radius_outer - width

# Create the model
# We start by drawing on the XY plane.
# We sketch two concentric circles and cut the inner from the outer to form a ring,
# but since we only want an arc, there are a few ways to do this.
# A robust way is to draw the cross-section and revolve it, or extrude a 2D sketch.

# Method: Create a sketch of the ring sector and extrude it.
result = (
    cq.Workplane("XY")
    .moveTo(radius_inner, 0)
    .lineTo(radius_outer, 0)
    # Create the outer arc
    .threePointArc((0, radius_outer), (-radius_outer, 0))
    # Close the loop by going inwards
    .lineTo(-radius_inner, 0)
    # Create the inner arc (reversed direction)
    .threePointArc((0, radius_inner), (radius_inner, 0))
    .close()
    .extrude(height)
)

# Alternative method (often cleaner for simple arcs):
# Draw a rectangle on the XZ plane at the radius distance and revolve it around Z axis.
# But generating the explicit 2D shape on XY and extruding is very straightforward for this view.
# Let's stick with the first approach but refine the arc creation to be simpler using polar coordinates or standard arc commands if available,
# but standard arc commands usually need endpoints.

# Let's try a different, more geometric composition approach which is often cleaner in code:
# Create a full cylinder, cut the inner hole, then cut away the half we don't need.
# OR: Revolve a rectangle.
# Let's go with Revolve. It's very parametric.

# Revolve approach:
# 1. Define a rectangular profile on the XZ plane (standing up).
# 2. Revolve it around the Z axis for 180 degrees.

# Dimensions for revolve
# Center of the rectangle should be at radius = radius_inner + width/2
rect_center_radius = radius_inner + width / 2.0

result = (
    cq.Workplane("XZ")
    # Move to the position of the cross-section
    .center(rect_center_radius, height / 2.0)
    # Draw the rectangular cross-section
    .rect(width, height)
    # Revolve around the Z axis (0,0,0) to (0,0,1)
    # We want a 180 degree revolution.
    # By default, revolve uses the Y axis of the current plane as the axis of revolution if not specified? 
    # No, revolve usually defaults to the local Y, but we want global Z.
    # On the XZ plane, the local Y is the global Z. So revolving around (0,0,0) to (0,1,0) in local coords works.
    # Let's be explicit with axis.
    .revolve(angle, (0, 0, 0), (0, 0, 1))
)