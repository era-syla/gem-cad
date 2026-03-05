import cadquery as cq

# --- Parameter Definitions ---
thickness = 3.0  # Thickness of all parts

# -- Flexure Part Parameters --
flex_length = 60.0
flex_width = 30.0
num_zags = 6
zag_gap = 1.5  # Width of the cuts
zag_wall = 1.5 # Thickness of the flexure material
zag_amplitude = 12.0 # How deep the cuts go from each side

# -- Square Panel Parameters --
panel_width = 40.0
panel_length = 30.0
slot_width = 10.0
slot_thickness = 3.0 # Matches material thickness usually
tab_width = 6.0
tab_depth = 3.0
small_hole_dia = 2.0

# -- Quarter Circle Part Parameters --
qc_radius = 25.0
qc_tab_width = 10.0

# --- Helper Function: Flexure Cut Profile ---
def create_flexure_cuts(length, width, n_zags, amplitude, gap):
    """
    Creates the zigzag cut pattern. This is tricky. 
    It's easier to make a solid block and subtract alternating wedges or rectangles.
    Let's use a subtraction approach with alternating rectangles for simplicity.
    """
    cuts = cq.Workplane("XY")
    
    # Calculate spacing
    step = length / n_zags
    
    for i in range(n_zags):
        x_pos = -length/2 + i * step + step/2
        
        # Cut coming from +Y
        cut_top = (cq.Workplane("XY")
                   .center(x_pos, width/2 - amplitude/2)
                   .rect(gap, amplitude)
                   .extrude(thickness))
        
        # Cut coming from -Y (offset by half a step usually, but looking at image, they are opposed)
        # Actually, looking closely at the image, they are triangular/trapezoidal cuts.
        # Let's approximate with alternating thin triangles to make a flexure hinge.
        
        # Revised approach: Triangular cuts
        # Top triangles pointing down
        p1_top = (x_pos - step/2 + gap/2, width/2)
        p2_top = (x_pos, width/2 - amplitude)
        p3_top = (x_pos + step/2 - gap/2, width/2)
        
        cut_tri_top = (cq.Workplane("XY")
                       .polyline([p1_top, p2_top, p3_top])
                       .close()
                       .extrude(thickness))
        
        cuts = cuts.union(cut_tri_top)
        
        # Bottom triangles pointing up (interleaved)
        # We need an extra set of cuts for the bottom, shifted
        x_pos_bot = x_pos + step/2
        if i < n_zags - 1: # Don't go off the end
             p1_bot = (x_pos_bot - step/2 + gap/2, -width/2)
             p2_bot = (x_pos_bot, -width/2 + amplitude)
             p3_bot = (x_pos_bot + step/2 - gap/2, -width/2)
             
             cut_tri_bot = (cq.Workplane("XY")
                           .polyline([p1_bot, p2_bot, p3_bot])
                           .close()
                           .extrude(thickness))
             cuts = cuts.union(cut_tri_bot)

    return cuts

# --- Part 1: The Flexure Component (Left) ---
# Base block
flex_base = cq.Workplane("XY").box(flex_length, flex_width, thickness)

# Generate triangular cuts
# Note: The visual logic in the image creates a specific zig-zag pattern. 
# We will create a simplified version using alternating triangles.
cuts = cq.Workplane("XY")
cut_width = (flex_length / num_zags) * 0.8
cut_depth = flex_width * 0.8
spacing = flex_length / num_zags

for i in range(num_zags):
    # Top cut
    x_loc = -flex_length/2 + (i * spacing) + spacing/2
    tri_top = (cq.Workplane("XY")
               .moveTo(x_loc - cut_width/2, flex_width/2)
               .lineTo(x_loc, flex_width/2 - cut_depth)
               .lineTo(x_loc + cut_width/2, flex_width/2)
               .close()
               .extrude(thickness))
    cuts = cuts.union(tri_top)
    
    # Bottom cut (shifted)
    if i < num_zags:
        x_loc_b = x_loc + spacing/2
        # Check boundary
        if x_loc_b < flex_length/2 - spacing/4:
            tri_bot = (cq.Workplane("XY")
                       .moveTo(x_loc_b - cut_width/2, -flex_width/2)
                       .lineTo(x_loc_b, -flex_width/2 + cut_depth)
                       .lineTo(x_loc_b + cut_width/2, -flex_width/2)
                       .close()
                       .extrude(thickness))
            cuts = cuts.union(tri_bot)

