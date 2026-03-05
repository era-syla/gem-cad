import cadquery as cq
import math

# --- Parametric Dimensions ---
tooth_count = 20          # Number of teeth
pitch = 2.0               # Pitch (distance between teeth, e.g., GT2 standard)
tooth_depth = 0.75        # Depth of the tooth cut
tooth_width_ratio = 0.5   # Ratio of tooth width to pitch

# Pulley Dimensions
pulley_width = 7.0        # Width of the toothed section
flange_thickness = 1.0    # Thickness of the side flanges
flange_diameter_add = 4.0 # How much larger the flange is than the pulley OD
hub_diameter = 12.0       # Diameter of the rear hub
hub_length = 5.0          # Length of the rear hub
bore_diameter = 5.0       # Center hole diameter

# Calculations
# Pitch Diameter (PD) = (N * Pitch) / PI
pitch_radius = (tooth_count * pitch) / (2 * math.pi)
outer_radius = pitch_radius - tooth_depth  # Approximate base radius for the cylinder
flange_radius = outer_radius + (flange_diameter_add / 2)
total_length = pulley_width + (2 * flange_thickness) + hub_length

# --- Tooth Profile Creation ---
# Create a single tooth cutter profile
# A simple trapezoidal or rounded profile works for visualization
def create_tooth_cutter(radius, depth, pitch_val, width_ratio):
    tooth_w = pitch_val * width_ratio
    # Create a shape to cut the tooth gap
    cutter = (
        cq.Workplane("XY")
        .moveTo(radius + depth/2, 0)
        .rect(depth * 2, tooth_w) # Oversized rectangle to ensure cut
        .extrude(pulley_width)
    )
    return cutter

# --- Modeling Steps ---

# 1. Main Body (The central cylinder for teeth)
# We start with the outer diameter cylinder
main_body = cq.Workplane("XY").circle(pitch_radius).extrude(pulley_width)

# 2. Cut Teeth
# We will iterate to cut each tooth slot
for i in range(tooth_count):
    angle = (360.0 / tooth_count) * i
    
    # Define a cutting shape (a simple slot for the tooth gap)
    # Using a trapezoidal-ish cut for a generic timing belt profile
    tooth_gap_width = pitch * (1 - tooth_width_ratio)
    
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=pulley_width/2) # Center cutter vertically on pulley width
        .transformed(rotate=cq.Vector(0, 0, angle))
        .moveTo(pitch_radius, 0)
        .rect(tooth_depth * 4, tooth_gap_width) # Oversized depth to ensure clean cut
        .extrude(pulley_width, both=True)
    )
    
    main_body = main_body.cut(cutter)

# 3. Add Flanges
# Front Flange
front_flange = (
    cq.Workplane("XY")
    .workplane(offset=pulley_width)
    .circle(flange_radius)
    .extrude(flange_thickness)
)

# Rear Flange
rear_flange = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness)
    .circle(flange_radius)
    .extrude(flange_thickness)
)

# 4. Add Rear Hub
hub = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness) # Start from back of rear flange
    .circle(hub_diameter / 2)
    .extrude(-hub_length) # Extrude backwards
)

# 5. Combine Parts
result = main_body.union(front_flange).union(rear_flange).union(hub)

# 6. Central Bore
# Cut the hole through the entire assembly
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(bore_diameter)
)

# Rotate for better isometric viewing similar to image
result = result.rotate((0,0,0), (1,0,0), -90)
