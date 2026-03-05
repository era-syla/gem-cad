import cadquery as cq
import math

# This appears to be a curved panel/bracket - like a quarter-cylinder section
# with some thickness, featuring screw holes on one face

# Parameters
outer_radius = 80
inner_radius = 70
thickness = 10  # panel thickness (radial)
height = 120    # vertical height
angle = 70      # arc angle in degrees

# Build the curved panel using a swept profile approach
# Create the arc profile in XZ plane, then extrude in Y direction

# Method: create the 2D cross-section (arc annulus) and extrude upward

# The cross section is an annular sector
# We'll build it by creating the outer arc, inner arc, and connecting lines

def make_curved_panel():
    # Create annular sector profile
    # Angles from -angle/2 to +angle/2
    start_angle = -angle / 2
    end_angle = angle / 2
    
    # Convert to radians
    start_rad = math.radians(start_angle)
    end_rad = math.radians(end_angle)
    
    # Points for outer arc
    outer_start = (outer_radius * math.cos(start_rad), outer_radius * math.sin(start_rad))
    outer_end = (outer_radius * math.cos(end_rad), outer_radius * math.sin(end_rad))
    
    # Points for inner arc
    inner_start = (inner_radius * math.cos(start_rad), inner_radius * math.sin(start_rad))
    inner_end = (inner_radius * math.cos(end_rad), inner_radius * math.sin(end_rad))
    
    # Create the profile using wire
    result = (
        cq.Workplane("XY")
        .moveTo(inner_start[0], inner_start[1])
        .lineTo(outer_start[0], outer_start[1])
        .threePointArc(
            (outer_radius, 0),
            (outer_end[0], outer_end[1])
        )
        .lineTo(inner_end[0], inner_end[1])
        .threePointArc(
            (inner_radius, 0),
            (inner_start[0], inner_start[1])
        )
        .close()
        .extrude(height)
    )
    return result

result = make_curved_panel()

# Add small fillets on edges
result = result.edges("|Z").fillet(2)

# Add screw holes on the flat side face
# The flat face at start_angle side - we need to add holes on the curved outer face
# Looking at the image, holes appear to be on one of the flat end faces

# Let's add 3 countersunk/through holes on the flat side face
# The flat faces are at the start and end angles
# Place holes on the larger flat face (the curved outer surface area)

# Add holes through the thickness (radial direction) on the outer curved surface
# Better approach: add holes on the flat vertical face

hole_radius = 3
hole_positions_z = [height * 0.15, height * 0.5, height * 0.82]

start_rad = math.radians(-angle / 2)
# Face normal direction for the start flat face
face_x = math.cos(start_rad)
face_y = math.sin(start_rad)

# Mid radius for hole placement
mid_radius = (inner_radius + outer_radius) / 2

# We'll drill holes through the flat end face at start angle
for z_pos in hole_positions_z:
    hole_x = mid_radius * math.cos(start_rad)
    hole_y = mid_radius * math.sin(start_rad)
    
    result = (
        result
        .workplane(offset=0)
        .transformed(offset=cq.Vector(0, 0, 0))
    )
    break

# Simpler hole approach - cut cylinders
for z_pos in hole_positions_z:
    # Create a cylinder along the face normal direction and subtract
    cyl = (
        cq.Workplane("XY")
        .transformed(offset=cq.Vector(0, 0, z_pos))
        .moveTo(mid_radius * math.cos(start_rad), mid_radius * math.sin(start_rad))
        .circle(hole_radius)
        .extrude(thickness + 5, both=True)
    )
    result = result.cut(cyl)