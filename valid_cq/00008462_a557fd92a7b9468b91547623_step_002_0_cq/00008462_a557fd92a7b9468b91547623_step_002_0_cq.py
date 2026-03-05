import cadquery as cq

# --- Parameters ---

# Main Body
body_width = 12.0
body_height = 12.0
body_depth = 4.0
fillet_radius = 0.5
wall_thickness = 0.5

# Circular Dome
dome_diameter_base = 10.0
dome_diameter_top = 7.0
dome_height = 2.5

# Push Button
button_diameter = 5.0
button_height = 1.5
button_fillet = 0.2

# Metal Bracket/Frame
frame_thickness = 0.3
frame_tab_width = 2.0
frame_tab_length = 1.5
clip_width = 6.0
clip_protrusion = 1.0

# Legs/Terminals
leg_width = 1.0
leg_thickness = 0.3
leg_offset_y = 3.5  # Distance from center to leg
leg_length_out = 3.0
leg_bend_radius = 1.0

# --- Geometry Construction ---

# 1. Main Plastic Body
# Start with the base square block
body = (cq.Workplane("XY")
    .box(body_width, body_height, body_depth)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. The circular dome on top
dome = (cq.Workplane("XY")
    .workplane(offset=body_depth/2)
    .circle(dome_diameter_base/2)
    .workplane(offset=dome_height)
    .circle(dome_diameter_top/2)
    .loft(combine=True)
)

# Combine body and dome (though loft might be separate initially, better to fuse)
main_shape = body.union(dome)

# 3. The Push Button
# Create a cylinder on top of the dome
button = (cq.Workplane("XY")
    .workplane(offset=body_depth/2 + dome_height)
    .circle(button_diameter/2)
    .extrude(button_height)
    .edges(">Z")
    .fillet(button_fillet)
)

main_shape = main_shape.union(button)

# 4. Metal Frame/Clip Details
# Top Clip mechanism (simplified representation)
top_clip = (cq.Workplane("XZ")
    .workplane(offset=body_height/2)
    .center(0, body_depth/2 - 1.0)
    .rect(clip_width, 3.0)
    .extrude(clip_protrusion)
)

# Add chamfer/shape to the clip to match the "folded metal" look
# We create a cutter to trim the clip
clip_cut = (cq.Workplane("YZ")
    .workplane(offset=clip_width/2)
    .moveTo(body_depth/2, body_height/2 + clip_protrusion)
    .lineTo(body_depth/2 + 2, body_height/2 + clip_protrusion)
    .lineTo(body_depth/2 + 2, body_height/2 - 1)
    .close()
    .extrude(-clip_width)
)

# Refine the top clip area
# Create a shape that represents the stamped metal top plate
top_plate = (cq.Workplane("XY")
    .workplane(offset=body_depth/2 - 0.1) # slightly embedded
    .rect(body_width + 0.5, body_height + 0.5) # Slightly larger than body
    .extrude(frame_thickness)
)

# Create a cutout in the center for the dome
top_plate = top_plate.cut(
    cq.Workplane("XY")
    .workplane(offset=body_depth/2 - 1)
    .circle(dome_diameter_base/2 + 0.2)
    .extrude(10)
)

# Only keep the "rim" part, intersecting with a box that covers the edges
rim_cutter = (cq.Workplane("XY")
    .workplane(offset=body_depth/2 - 1)
    .rect(body_width - 1.0, body_height - 1.0)
    .extrude(10)
)
top_plate = top_plate.cut(rim_cutter)

# Add side tabs (little rectangular protrusions on the sides)
side_tab_r = (cq.Workplane("YZ")
    .workplane(offset=body_width/2)
    .center(0, 0)
    .rect(1.5, 4.0)
    .extrude(0.5)
)
side_tab_l = (cq.Workplane("YZ")
    .workplane(offset=-body_width/2 - 0.5)
    .center(0, 0)
    .rect(1.5, 4.0)
    .extrude(0.5)
)

main_shape = main_shape.union(top_plate).union(side_tab_r).union(side_tab_l)

# 5. Top complex clip geometry (the folded over part)
# This is a bit stylized based on the image
clip_profile = (cq.Workplane("XZ")
    .workplane(offset=body_height/2)
    .moveTo(-clip_width/2, body_depth/2)
    .lineTo(-clip_width/2, body_depth/2 + 0.5)
    .lineTo(-clip_width/2 + 1, body_depth/2 + 1.2)
    .lineTo(clip_width/2 - 1, body_depth/2 + 1.2)
    .lineTo(clip_width/2, body_depth/2 + 0.5)
    .lineTo(clip_width/2, body_depth/2)
    .close()
    .extrude(1.5) # Stick out from top
)
main_shape = main_shape.union(clip_profile)


# 6. Legs / Terminals
def create_leg(y_offset, side_mirror=1):
    # Determine start plane based on side
    x_offset = (body_width/2) * side_mirror
    
    # Draw path for the leg
    path = (cq.Workplane("XZ")
        .workplane(offset=y_offset)
        .moveTo(x_offset, -1.0) # Start inside body
        .lineTo(x_offset + (1.5 * side_mirror), -1.0) # Come out straight
        .tangentArcPoint((x_offset + (3.0 * side_mirror), -2.5), relative=False) # Bend down
        .lineTo(x_offset + (3.0 * side_mirror), -3.5) # Straight down tip
    )
    
    # Create the profile to sweep
    profile = (cq.Workplane("YZ")
        .workplane(offset=x_offset)
        .moveTo(0, y_offset)
        .rect(leg_thickness, leg_width)
    )
    
    # Simple extrusions are often more robust than sweeps for simple bent sheet metal
    # Let's model it with extrusions for stability
    
    part1 = (cq.Workplane("XY")
             .workplane(offset=-1.0)
             .center(x_offset, y_offset)
             .rect(0.1, leg_width) # anchor
             .extrude(leg_thickness)
             )
    
    # Leg coming out
    leg_geo = (cq.Workplane("XY")
        .workplane(offset=-1.0)
        .moveTo(x_offset, y_offset + leg_width/2)
        .lineTo(x_offset, y_offset - leg_width/2)
        .lineTo(x_offset + (2.0 * side_mirror), y_offset - leg_width/2)
        .lineTo(x_offset + (2.0 * side_mirror), y_offset + leg_width/2)
        .close()
        .extrude(leg_thickness)
    )
    
    # The S-bend
    bend_center_x = x_offset + (2.5 * side_mirror)
    bend_center_z = -1.0
    
    # We construct a custom solid for the bent terminal for accuracy to the image
    # Profile on the side face
    leg_sketch = (cq.Workplane("XZ")
        .workplane(offset=y_offset)
        .moveTo(x_offset, -0.5)
        .lineTo(x_offset + (1.5*side_mirror), -0.5) # Straight section out
        .tangentArcPoint([x_offset + (3.0*side_mirror), -2.0], relative=False) # Curve down
        .lineTo(x_offset + (3.0*side_mirror), -2.5) # Short straight tip
        # Thickness
        .lineTo(x_offset + (3.0*side_mirror) - (0.3*side_mirror), -2.5) 
        .tangentArcPoint([x_offset + (1.5*side_mirror), -0.5 - 0.3], relative=False)
        .lineTo(x_offset, -0.5 - 0.3)
        .close()
        .extrude(leg_width/2, both=True)
    )

    return leg_sketch

# Create 2 legs on the left side
leg1 = create_leg(leg_offset_y, side_mirror=-1)
leg2 = create_leg(-leg_offset_y, side_mirror=-1)

# Union everything
result = main_shape.union(leg1).union(leg2)

# Rotate to match image orientation roughly (Optional, but good for preview)
# The image shows Isometric view
result = result.rotate((0,0,0), (1,0,0), -90).rotate((0,0,0), (0,0,1), -45)