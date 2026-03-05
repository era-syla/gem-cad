import cadquery as cq

# 1. Define parametric control points for the 3D ribbon curve
# The points approximate the start (high left), dip (low center),
# arch (high right), and end (low right) of the shape in the image.
points = [
    cq.Vector(-10, 5, 12),  # Start point
    cq.Vector(-3, 0, 4),    # Inflection/Dip point
    cq.Vector(5, 8, 10),    # Arch peak
    cq.Vector(12, 2, 4)     # End point
]

# 2. Generate the 3D spline path
# Create a spline edge passing through the points and convert to a wire
path_edge = cq.Edge.makeSpline(points)
path_wire = cq.Wire.assembleEdges([path_edge])

# 3. Determine the start orientation for the profile
# We need a construction plane at the start of the curve.
# To ensure the ribbon starts in a stable orientation (roughly "flat" relative to the ground),
# we calculate a local X-axis that is perpendicular to both the path tangent and the global Z-axis.
start_pt = path_edge.startPoint()
tangent = path_edge.tangentAt(0)
z_axis = cq.Vector(0, 0, 1)

# Calculate cross product to get a horizontal vector perpendicular to the path
x_dir = tangent.cross(z_axis).normalized()

# Create the plane defined by origin, normal (tangent), and x-direction
plane = cq.Plane(origin=start_pt, normal=tangent, xDir=x_dir)

# 4. Define parametric dimensions for the ribbon profile
ribbon_width = 3.0
ribbon_thickness = 0.15

# 5. Create the final solid geometry
# - Workplane(plane): Create a drawing plane at the start of the path
# - rect(...): Draw the rectangular cross-section of the ribbon
# - sweep(...): Sweep the rectangle along the path
# - isFrenet=True: Uses the Frenet-Serret frame to naturally bank/twist the profile along the curve
result = (
    cq.Workplane(plane)
    .rect(ribbon_width, ribbon_thickness)
    .sweep(cq.Workplane(obj=path_wire), isFrenet=True)
)