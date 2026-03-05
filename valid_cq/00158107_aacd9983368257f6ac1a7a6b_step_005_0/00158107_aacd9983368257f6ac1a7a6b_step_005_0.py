import cadquery as cq

# Parametric dimensions
radius = 10.0          # Radius of the rounded end
width = radius * 2     # Main width of the body
length = 25.0          # Length of the straight section (center of hole to back face)
height = 15.0          # Thickness of the part
tab_length = 8.0       # Length of the side tab along the main axis
tab_width = 8.0        # Width of the side tab protrusion
hole_diameter = 8.0    # Diameter of the through hole

# Create the 2D profile and extrude
# The profile starts at the back-left corner (relative to the straight edge),
# goes along the straight edge, arcs around the front, creates the stepped edge,
# and closes back at the start.
# Coordinate system: Origin (0,0) is the center of the rounded end/hole.
# The body extends in the -X direction.
# The straight edge is at Y = -radius.
# The stepped edge is on the +Y side.

result = (
    cq.Workplane("XY")
    .moveTo(-length, -radius)               # Start at back corner (straight side)
    .lineTo(0, -radius)                     # Line to start of arc
    .threePointArc((radius, 0), (0, radius)) # Semi-circle arc to the other side
    .lineTo(-length + tab_length, radius)   # Line to the start of the tab
    .lineTo(-length + tab_length, radius + tab_width) # Step out for the tab
    .lineTo(-length, radius + tab_width)    # Line to back corner of tab
    .close()                                # Close back to (-length, -radius)
    .extrude(height)
)

# Cut the through hole centered at the origin (center of the arc)
result = (
    result.faces(">Z")
    .workplane()
    .moveTo(0, 0)
    .circle(hole_diameter / 2)
    .cutThruAll()
)