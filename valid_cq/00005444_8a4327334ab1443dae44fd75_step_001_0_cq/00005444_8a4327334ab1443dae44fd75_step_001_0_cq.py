import cadquery as cq
import math

# --- Parameters ---

# Extrusion Profile (2020 Aluminum Extrusion approximation)
extrusion_width = 20.0
vertical_length = 600.0
base_length = 300.0
slot_width = 6.0
slot_depth = 6.0

# Base and Top Corners
corner_height = 40.0
corner_radius = 45.0  # Outer radius of the plastic bracket
corner_thickness = 5.0

# Build Plate
plate_radius = 110.0
plate_thickness = 4.0

# Linear Rail / Carriage (Simplified)
carriage_width = 40.0
carriage_height = 60.0
carriage_depth = 20.0
carriage_z_pos = 350.0  # Position up the tower

# Effector / Diagonal Rod connection (Floating piece)
effector_radius = 40.0
effector_thickness = 5.0
rod_length = 250.0
rod_thickness = 4.0


# --- Helper Functions ---

def create_extrusion(length):
    """Creates a simplified 2020 extrusion profile."""
    # Basic square
    sq = cq.Workplane("XY").box(extrusion_width, extrusion_width, length)
    
    # Create slots (subtracting boxes)
    slot_x = cq.Workplane("XY").box(extrusion_width + 1, slot_width, length)
    slot_y = cq.Workplane("XY").box(slot_width, extrusion_width + 1, length)
    
    # Center hole
    core = cq.Workplane("XY").circle(2.5).extrude(length)
    
    profile = sq.cut(slot_x).cut(slot_y).cut(core)
    return profile

def create_corner_bracket(is_top=False):
    """Creates the triangular/rounded corner bracket for the frame."""
    pts = [
        (0, 0),
        (corner_radius, 0),
        (corner_radius, 10), # Small flat
        (10, corner_radius), # Small flat
        (0, corner_radius),
        (0, 0)
    ]
    
    # Base shape - approximate a quarter circle with tangent exits
    base = cq.Workplane("XY") \
        .moveTo(0,0) \
        .lineTo(corner_radius, 0) \
        .radiusArc((0, corner_radius), corner_radius) \
        .close() \
        .extrude(corner_height)
        
    # Cutouts for extrusions
    cut_v = cq.Workplane("XY").box(extrusion_width + 0.5, extrusion_width + 0.5, corner_height + 2)
    cut_h = cq.Workplane("XY").box(corner_radius * 2, extrusion_width + 0.5, extrusion_width + 0.5)
    
    # Position the cuts
    # Vertical extrusion slot is at the corner (0,0)
    cut_v = cut_v.translate((extrusion_width/2, extrusion_width/2, corner_height/2))
    
    # Horizontal extrusion slot
    cut_h = cut_h.translate((corner_radius, extrusion_width/2, extrusion_width/2))
    if is_top:
        # For top bracket, the horizontal cut might be different or absent in this specific view, 
        # but let's assume symmetry for the frame logic.
        # Actually, looking at image, top bracket holds the top of the vertical rail.
        pass

    bracket = base.cut(cut_v).cut(cut_h)
    
    # Add mounting holes (simplified)
    hole_z = corner_height / 2
    bracket = bracket.faces(">X").workplane().center(0, hole_z).circle(2.5).cutThruAll()
    bracket = bracket.faces(">Y").workplane().center(0, hole_z).circle(2.5).cutThruAll()
    
    return bracket

# --- Assembly Construction ---

# 1. Vertical Extrusion
vertical_rail = create_extrusion(vertical_length)
# Shift so base starts at Z=0
vertical_rail = vertical_rail.translate((extrusion_width/2, extrusion_width/2, vertical_length/2))

# 2. Horizontal Extrusion (Base)
base_rail = create_extrusion(base_length)
# Rotate to lie flat along X axis
base_rail = base_rail.rotate((0,0,0), (0,1,0), 90)
# Position
base_rail = base_rail.translate((base_length/2 + extrusion_width, extrusion_width/2, extrusion_width/2))

