import cadquery as cq

# --- Parameters ---
arm_length = 80.0       # Length of the L-bracket arms
width = 40.0            # Height/Width of the bracket strip
thickness = 4.0         # Material thickness
hole_diameter = 6.0     # Diameter of the mounting holes
outer_radius = 6.0      # Fillet radius on the outer corner
hole_positions = [20.0, 50.0] # Distance of hole centers from the end of the arms

# --- Derived Parameters ---
inner_radius = max(0.1, outer_radius - thickness) # Ensure valid inner radius

# --- Modeling ---

# 1. Define the L-shaped profile sketch
# Coordinates define the cross-section on the XY plane.
# Origin (0,0) is the outer corner.
points = [
    (0, arm_length),            # Top of vertical arm
    (thickness, arm_length),    # Inner top
    (thickness, thickness),     # Inner corner
    (arm_length, thickness),    # Inner right
    (arm_length, 0),            # Right tip
    (0, 0)                      # Outer corner (Origin)
]

# 2. Extrude the base shape
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(width)
)

# 3. Apply fillets to the corner edges
# Select edges nearest to the theoretical corners at mid-height
result = (
    result
    .edges(cq.selectors.NearestToPointSelector((0, 0, width/2)))
    .fillet(outer_radius)
    .edges(cq.selectors.NearestToPointSelector((thickness, thickness, width/2)))
    .fillet(inner_radius)
)

# 4. Create mounting holes
# Calculate local coordinates relative to face centers
# Global pos = arm_length - pos_from_end
# Face center = arm_length / 2
# Local pos = (arm_length - pos_from_end) - (arm_length / 2) = arm_length/2 - pos_from_end
local_hole_x = [(arm_length/2 - pos, 0) for pos in hole_positions]

# Cut holes on the X-aligned arm (Front face, Normal -Y)
result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints(local_hole_x)
    .hole(hole_diameter)
)

# Cut holes on the Y-aligned arm (Side face, Normal -X)
result = (
    result
    .faces("<X")
    .workplane()
    .pushPoints(local_hole_x)
    .hole(hole_diameter)
)