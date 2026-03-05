import cadquery as cq
import math

# --- Parameters ---

# General
clearance = 1.0  # Gap between rings

# Inner Wheel (Gear/Spoked)
inner_radius = 25.0
inner_width = 12.0
hub_radius = 6.0
shaft_hole_side = 4.0
spoke_count = 3
spoke_thickness = 3.0
num_teeth = 36
tooth_height = 1.5

# Middle Ring
middle_inner_radius = inner_radius + clearance + tooth_height
middle_thickness = 3.0
middle_outer_radius = middle_inner_radius + middle_thickness
middle_width = 14.0
middle_pattern_depth = 0.5 # For the decorative pockets

# Outer Ring
outer_inner_radius = middle_outer_radius + clearance
outer_thickness = 4.0
outer_outer_radius = outer_inner_radius + outer_thickness
outer_width = 18.0
outer_rib_thickness = 1.0

# --- Helper Functions ---

def create_gear_tooth(r_root, r_tip, width):
    """Creates a simple trapezoidal gear tooth profile."""
    top_width = (2 * math.pi * r_root) / num_teeth * 0.4
    bottom_width = (2 * math.pi * r_root) / num_teeth * 0.6
    
    # Create the tooth profile centered at origin
    tooth_poly = [
        (-bottom_width/2, r_root),
        (-top_width/2, r_tip),
        (top_width/2, r_tip),
        (bottom_width/2, r_root)
    ]
    
    tooth = (
        cq.Workplane("XY")
        .polyline(tooth_poly).close()
        .extrude(width)
        .translate((0, 0, -width/2))
    )
    return tooth

# --- 1. Inner Ring Construction ---

# Basic Rim
inner_rim = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .circle(inner_radius - 2.0) # Rim thickness
    .extrude(inner_width)
    .translate((0, 0, -inner_width/2))
)

# Hub
hub = (
    cq.Workplane("XY")
    .circle(hub_radius)
    .rect(shaft_hole_side, shaft_hole_side) # Square hole
    .extrude(inner_width)
    .translate((0, 0, -inner_width/2))
)

# Spokes (Curved)
spokes = cq.Workplane("XY")
for i in range(spoke_count):
    angle = i * (360.0 / spoke_count)
    
    # Create a curved path for the spoke
    # We define a 3-point arc starting from hub to rim
    p1 = (hub_radius - 1, 0)
    p2 = ((inner_radius + hub_radius)/2, 8) # Control point for curve
    p3 = (inner_radius - 2, 5) # End at rim
    
    # Define the cross section of the spoke
    spoke_geo = (
        cq.Workplane("XY")
        .moveTo(*p1)
        .threePointArc(p2, p3)
        .lineTo(p3[0]-1, p3[1]-3) # Add some thickness logic visually
        .threePointArc((p2[0], p2[1]-3), (p1[0], p1[1]-3))
        .close()
        .extrude(inner_width)
        .translate((0,0,-inner_width/2))
        .rotate((0,0,1), (0,0,0), angle)
    )
    spokes = spokes.union(spoke_geo)

# Gear Teeth
teeth = cq.Workplane("XY")
tooth_shape = create_gear_tooth(inner_radius, inner_radius + tooth_height, inner_width)

for i in range(num_teeth):
    angle = i * (360.0 / num_teeth)
    rotated_tooth = tooth_shape.rotate((0,0,0), (0,0,1), angle - 90) # Adjust -90 to align with Y axis logic
    teeth = teeth.union(rotated_tooth)

inner_assembly = inner_rim.union(hub).union(spokes).union(teeth)
# Rotate inner assembly slightly to match image pose
inner_assembly = inner_assembly.rotate((1,0,0), (0,0,0), 20).rotate((0,1,0), (0,0,0), 30)


# --- 2. Middle Ring Construction ---

middle_ring = (
    cq.Workplane("XY")
    .circle(middle_outer_radius)
    .circle(middle_inner_radius)
    .extrude(middle_width)
    .translate((0, 0, -middle_width/2))
)