# 3. Base Corner Bracket
base_bracket = create_corner_bracket(is_top=False)
# The bracket needs to wrap around the origin
base_bracket = base_bracket.translate((0, 0, 0))

# 4. Top Corner Bracket
top_bracket = create_corner_bracket(is_top=True)
# Flip it upside down for the top
top_bracket = top_bracket.rotate((0,0,0), (1,0,0), 180)
# Move to top of vertical rail
top_bracket = top_bracket.translate((0, 0, vertical_length))

# 5. Build Plate
# A simple cylinder
build_plate = cq.Workplane("XY").circle(plate_radius).extrude(plate_thickness)
# Position it roughly centered relative to the implied delta geometry
# Based on image, it sits 'inside' the frame arc
build_plate = build_plate.translate((base_length/2, base_length/2, extrusion_width + 10))

# 6. Carriage (Roller / Linear Guide Block)
carriage = cq.Workplane("XY").box(carriage_width, carriage_depth, carriage_height)
# Add some wheel details (cylinders)
wheel = cq.Workplane("YZ").circle(8).extrude(5)
wheels = (
    wheel.translate((carriage_depth/2 + 2.5, carriage_height/2 - 10, carriage_width/2 + 4))
    .union(wheel.translate((carriage_depth/2 + 2.5, -carriage_height/2 + 10, carriage_width/2 + 4)))
    .union(wheel.translate((carriage_depth/2 + 2.5, carriage_height/2 - 10, -carriage_width/2 - 4)))
    .union(wheel.translate((carriage_depth/2 + 2.5, -carriage_height/2 + 10, -carriage_width/2 - 4)))
)
carriage = carriage.union(wheels)
# Position on the vertical rail
carriage = carriage.translate((extrusion_width/2, -carriage_depth/2, carriage_z_pos))

# 7. Effector / Floating Plate
# A hexagon or pentagon shape with a hole
effector = cq.Workplane("XY").polygon(5, effector_radius * 2).extrude(effector_thickness)
effector = effector.cut(cq.Workplane("XY").circle(effector_radius/2).extrude(effector_thickness))
# Position floating in space, connected by "invisible" rods in this specific requested code structure
# But let's add thin lines to represent rods
effector = effector.translate((base_length/2, base_length/2, carriage_z_pos - 50))

# 8. Diagonal Rods (Representation)
# Line from carriage to effector
start_pt = (extrusion_width/2, -carriage_depth/2, carriage_z_pos)
end_pt = (base_length/2, base_length/2 - effector_radius, carriage_z_pos - 50)

# Create a rod
path = cq.Workplane("XY").moveTo(start_pt[0], start_pt[1]).lineTo(end_pt[0], end_pt[1])
# Since diagonal 3D lines are tricky with simple extrudes, we'll use a rotated cylinder approach
# Calculate vector
dx = end_pt[0] - start_pt[0]
dy = end_pt[1] - start_pt[1]
dz = end_pt[2] - start_pt[2]
dist = math.sqrt(dx**2 + dy**2 + dz**2)

# Create rod at origin along Z
rod = cq.Workplane("XY").circle(rod_thickness/2).extrude(dist)
# Rotate and translate (simplified alignment)
# Finding exact rotation matrix for arbitrary vector is complex in pure CQ without numpy, 
# so we will approximate visual placement for this generated model.
# Visual approximation: The rod goes from the carriage generally towards the center plate.
rod_center_x = (start_pt[0] + end_pt[0]) / 2
rod_center_y = (start_pt[1] + end_pt[1]) / 2
rod_center_z = (start_pt[2] + end_pt[2]) / 2

# We will create a simple thin box to represent the linkage visually connecting them
linkage = cq.Workplane("XY").box(5, 5, dist)
# Rotate it roughly to match
linkage = linkage.rotate((0,0,0), (1, -1, 0), 60) # Tilted down and in
linkage = linkage.translate((rod_center_x, rod_center_y, rod_center_z))


# --- Combine Final Result ---

result = (
    vertical_rail
    .union(base_rail)
    .union(base_bracket)
    .union(top_bracket)
    .union(build_plate)
    .union(carriage)
    .union(effector)
    .union(linkage)
)

# Export or Display
# show_object(result)