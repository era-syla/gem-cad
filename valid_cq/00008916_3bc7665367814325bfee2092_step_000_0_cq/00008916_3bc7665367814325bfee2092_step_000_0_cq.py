import cadquery as cq

# Parameters used to define the geometry
base_diameter = 100.0
top_diameter = 40.0
height = 50.0
wall_thickness = 2.0
fillet_radius = 5.0  # Used for smoothing, though the main shape is lofted/revolved

# The profile curve control points
# We want a concave curve, so we can define a spline or use the revolution of a specific edge
# Strategy: Create a 2D profile and revolve it.
# The profile is defined by:
# 1. A point at (base_radius, 0)
# 2. A point at (top_radius, height)
# 3. A tangent/control point to creating the sweeping curve.

base_radius = base_diameter / 2.0
top_radius = top_diameter / 2.0

# Define the outer profile using a spline for that smooth "bell" shape
# Points: Start (base), Control Point (approximate), End (top)
# The control point helps define the curvature. 
# A control point closer to the axis and lower down creates the flare.
p_start = (base_radius, 0)
p_end = (top_radius, height)
p_control = (top_radius * 0.8, height * 0.15) # Pulls the curve in early to create the flare

# Create the outer shell by revolving a face
# We construct the cross-section face first
result = (
    cq.Workplane("XZ")
    .moveTo(base_radius, 0)
    .spline([p_end], tangents=[(-1, 0.5), (0, 1)], includeCurrent=True) # Tangents help shape the curve
    .lineTo(0, height)
    .lineTo(0, 0)
    .close()
    .revolve(360)
)

# Hollow out the object to create the wall thickness
# Using shell is often the easiest way to get uniform thickness on curved surfaces
result = result.faces(">Z").shell(-wall_thickness)

# Optional: Add small fillets to the sharp edges if desired, 
# though the image shows relatively sharp rims. Let's add very small rounded edges for realism.
result = result.edges(">Z or <Z").fillet(0.5)
