import cadquery as cq
import math

# Parameters
outer_radius = 40
wall_thickness = 3
height = 40
inner_radius = outer_radius - wall_thickness

# Create the main cylindrical shell (hollow cylinder)
outer_cyl = cq.Workplane("XY").circle(outer_radius).extrude(height)
inner_cyl = cq.Workplane("XY").circle(inner_radius).extrude(height)
shell = outer_cyl.cut(inner_cyl)

# Top ring opening - large arc cutout at the top
# Create a large arc slot near the top of the cylinder
# The top has a large circular arc opening (like a C-shape cutout from the top)

# Large arc cutout on top - positioned on the front face
# This is a slot that goes through the top portion of the cylinder wall
# Create arc cutout by cutting a torus-like shape

# Top large arc slot - cut through the wall from the top
arc_cut_height = height * 0.45  # Height of the arc cutout region
arc_cut_start = height - arc_cut_height  # Start from this z height

# Create vertical slots around the cylinder
# Based on image: 4 vertical slots at 90 degree intervals, plus 2 horizontal slots on one side

def make_vertical_slot(angle_deg, slot_width, slot_height, slot_start_z, radius):
    """Create a box cutter for a vertical slot"""
    angle_rad = math.radians(angle_deg)
    x = math.cos(angle_rad) * radius
    y = math.sin(angle_rad) * radius
    
    cutter = (cq.Workplane("XY")
              .transformed(offset=cq.Vector(x, y, slot_start_z))
              .rect(slot_width, wall_thickness * 3)
              .extrude(slot_height))
    return cutter

# Vertical slots - 4 positions at 0, 90, 180, 270 degrees
slot_width = 8
slot_height_lower = height * 0.5
slot_start_lower = 2

# Cut vertical slots through the wall
angles = [0, 90, 180, 270]
for angle in angles:
    angle_rad = math.radians(angle)
    cx = math.cos(angle_rad) * outer_radius * 1.0
    cy = math.sin(angle_rad) * outer_radius * 1.0
    
    cutter = (cq.Workplane("XY")
              .transformed(offset=cq.Vector(cx, cy, slot_start_lower))
              .rect(slot_width, wall_thickness * 4)
              .extrude(slot_height_lower))
    shell = shell.cut(cutter)

# Top arc cutouts - large openings at the top
# Two large arc cutouts at top (front and back areas)
for angle in [45, 225]:
    angle_rad = math.radians(angle)
    cx = math.cos(angle_rad) * outer_radius
    cy = math.sin(angle_rad) * outer_radius
    
    top_cutter = (cq.Workplane("XY")
                  .transformed(offset=cq.Vector(cx, cy, height * 0.55))
                  .rect(outer_radius * 1.2, wall_thickness * 4)
                  .extrude(height * 0.45))
    shell = shell.cut(top_cutter)

# Horizontal slots on the right side (two horizontal rectangular cutouts)
for z_pos in [height * 0.25, height * 0.42]:
    h_cutter = (cq.Workplane("XY")
                .transformed(offset=cq.Vector(outer_radius, 0, z_pos))
                .rect(wall_thickness * 4, 14)
                .extrude(6))
    shell = shell.cut(h_cutter)

# Add a solid bottom
bottom = cq.Workplane("XY").circle(outer_radius).extrude(3)
shell = shell.union(bottom)

# Clean up with small fillets on selected edges
try:
    result = shell.edges("|Z").fillet(1.0)
except:
    result = shell