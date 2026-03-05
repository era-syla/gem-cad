import cadquery as cq
import math

# --- Parameters ---
# Flange dimensions
flange_diameter = 120.0
flange_thickness = 20.0

# Shaft dimensions
shaft_diameter = 50.0
shaft_length = 80.0  # Length extending from the flange

# Bolt hole pattern dimensions
bolt_circle_diameter = 90.0
num_holes = 8
hole_diameter = 10.0

# Internal Spline dimensions (approximate based on visual)
spline_outer_diameter = 25.0  # Tip diameter
spline_inner_diameter = 20.0  # Root diameter
num_teeth = 18
spline_depth = flange_thickness + shaft_length  # Through entire part

# --- Helper Function for Spline Profile ---
def create_spline_profile(outer_r, inner_r, teeth):
    """
    Creates a 2D sketch of a star/spline shape.
    """
    points = []
    angle_step = 2 * math.pi / (2 * teeth)
    
    for i in range(2 * teeth):
        angle = i * angle_step
        # Alternating between outer and inner radius
        r = outer_r if i % 2 == 0 else inner_r
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x, y))
    
    # Close the loop
    points.append(points[0])
    return points

# --- Modeling ---

# 1. Create the main Flange Base
# We start with the large disk.
flange = cq.Workplane("XY").circle(flange_diameter / 2).extrude(flange_thickness)

# 2. Create the Shaft
# Extrude the shaft from the face of the flange.
shaft = (
    flange.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# 3. Create the Bolt Holes
# Select the flange face, sketch the points on a circle, and cut through.
result_with_holes = (
    shaft.faces("<Z") # Select the back face of the flange to drill through
    .workplane()
    .polarArray(bolt_circle_diameter / 2, 0, 360, num_holes)
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# 4. Create the Internal Spline
# We need to cut a splined hole through the center axis.
# Generate the profile points
spline_points = create_spline_profile(
    spline_outer_diameter / 2, 
    spline_inner_diameter / 2, 
    num_teeth
)

# Cut the spline
result = (
    result_with_holes.faces(">Z") # Select front face of shaft
    .workplane()
    .polyline(spline_points)
    .close()
    .cutThruAll()
)

# Export or display (optional, but good practice for script output)
# cq.exporters.export(result, "flange_shaft.step")