import cadquery as cq

# Parametric dimensions
cylinder_diameter = 20.0
cylinder_length = 20.0
wedge_length = 15.0  # Length of the prismatic/wedge section protruding
wedge_width = cylinder_diameter # Width of the wedge at the base
wedge_tip_thickness = 0.0 # Assuming it comes to a sharp edge

# Create the base cylinder
# We orient it along the Y axis or Z axis. Let's use the X axis for the cylinder length to match a common lathe-like orientation.
# Cylinder: radius=10, height=20, centered at origin or offset.
# Let's align the interface between the cylinder and the wedge at X=0.
cylinder = (
    cq.Workplane("YZ")
    .circle(cylinder_diameter / 2.0)
    .extrude(cylinder_length)
)

# Create the wedge/triangular prism part
# This part extends from the face of the cylinder in the opposite direction.
# Looking at the image, the wedge has a triangular cross-section when viewed from the side.
# The base of the triangle is the diameter of the cylinder.
# The tip of the wedge is horizontal.

# Let's sketch on the YZ plane (the face of the cylinder at X=0) and extrude backwards (-X).
# However, the image shows a "chisel" or "screwdriver" tip shape.
# This shape is essentially a loft or a cut from a cylinder, or simply a wedge shape attached to it.
# Let's model it as a separate solid and union it.

# The wedge profile (side view) looks like a triangle.
# Let's draw the profile on the XY plane (side view).
# The base of the triangle is vertical (along Z), matching the cylinder diameter.
# The point is towards negative X.

wedge = (
    cq.Workplane("XY")
    .moveTo(0, cylinder_diameter / 2.0)  # Top of the cylinder face
    .lineTo(0, -cylinder_diameter / 2.0) # Bottom of the cylinder face
    .lineTo(-wedge_length, 0)            # The tip of the wedge
    .close()
    .extrude(cylinder_diameter)          # Extrude along Z initially (this creates a blocky wedge)
)

# Wait, the extrusion above creates a prism with a rectangular cross-section along the extrusion path.
# Let's rethink the orientation to match the image better.
# Image features:
# 1. A cylinder on the right.
# 2. A "chisel" shape on the left.
# The chisel shape transitions from the circular face of the cylinder to a horizontal line edge.

# Alternative approach: Loft
# Loft from a circle (at the interface) to a rectangle (at the tip).
# Circle at X=0.
# Rectangle (very thin, representing the line edge) at X = -wedge_length.

# Let's try the Loft approach as it handles the transition smoothly if needed, 
# but looking closely at the image, the sides of the wedge part seem flat (planar), not conical.
# This implies it is a V-shape cut from a cylinder or a triangular prism intersected with a cylinder, 
# or simply a triangular prism that matches the diameter.

# Let's look at the flat faces. The two sloping faces meet at a sharp horizontal edge.
# The sides of this wedge section are also flat and vertical.
# This confirms it is a simple triangular prism, oriented horizontally.
# Specifically:
# Cross-section on the XZ plane is a triangle.
# Extruded along Y? No, the edge is horizontal.

# Let's refine the shape logic:
# 1. Cylinder: Axis along X. Radius R.
# 2. Wedge: Attached to the -X face of the cylinder.
#    - It tapers to a horizontal line (parallel to Y axis).
#    - Its width at the base (connection to cylinder) matches the cylinder diameter.
#    - Its height at the base matches the cylinder diameter.

# Let's construct the wedge:
# Draw a triangle on the XZ plane.
# Points: (0, R), (0, -R), (-Length, 0).
# Extrude this symmetrically along Y by 'cylinder_diameter'.
# Then intersect this with a cylinder? Or just leave it?
# In the image, the side walls of the wedge section appear to be flat (planar), not curved like the cylinder.
# If they are flat, it's just a prism.
# If they are curved (continuation of cylinder), it's a cylinder with two V-cuts.
# Looking at the transition line between the cylinder and the wedge part:
# It looks like a straight line segment on the side? No, it looks like a full circle face joining a shape that fits within it.
# Actually, looking very closely, the side of the wedge part is a FLAT plane.
# This means the wedge is a simple extrusion of a triangle.
# However, the base of the triangle (where it touches the cylinder) is a rectangle (height * width).
# But the cylinder face is a circle.
# If we just attach a rectangular-base prism to a circle, the corners of the prism will stick out.
# OR, the prism width matches the cylinder diameter, and the corners are tangent.
# In the image, the junction looks perfectly clean. The "corners" of the rectangular base of the wedge seem to align exactly with the tangent of the circle.

# Let's try constructing the wedge as a simple extrusion of a triangle on the XZ plane, extruded along Y.
# Height of triangle = Cylinder Diameter (Z axis spans -R to R).
# Length of triangle = Wedge Length (X axis).
# Width of extrusion = Cylinder Diameter (Y axis).

wedge_profile = (
    cq.Workplane("XZ")
    .moveTo(0, cylinder_diameter / 2.0)
    .lineTo(0, -cylinder_diameter / 2.0)
    .lineTo(-wedge_length, 0)
    .close()
)

# Extrude symmetrically in Y so it aligns with the cylinder axis
wedge_solid = wedge_profile.extrude(cylinder_diameter / 2.0, both=True)

# Now creates the cylinder
cylinder_solid = (
    cq.Workplane("YZ")
    .circle(cylinder_diameter / 2.0)
    .extrude(cylinder_length)
)

# Combine them
result = wedge_solid.union(cylinder_solid)

# Rotate for better viewing angle similar to image
result = result.rotate((0, 0, 0), (0, 1, 0), -45).rotate((0,0,0), (0,0,1), 45)