import cadquery as cq

# Parameters
track_width = 30.0
track_height = 8.0
track_length = 30.0
wall_thickness = 2.0
num_ribs = 4

# Dimensions for the T-slot-like profile
rib_width = 2.0
rib_spacing = (track_width - num_ribs * rib_width) / (num_ribs - 1) if num_ribs > 1 else 0
flange_width = 4.0  # Width of the top T-part
flange_thickness = 1.5
base_thickness = 2.0
channel_depth = track_height - base_thickness

# Side panel dimensions
panel_height = 40.0
panel_thickness = 2.0
panel_width = 20.0
panel_gap = 5.0 # Gap between the two hanging panels

# 1. Create the main track profile (the top part with ribs)
# We will sketch the cross-section on the XZ plane and extrude in Y

def create_track_profile():
    # Base rectangle
    sketch = cq.Sketch().rect(track_width, track_height)
    
    # We need to cut out the spaces between ribs to form the T-shapes
    # The profile looks like a base plate with T-shaped walls rising up
    
    # Let's try an additive approach instead.
    # Base plate
    s = cq.Workplane("XY").box(track_width, track_length, base_thickness)
    
    # Create the ribs (stems)
    # Calculate starting position (centered)
    start_x = -track_width / 2 + rib_width / 2
    
    # Creating a compound profile to extrude
    profile_sketch = cq.Workplane("XZ").center(0, base_thickness/2)
    
    # Calculate spacing for the repeating pattern
    # Total width is track_width
    # We have 'num_ribs'
    # Pitch is track_width / num_ribs roughly, but let's be more precise
    pitch = track_width / num_ribs
    
    # Let's draw the full cross section in 2D first
    # Points for the cross section
    pts = []
    
    # Helper to create the T-shape profile
    # We'll draw the negative space (the channels) and cut them from a block? 
    # Or draw the positive shape? Positive shape is usually robust.
    
    # Let's define the solid block first then cut channels.
    # Total block
    solid_block = cq.Workplane("XY").box(track_width, track_length, track_height)
    
    # Cut 1: The main channel underneath the T-flanges? No, the image shows distinct T-profiles.
    # It looks like a solid base with T-profiles sticking up.
    
    # Let's restart the approach: Create the 2D profile on XZ plane and extrude Y.
    
    # Origin at center bottom of the track
    s = cq.Workplane("XZ")
    
    # Draw the base
    s = s.moveTo(-track_width/2, 0).lineTo(track_width/2, 0).lineTo(track_width/2, base_thickness).lineTo(-track_width/2, base_thickness).close()
    base = s.extrude(track_length)
    
    # Draw the T-ribs
    # Rib dimensions
    stem_h = track_height - base_thickness - flange_thickness
    
    ribs = []
    
    # Calculate centers for ribs to distribute them evenly
    # The image shows ribs spanning the whole width.
    # Let's assume equal spacing.
    spacing = track_width / num_ribs
    first_center_x = -track_width/2 + spacing/2
    
    for i in range(num_ribs):
        center_x = first_center_x + i * spacing
        
        # Draw Stem
        stem = (cq.Workplane("XZ")
                .workplane(offset=-track_length/2) # align with base
                .center(center_x, base_thickness)
                .rect(rib_width, stem_h, centered=(True, False)) # Anchor bottom center
                .extrude(track_length))
        
        # Draw Flange (Top of T)
        flange = (cq.Workplane("XZ")
                  .workplane(offset=-track_length/2)
                  .center(center_x, track_height - flange_thickness)
                  .rect(flange_width, flange_thickness, centered=(True, False))
                  .extrude(track_length))
        
        ribs.append(stem)
        ribs.append(flange)
        
    track = base
    for r in ribs:
        track = track.union(r)
        
    return track

# Generate the track
track = create_track_profile()

# 2. Create the left panel (L-shape extension)
# It extends from the side of the track and goes down.
# Based on the image, the left panel connects to the side of the track base.

left_panel_connector = (cq.Workplane("XY")
                        .workplane(offset=base_thickness/2) # Center vertically on the base
                        .center(-track_width/2 - panel_thickness/2, 0) # Position to the left
                        .box(panel_thickness, track_length, base_thickness)) # Extends sideways

# The large vertical plate hanging down on the left
left_vertical_panel = (cq.Workplane("XY")
                       .workplane(offset=0) # Start at z=0 (bottom of track)
                       .center(-track_width/2 - panel_thickness/2, 0)
                       .box(panel_thickness, track_length, panel_height) # Create box
                       .translate((0, 0, -panel_height/2))) # Move down

# 3. Create the right panel
# The right panel seems to hang from the second channel or is attached to the bottom?
# Looking closely at the image, the right panel is narrower and hangs down from underneath the track, 
# seemingly positioned within a specific channel or offset from the center.
# Let's position it offset to the right.

right_panel_offset = track_width/4 # Approximate position
right_vertical_panel = (cq.Workplane("XY")
                        .workplane(offset=0)
                        .center(right_panel_offset, 0)
                        .box(panel_thickness, track_length, panel_height)
                        .translate((0, 0, -panel_height/2)))


# Combine all parts
result = track.union(left_vertical_panel).union(right_vertical_panel)

# Refinement: The left panel in the image looks like an "L" bracket attached to the side.
# The image shows a block attached to the side of the track, then the sheet going down.
# Let's adjust the left connection.

# Create a block attached to the side of the track
side_block_width = 6.0
side_block = (cq.Workplane("XZ")
              .workplane(offset=-track_length/2)
              .moveTo(-track_width/2, 0)
              .lineTo(-track_width/2 - side_block_width, 0)
              .lineTo(-track_width/2 - side_block_width, track_height) 
              .lineTo(-track_width/2, track_height)
              .close()
              .extrude(track_length))

# Now attach the big sheet to the bottom of this side block
left_sheet = (cq.Workplane("XY")
              .workplane(offset=0)
              .center(-track_width/2 - side_block_width + panel_thickness/2, 0) # Align with outer edge
              .box(panel_thickness, track_length, 50.0) # Height 50
              .translate((0, 0, -25.0)))

# The right sheet hangs from *under* the track, roughly aligned with the 3rd rib gap?
# It looks like it slots into the profile. 
# Let's simply attach it to the bottom face of the track at a specific X offset.
right_sheet_x = track_width/2 - (track_width/num_ribs) * 1.5 # Roughly 3/4 way across
right_sheet = (cq.Workplane("XY")
               .workplane(offset=0)
               .center(right_sheet_x, 0)
               .box(panel_thickness, track_length, 40.0)
               .translate((0, 0, -20.0)))

# Re-assembling with the more accurate geometry interpretation
result = track.union(side_block).union(left_sheet).union(right_sheet)

# Apply a fillet to the top edge of the side block to match the smooth look if needed, 
# but sharp corners are standard for extrusions. The image shows standard sharp edges.

# Rotate for better viewing angle similar to image
# (CadQuery usually exports in standard orientation, rotation is for view)
# result = result.rotate((0,0,0), (1,0,0), -90) 

# Export/Show
# show_object(result)