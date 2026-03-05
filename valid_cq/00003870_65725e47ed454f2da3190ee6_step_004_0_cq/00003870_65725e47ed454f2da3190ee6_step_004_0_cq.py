import cadquery as cq
import math

# --- Parameters ---

# Main Base/Backing Plate
base_width = 80.0
base_height = 50.0
base_thickness = 4.0
base_notch_width = 15.0
base_notch_height = 5.0

# Protractor/Arc Vertical Part
arc_radius_outer = 60.0
arc_radius_inner = 15.0  # Cutout radius near the joint
arc_thickness = 4.0
arc_center_offset_y = 10.0 # Height of the center relative to the bottom of this part
slot_length = 8.0
slot_width = 2.5
slot_count = 7
slot_start_angle = 10
slot_end_angle = 80

# Mounting Block (The rectangular protrusion)
block_length = 25.0
block_width = 12.0
block_height = 10.0
block_hole_dia = 3.0

# PCB (The black plate)
pcb_length = 80.0
pcb_width = 60.0
pcb_thickness = 1.6
pcb_cutout_width = 10.0
pcb_cutout_depth = 5.0
pcb_side_cutout_width = 4.0
pcb_side_cutout_depth = 15.0

# Assembly offsets
arc_offset_from_edge = 20.0  # Where the arc part sits relative to the side of the base

# --- Construction ---

# 1. Base Plate (Vertical back plate in the image)
base_plate = (
    cq.Workplane("XZ")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)

# Add a small notch at the bottom center
base_notch = (
    cq.Workplane("XZ")
    .center(0, -base_height/2)
    .rect(base_notch_width, base_notch_height)
    .extrude(base_thickness)
)
base_plate = base_plate.cut(base_notch)


# 2. Arc Part (The vertical quarter-circle part)
# We sketch a quarter circle shape
arc_part = (
    cq.Workplane("YZ")
    .lineTo(0, arc_radius_outer)
    # Create the outer arc
    .radiusArc((arc_radius_outer, 0), -arc_radius_outer)
    .lineTo(0,0)
    .close()
    .extrude(arc_thickness)
)

# Create the radial slots
for i in range(slot_count):
    angle = slot_start_angle + (i * (slot_end_angle - slot_start_angle) / (slot_count - 1))
    
    # Calculate position for the slot
    # Radius to center of slot
    slot_r = arc_radius_outer - 10.0
    
    # We rotate a workplane to cut the slot
    slot_cut = (
        cq.Workplane("YZ")
        .transformed(rotate=(0, 0, angle))
        .center(slot_r, 0)
        .rect(slot_length, slot_width)
        .extrude(arc_thickness)
    )
    arc_part = arc_part.cut(slot_cut)

# Add the mounting block to the arc part
mounting_block = (
    cq.Workplane("YZ")
    .center(block_length/2, block_height/2) 
    .rect(block_length, block_height)
    .extrude(block_width)
)

# Add hole to mounting block
mounting_hole = (
    cq.Workplane("YZ")
    .center(block_length/2, block_height/2)
    .circle(block_hole_dia/2)
    .extrude(block_width)
)
mounting_block = mounting_block.cut(mounting_hole)

# Combine arc and block, moving block to correct side
# The block extrudes in X+, arc extrudes in X+. We want block on one side.
# Let's adjust positions later in assembly, but for now combine locally if needed.
# Actually, looking at the image, the block is attached to the Arc part.
arc_assembly = arc_part.union(mounting_block.translate((0, 0, arc_thickness)))


# 3. PCB (The horizontal plate)
# Basic Rectangle
pcb = (
    cq.Workplane("XY")
    .rect(pcb_length, pcb_width)
    .extrude(pcb_thickness)
)

# Add cutouts to PCB to match image features
# Front notch (for the mounting block)
front_notch = (
    cq.Workplane("XY")
    .center(-pcb_length/2, 0)
    .rect(pcb_cutout_depth*2, pcb_cutout_width) # oversized X to ensure cut
    .extrude(pcb_thickness)
)
pcb = pcb.cut(front_notch)

# Side cutouts/features (simplified based on visual)
side_cutout_1 = (
    cq.Workplane("XY")
    .center(pcb_length/2, pcb_width/4)
    .rect(pcb_side_cutout_depth, pcb_side_cutout_width)
    .extrude(pcb_thickness)
)
side_cutout_2 = (
    cq.Workplane("XY")
    .center(pcb_length/2, -pcb_width/4)
    .rect(pcb_side_cutout_depth, pcb_side_cutout_width)
    .extrude(pcb_thickness)
)
pcb = pcb.cut(side_cutout_1).cut(side_cutout_2)

# Add some holes to the PCB to mimic the image
pcb_holes = (
    cq.Workplane("XY")
    .rect(pcb_length - 10, pcb_width - 10, forConstruction=True)
    .vertices()
    .circle(1.5)
    .extrude(pcb_thickness)
)
pcb = pcb.cut(pcb_holes)

# --- Assembly / Positioning ---

# Position the Base Plate
# Let's assume the intersection of the plates is near the origin
base_plate_moved = base_plate.translate((-base_width/2 + 20, 0, -base_height/2))

# Position the Arc Assembly
# It stands vertically on the PCB, perpendicular to the base plate
arc_assembly_moved = (
    arc_assembly
    .rotate((0,0,0), (1,0,0), -90) # Rotate upright
    .translate((-10, 0, 0)) # Align with PCB cutout
)

# Position the PCB
# It sits horizontally
pcb_moved = pcb.translate((pcb_length/2 - 10, 0, -pcb_thickness))

# Combine everything into one result
# Note: In a real assembly, these would be separate parts. Here we union for a single model visualization.
result = base_plate_moved.union(arc_assembly_moved).union(pcb_moved)

# If you want to color/mate them properly, you'd use an Assembly, but the prompt asks for a 'result' geometry.