# Add triangular pockets/recesses on the outer face
# This is a simplification of the complex truss pattern seen in the image
pocket_width = (2 * math.pi * middle_outer_radius) / 12 # 12 pockets
pocket_h = middle_width * 0.7

# Create a cutter for the pocket
cutter = (
    cq.Workplane("XZ")
    .moveTo(middle_outer_radius, -pocket_h/2)
    .lineTo(middle_outer_radius, pocket_h/2)
    .lineTo(middle_outer_radius - middle_pattern_depth*2, 0) # Depth inward
    .close()
    .extrude(pocket_width * 0.6) # Extrude along circumference tangent
    .translate((0, -pocket_width * 0.3, 0)) # Center it
)

# Apply pockets pattern
for i in range(12):
    angle = i * (360.0 / 12)
    rotated_cutter = cutter.rotate((0,0,0), (0,0,1), angle)
    middle_ring = middle_ring.cut(rotated_cutter)

# Rotate middle ring to create the gimbal effect
middle_ring = middle_ring.rotate((1,0,0), (0,0,0), -15).rotate((0,0,1), (0,0,0), 10)


# --- 3. Outer Ring Construction ---

outer_ring_main = (
    cq.Workplane("XY")
    .circle(outer_outer_radius)
    .circle(outer_inner_radius)
    .extrude(outer_width)
    .translate((0, 0, -outer_width/2))
)

# Create the rectangular/triangular ribbed pattern on the outside
# We will cut rectangular pockets leaving ribs behind
num_outer_sections = 12
angle_per_section = 360.0 / num_outer_sections

outer_ring_patterned = outer_ring_main

# Define the pocket shape to cut out material
# We create a solid block and subtract it from the ring surface
pocket_w_angle = angle_per_section * 0.8 # leaving 20% for ribs
section_arc_length = (2 * math.pi * outer_outer_radius) / num_outer_sections
cut_width = section_arc_length - outer_rib_thickness
cut_height = (outer_width / 2) - (outer_rib_thickness * 1.5)
cut_depth = 1.0

# Create a cutting tool for the grid pattern (top and bottom row)
# This is an approximation of the truss structure
def create_pocket_tool(z_offset, is_triangle=False):
    tool = cq.Workplane("XY").workplane(offset=z_offset)
    
    if is_triangle:
         # Triangle cut for variety like in image
        tool = (tool
            .moveTo(outer_outer_radius + 5, -cut_width/2)
            .lineTo(outer_outer_radius - cut_depth, -cut_width/2)
            .lineTo(outer_outer_radius - cut_depth, cut_width/2)
            .close()
            .extrude(cut_height)
        )
    else:
        # Rectangle cut
        tool = (tool
            .moveTo(outer_outer_radius + 2, -cut_width/2)
            .lineTo(outer_outer_radius - cut_depth, -cut_width/2)
            .lineTo(outer_outer_radius - cut_depth, cut_width/2)
            .lineTo(outer_outer_radius + 2, cut_width/2)
            .close()
            .extrude(cut_height)
        )
    return tool

for i in range(num_outer_sections):
    angle = i * angle_per_section
    
    # Top Row Cuts
    top_cut = (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(0, 0, angle))
        .transformed(offset=cq.Vector(outer_outer_radius, 0, 0.5)) # Slight Z offset from center
        .box(2, cut_width, cut_height, centered=(True, True, False)) # Cut inwards
    )
    
    # Bottom Row Cuts
    bottom_cut = (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(0, 0, angle))
        .transformed(offset=cq.Vector(outer_outer_radius, 0, -0.5 - cut_height)) # Negative Z
        .box(2, cut_width, cut_height, centered=(True, True, False))
    )

    # Diagonal rib logic (simplification: cut a triangle out of the rectangular pocket area)
    # To achieve the diagonal truss look, we simply cut two triangles leaving a diagonal rib
    
    # Simple rectangular pockets for now to match the "grid" look
    outer_ring_patterned = outer_ring_patterned.cut(top_cut).cut(bottom_cut)

# --- Final Assembly ---

# Combine all parts
result = inner_assembly.union(middle_ring).union(outer_ring_patterned)