part1 = flex_base.cut(cuts)

# Add the notch feature on the right end of Part 1
notch_cut = (cq.Workplane("XY")
             .rect(tab_width, tab_depth)
             .extrude(thickness)
             .translate((flex_length/2, 0, 0)))

# Add small locking nub
nub_cut = (cq.Workplane("XY")
           .rect(2, 2)
           .extrude(thickness)
           .translate((flex_length/2 - 2, tab_width/2 + 1, 0))) # Approximate pos

part1 = part1.cut(notch_cut)


# --- Part 2: The Quarter Circle (Top Middle) ---
part2_base = (cq.Workplane("XY")
              .lineTo(qc_radius, 0)
              .lineTo(qc_radius, qc_radius)
              .lineTo(0, qc_radius) # Square corner? No, it's an arc.
              .close()) 

# Actually, construct using arc
part2 = (cq.Workplane("XY")
         .moveTo(0,0)
         .lineTo(qc_radius, 0)
         .threePointArc((qc_radius * 0.707, qc_radius * 0.707), (0, qc_radius))
         .close()
         .extrude(thickness))

# Add the stepping/tabs on the straight edges
# Tab on X-axis edge
tab_x = (cq.Workplane("XY")
         .rect(qc_tab_width, tab_depth)
         .extrude(thickness)
         .translate((qc_radius/2, -tab_depth/2, 0)))

# Tab on Y-axis edge
tab_y = (cq.Workplane("XY")
         .rect(tab_depth, qc_tab_width)
         .extrude(thickness)
         .translate((-tab_depth/2, qc_radius/2, 0)))

# It looks like the tabs are actually subtractions (notches) or specific shapes.
# Based on image, the quarter circle has tabs sticking OUT.
# Let's redefine the quarter circle to include the tabs.
part2 = (cq.Workplane("XY")
         .moveTo(0, qc_radius)
         .lineTo(0, 0)
         .lineTo(qc_radius, 0)
         # Arc back
         .threePointArc((qc_radius * 0.707, qc_radius * 0.707), (0, qc_radius))
         .close()
         .extrude(thickness))

# Cut notches into the straight edges instead of adding tabs (matches mating logic usually)
# The image shows tabs protruding.
part2 = part2.union(tab_x).union(tab_y)


# --- Part 3 & 4: The Square/Rectangular Plates (Bottom Middle & Right) ---
# These look identical or mirrored.

def create_panel(rotation=0):
    p = cq.Workplane("XY").box(panel_width, panel_length, thickness)
    
    # Slot (for a tab to fit in)
    slot = (cq.Workplane("XY")
            .rect(slot_width, slot_thickness)
            .extrude(thickness)
            .translate((0, panel_length/2 - slot_thickness, 0))) # Near edge
            
    # Notch/Cutout on the opposite side
    # Complex cutout with a hole
    notch_w = 8.0
    notch_d = 4.0
    notch = (cq.Workplane("XY")
             .rect(notch_w, notch_d)
             .extrude(thickness)
             .translate((0, -panel_length/2 + notch_d/2, 0)))
             
    # Small circular hole in the notch area (likely for a screw/axle)
    hole = (cq.Workplane("XY")
            .circle(small_hole_dia/2)
            .extrude(thickness)
            .translate((0, -panel_length/2 + notch_d/2, 0)))
            
    p = p.cut(slot).cut(notch)
    
    # Add the cross-drilled hole visible in the notch edge? 
    # The image shows a hole through the thickness or a half-circle cutout. 
    # Looks like a cutout.
    
    return p.rotate((0,0,1), (0,0,0), rotation)

part3 = create_panel(0)
part4 = create_panel(90) # Just rotated for variety, though image shows flat

# --- Assembly / Positioning ---
# Move parts to match image layout roughly

# Flexure (Left)
part1 = part1.translate((-60, 0, 0))

# Quarter Circle (Top Middle)
part2 = part2.translate((0, 40, 0))

# Panel 1 (Bottom Middle)
part3 = part3.translate((0, -10, 0))

# Panel 2 (Right)
part4 = create_panel(0).translate((50, 10, 0))

# Combine all into one result for visualization
result = part1.union(part2).union(part3).union(part4)