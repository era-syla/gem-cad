import cadquery as cq
import math

# --- Model Parameters ---
# Shaft dimensions
shaft_diameter = 12.0
shaft_length = 24.0

# Flange dimensions
flange_diameter = 24.0
flange_width = 16.0  # Width across flat sides
flange_thickness = 4.0

# Neck dimensions
neck_diameter = 12.0
neck_visible_length = 3.0  # Length of neck visible before merging into ball

# Ball dimensions
ball_diameter = 22.0
ball_radius = ball_diameter / 2.0
ball_flat_offset = 7.5  # Distance from ball center to the flat face

# --- Calculation ---
# Calculate the distance from the ball center to where the neck cylinder 
# intersects the sphere surface (Pythagorean theorem)
# This ensures the neck cylinder merges cleanly into the ball
dist_center_to_neck_surface = math.sqrt(ball_radius**2 - (neck_diameter / 2.0)**2)

# Total length to extrude the neck so the end face is at the ball center
neck_extrusion_length = neck_visible_length + dist_center_to_neck_surface

# --- Geometry Construction ---

# 1. Create the cylindrical shaft aligned along the X-axis
result = cq.Workplane("YZ").circle(shaft_diameter / 2.0).extrude(shaft_length)

# 2. Create the Flange
# Use a sketch to define the "Double-D" shape (Circle intersected with Rectangle)
flange_sketch = (
    cq.Sketch()
    .circle(flange_diameter / 2.0)
    .rect(flange_width, flange_diameter, mode='i') # Intersect mode to create flats
)

result = (
    result.faces(">X")
    .workplane()
    .placeSketch(flange_sketch)
    .extrude(flange_thickness)
)

# 3. Create the Neck
# Extrude a cylinder from the flange to the center of the ball
result = (
    result.faces(">X")
    .workplane()
    .circle(neck_diameter / 2.0)
    .extrude(neck_extrusion_length)
)

# 4. Create the Ball
# Place a sphere at the end of the neck (which corresponds to the ball center)
result = (
    result.faces(">X")
    .workplane()
    .sphere(ball_radius)
)

# 5. Create the Flat Face on the Ball
# Select the tip of the sphere (+X), establish a workplane, 
# offset it back to the cut position, and remove material outwards.
# Note: faces(">X") on the sphere selects the spherical face; 
# .workplane() creates a plane tangent to the tip (Max X).
cut_offset_from_tip = -ball_radius + ball_flat_offset

result = (
    result.faces(">X")
    .workplane(offset=cut_offset_from_tip)
    .rect(ball_diameter * 2, ball_diameter * 2) # Create a large cutting rectangle
    .extrude(ball_diameter, combine='cut')      # Cut outwards (along +X normal)
)