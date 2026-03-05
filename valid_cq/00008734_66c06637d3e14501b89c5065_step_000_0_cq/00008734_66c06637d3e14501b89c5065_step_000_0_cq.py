import cadquery as cq

# --- Parametric Variables ---
# Main vertical rail dimensions
rail_length = 400.0
rail_width = 30.0
rail_depth = 15.0
wall_thickness = 1.5

# Slot parameters
slot_length = 15.0
slot_width = 4.0
slot_spacing = 30.0

# Horizontal bracket dimensions
bracket_length = 100.0
bracket_width = 35.0  # Slightly wider than the rail
bracket_height = 25.0
bracket_wall_thick = 1.5

# Top Latch/Mechanism
latch_height = 40.0
latch_width = 25.0

# --- Helper Functions ---
def create_channel(length, width, depth, thickness):
    """Creates a C-channel profile extruded to length."""
    pts = [
        (0, 0),
        (width, 0),
        (width, depth),
        (width - thickness, depth),
        (width - thickness, thickness),
        (thickness, thickness),
        (thickness, depth),
        (0, depth),
        (0, 0)
    ]
    return cq.Workplane("XY").polyline(pts).close().extrude(length)

# --- Main Geometry Construction ---

# 1. Main Vertical Rail (C-channel)
# The image shows a C-channel shape.
rail = create_channel(rail_length, rail_width, rail_depth, wall_thickness)

# Add slots to the face of the rail
# We'll create a series of cutouts along the length
# The slots appear in pairs or single lines. Let's approximate the pattern.

# Define the face to cut
rail_face = rail.faces(">Y").workplane()

# Cut lower slots (single column)
for i in range(4):
    y_pos = 30 + (i * slot_spacing)
    rail = (rail.faces(">Y").workplane(centerOption="CenterOfBoundBox")
            .center(0, -rail_length/2 + y_pos)
            .rect(slot_width, slot_length)
            .cutThruAll())

# Cut middle slots (single column, wider spacing)
for i in range(3):
    y_pos = 160 + (i * 50)
    rail = (rail.faces(">Y").workplane(centerOption="CenterOfBoundBox")
            .center(0, -rail_length/2 + y_pos)
            .rect(slot_width, slot_length)
            .cutThruAll())

# Cut upper slots (double column pattern)
upper_start = 320
for i in range(2):
    y_pos = upper_start + (i * 25)
    # Left slot
    rail = (rail.faces(">Y").workplane(centerOption="CenterOfBoundBox")
            .center(-6, -rail_length/2 + y_pos)
            .rect(slot_width, slot_length)
            .cutThruAll())
    # Right slot
    rail = (rail.faces(">Y").workplane(centerOption="CenterOfBoundBox")
            .center(6, -rail_length/2 + y_pos)
            .rect(slot_width, slot_length)
            .cutThruAll())


# 2. Horizontal Bracket
# This looks like a U-shaped piece attached to the side or front.
# Based on the image, it extends perpendicular to the main rail.

bracket_sketch = (cq.Workplane("XZ")
                  .rect(bracket_width, bracket_height)
                  .rect(bracket_width - 2*bracket_wall_thick, bracket_height - 2*bracket_wall_thick)
                  .extrude(bracket_length))

# Position the bracket roughly halfway up
bracket = (bracket_sketch
           .rotate((0,0,0), (0,1,0), -90) # Orient correctly
           .translate((-bracket_length/2 - rail_width/2, rail_depth/2, rail_length/2)) # Move to side
           )

# Add cutout to the bracket (the angled top edge)
bracket_cutout = (cq.Workplane("XY")
                  .moveTo(-bracket_length, 0)
                  .lineTo(0, 0)
                  .lineTo(0, bracket_height)
                  .close()
                  .extrude(bracket_width + 10) # Make it wide enough to cut
                  .translate((-bracket_length - rail_width/2, 0, rail_length/2 - 10))
                  .rotate((0,0,0), (1,0,0), 90)
                  )

# Clean up bracket geometry - simplified representation of the folded sheet metal
# Create a base U-shape extrusion
bracket_profile = (cq.Workplane("YZ")
                   .moveTo(0,0)
                   .lineTo(bracket_width, 0)
                   .lineTo(bracket_width, bracket_height)
                   .lineTo(bracket_width - bracket_wall_thick, bracket_height)
                   .lineTo(bracket_width - bracket_wall_thick, bracket_wall_thick)
                   .lineTo(bracket_wall_thick, bracket_wall_thick)
                   .lineTo(bracket_wall_thick, bracket_height)
                   .lineTo(0, bracket_height)
                   .close()
                   .extrude(bracket_length)
                   )

# Orient and position the bracket
bracket_final = (bracket_profile
                 .rotate((0,0,0), (0,0,1), -90)
                 .translate((-rail_width/2, rail_depth, rail_length/2 - 20))
                 )
# Cut a slope on the end of the bracket
cut_box = (cq.Workplane("XY")
           .rect(bracket_length, bracket_width)
           .extrude(bracket_height)
           .rotate((0,0,0), (0,1,0), -30) # Angled cut
           .translate((-bracket_length - 20, rail_depth, rail_length/2 + 20))
           )

bracket_final = bracket_final.cut(cut_box)


# 3. Top Mechanism (Slider/Latch)
# A piece inside the top of the rail
top_insert = (cq.Workplane("XY")
              .rect(rail_width - 2*wall_thickness - 0.5, rail_depth - wall_thickness - 0.5)
              .extrude(50)
              .translate((rail_width/2, rail_depth/2 + wall_thickness/2, rail_length - 50))
              )

# A tab sticking out the back/side at the top
top_tab = (cq.Workplane("YZ")
           .moveTo(0,0)
           .lineTo(20, 0)
           .lineTo(20, 15)
           .lineTo(5, 15)
           .lineTo(5, 30)
           .lineTo(0, 30)
           .close()
           .extrude(2)
           .translate((rail_width, 0, rail_length - 40))
           )


# 4. Bottom Mechanism (Lock/Stopper)
# A block inside the lower section
bottom_block = (cq.Workplane("XY")
                .rect(rail_width - 4, rail_depth)
                .extrude(25)
                .translate((rail_width/2, rail_depth/2, 80))
                )

# Detail on the bottom block (the square cutout face)
bottom_detail = (cq.Workplane("XZ")
                 .rect(15, 15)
                 .extrude(5)
                 .translate((rail_width/2, 80 + 12.5, rail_depth))
                 )

# Combine everything
result = rail.union(bracket_final).union(top_insert).union(top_tab).union(bottom_block).union(bottom_detail)

# Rotate to match image orientation (standing up, facing somewhat right)
result = result.rotate((0,0,0), (1,0,0), -90).rotate((0,0,0), (0,0,1), 45)