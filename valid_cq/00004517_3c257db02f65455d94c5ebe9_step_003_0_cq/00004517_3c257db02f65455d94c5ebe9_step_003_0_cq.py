import cadquery as cq

# --- NEMA 17 Stepper Motor Parameters ---
# Standard NEMA 17 dimensions (approximate)
motor_width = 42.3  # Width/Height of the faceplate
motor_length = 40.0 # Length of the motor body (excluding shaft)
plate_thickness = 2.0 # Thickness of the front and back end plates
stator_chamfer = 3.0  # Chamfer size for the stator stack

# Shaft dimensions
shaft_diameter = 5.0
shaft_length = 24.0 # Length protruding from face
boss_diameter = 22.0
boss_height = 2.0

# Mounting holes
hole_spacing = 31.0
hole_diameter = 3.0 # M3 screw clearance
mounting_depth = 4.5

# --- Modeling ---

# 1. Create the main body profile (Square with chamfered corners)
# We create a square and then cut the corners to create the octagonal-ish stator shape
# Or, simpler: create the square end caps and the profiled stator separately.

# Front and Back Plates (Square with rounded corners)
plate_sketch = (
    cq.Sketch()
    .rect(motor_width, motor_width)
    .vertices()
    .fillet(1.0) # Small fillet on the corners
)

front_plate = cq.Workplane("XY").placeSketch(plate_sketch).extrude(plate_thickness)
back_plate = cq.Workplane("XY").workplane(offset=motor_length - plate_thickness).placeSketch(plate_sketch).extrude(plate_thickness)

# Stator Stack (The black middle part, often chamfered)
# It sits between the plates
stator_height = motor_length - (2 * plate_thickness)

stator_sketch = (
    cq.Sketch()
    .rect(motor_width, motor_width)
    .vertices()
    .chamfer(stator_chamfer) # Significant chamfer on the stator corners
)

stator = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness)
    .placeSketch(stator_sketch)
    .extrude(stator_height)
)

# Combine main body parts
motor_body = front_plate.union(stator).union(back_plate)

# 2. Add the Boss (Raised circle on front)
boss = (
    cq.Workplane("XY")
    .workplane(offset=0) # On top of the front plate (which started at Z=0 and went down? No, let's assume Z=0 is front face)
    # Re-evaluating coordinates: Let Z=0 be the front face of the motor.
)

# Let's rebuild slightly for better coordinate management.
# Z=0 is the mounting face. Z-negative is the motor body. Z-positive is the shaft.

# Re-doing the body based on Z=0 at the front face
body_sketch = (
    cq.Sketch()
    .rect(motor_width, motor_width)
    .vertices()
    .fillet(1.0)
)

# Front End Cap
end_cap_front = cq.Workplane("XY").placeSketch(body_sketch).extrude(-plate_thickness)

# Stator
stator_profile = (
    cq.Sketch()
    .rect(motor_width, motor_width)
    .vertices()
    .chamfer(stator_chamfer)
)
stator_stack = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness)
    .placeSketch(stator_profile)
    .extrude(-(motor_length - 2*plate_thickness))
)

# Back End Cap
end_cap_back = (
    cq.Workplane("XY")
    .workplane(offset=-(motor_length - plate_thickness))
    .placeSketch(body_sketch)
    .extrude(-plate_thickness)
)

motor_main = end_cap_front.union(stator_stack).union(end_cap_back)

# 3. Add Circular Boss
boss = (
    cq.Workplane("XY")
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# 4. Add Shaft
shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# 5. Mounting Holes
# Create points for the 4 holes
hole_locs = [
    (hole_spacing/2, hole_spacing/2),
    (hole_spacing/2, -hole_spacing/2),
    (-hole_spacing/2, hole_spacing/2),
    (-hole_spacing/2, -hole_spacing/2)
]

# Create the full union before drilling
result = motor_main.union(boss).union(shaft)

# Cut the mounting holes
result = (
    result
    .faces(">Z") # Select front face
    .workplane()
    .pushPoints(hole_locs)
    .hole(hole_diameter, depth=mounting_depth)
)

# Optional: Add the wire tail visible in the image
# This is a bit artistic, simple representation
wire_path = (
    cq.Workplane("YZ")
    .workplane(offset=motor_width/2) # Move to the side of the motor
    .moveTo(-motor_length + 5, -5)   # Near the back bottom corner
    .lineTo(-motor_length - 50, -30) # Stick out
)

# Create a small wire shape to sweep (optional, image shows a line)
# CadQuery can't render a simple line as a solid, so we make a thin tube
wire = (
    cq.Workplane("YZ")
    .workplane(offset=motor_width/2)
    .moveTo(-motor_length + 5, -5)
    .circle(0.5) # 1mm thick wire
    .extrude(100) # Simple extrusion straight out
    .rotate((0,0,0), (0,1,0), -20) # Angle it slightly to match image perspective
    .translate((-20, 0, -10)) # Adjust position
)

# Simplify wire to just a straight cylinder for robustness
wire_simple = (
    cq.Workplane("XY")
    .workplane(offset=-motor_length + 5) # Near back
    .moveTo(motor_width/2, -motor_width/4) # Side
    .circle(0.8)
    .extrude(150)
    .rotate((0,0,0), (0,0,1), 150) # Rotate to stick out to the left/back
)

result = result.union(wire_simple)