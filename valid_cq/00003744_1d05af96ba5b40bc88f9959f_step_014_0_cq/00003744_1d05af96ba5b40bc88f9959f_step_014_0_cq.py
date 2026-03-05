import cadquery as cq
import math

# --- Dimensions (Parametric) ---
# Main drum/housing dimensions
drum_radius = 25.0
drum_height = 15.0
drum_wall_thickness = 2.0
boss_radius = 3.5
boss_hole_radius = 1.5

# Back/Left mounting structure dimensions
spine_width = 15.0
spine_height = 80.0
spine_thickness = 4.0
tube_clip_radius = 12.0
tube_clip_thickness = 3.0
tube_clip_opening_angle = 60.0 # degrees

# Top hinge/bracket dimensions
top_bracket_width = 20.0
top_bracket_height = 15.0
top_bracket_angle = 30.0 # approximate angle of the wings

# --- Helper Functions ---

def create_main_housing():
    """Creates the large cylindrical drum housing on the right."""
    # Base cylinder
    housing = cq.Workplane("XY").circle(drum_radius).extrude(drum_height)
    
    # Internal cutout (shelling effect)
    cutout = cq.Workplane("XY").circle(drum_radius - drum_wall_thickness).extrude(drum_height - drum_wall_thickness)
    housing = housing.cut(cutout)
    
    # Add mounting bosses (screw holes)
    # Boss 1 (Top Left)
    boss1_center = (-drum_radius * 0.7, drum_radius * 0.7)
    boss1 = (cq.Workplane("XY")
             .center(boss1_center[0], boss1_center[1])
             .circle(boss_radius)
             .extrude(drum_height)
            )
    boss1_hole = (cq.Workplane("XY")
             .center(boss1_center[0], boss1_center[1])
             .circle(boss_hole_radius)
             .extrude(drum_height)
            )
    
    # Boss 2 (Bottom Right)
    boss2_center = (drum_radius * 0.6, -drum_radius * 0.8)
    boss2 = (cq.Workplane("XY")
             .center(boss2_center[0], boss2_center[1])
             .circle(boss_radius)
             .extrude(drum_height)
            )
    boss2_hole = (cq.Workplane("XY")
             .center(boss2_center[0], boss2_center[1])
             .circle(boss_hole_radius)
             .extrude(drum_height)
            )
            
    housing = housing.union(boss1).cut(boss1_hole)
    housing = housing.union(boss2).cut(boss2_hole)
    
    # Square bottom extension
    extension = (cq.Workplane("XY")
                 .center(-5, -drum_radius)
                 .rect(20, 15)
                 .extrude(drum_height)
                 )
    housing = housing.union(extension)
    
    return housing

def create_spine_and_clips():
    """Creates the vertical spine and the C-clips on the left."""
    
    # The main vertical spine connecting the drum to the clips
    spine = (cq.Workplane("YZ")
             .workplane(offset=-spine_width/2 - 15) # Offset to left of drum
             .rect(spine_height, spine_width)
             .extrude(spine_thickness)
             )
    
    # Move spine to correct position relative to drum
    spine = spine.translate((-15, 0, drum_height/2))

    # Create the C-clip profile (for snapping onto a tube)
    # We create a tube and cut a sector out of it
    clip_outer_r = tube_clip_radius + tube_clip_thickness
    
    clip = (cq.Workplane("XY")
            .circle(clip_outer_r)
            .extrude(spine_width)
            )
    
    clip_hole = (cq.Workplane("XY")
                 .circle(tube_clip_radius)
                 .extrude(spine_width)
                 )
    
    # Create the opening for the C-clip
    opening_width = 2 * clip_outer_r * math.sin(math.radians(tube_clip_opening_angle/2))
    opening = (cq.Workplane("XY")
               .center(-clip_outer_r, 0)
               .rect(clip_outer_r, opening_width * 2) # Make it large enough
               .extrude(spine_width)
               )
    
    final_clip = clip.cut(clip_hole).cut(opening)
    
    # Rotate and position the clip
    final_clip = final_clip.rotate((0,0,0), (1,0,0), 90) # Stand it up
    final_clip = final_clip.translate((-15 - spine_thickness, 0, drum_height/2))
    
    # There are two clips, top and bottom, or one long one? 
    # Image suggests a complex structure. Let's make a top and bottom section cut.
    # Actually, looking closely, it's a long vertical spine with a clip shape on the back.
    # Let's refine: The spine IS the back of the clip structure.
    
    # Alternative approach: Extrude the profile of the clip + spine
    path = cq.Workplane("XZ").moveTo(0, 0).lineTo(0, spine_height).wire()
    
    # Define the cross-section of the clip area
    # This is a simplified profile based on the left side of the image
    s = cq.Workplane("XY")
    
    # The semi-circle part
    s = s.moveTo(-25, 10).threePointArc((-35, 0), (-25, -10))
    s = s.lineTo(-22, -10).lineTo(-22, 10).close()
    
    # Let's stick to constructive solid geometry for robustness
    
    # Refined Clip Geometry
    # Lower Clip
    lower_clip = final_clip.translate((0, -15, 0))
    # Upper Clip portion
    upper_clip = final_clip.translate((0, 25, 0))
    
    # Connecting block between clips and drum
    connector = (cq.Workplane("YZ")
                 .workplane(offset=-25)
                 .rect(60, 15)
                 .extrude(10)
                 )
    connector = connector.translate((-5, 5, drum_height/2))
    
    return lower_clip.union(upper_clip).union(connector)


def create_top_mechanism():
    """Creates the angled bracket at the top."""
    # Triangle/Wedge shape
    wedge_height = 15.0
    wedge_width = 18.0
    wedge_depth = 20.0
    
    pts = [
        (0, 0),
        (wedge_width, 0),
        (wedge_width/2, wedge_height)
    ]
    
    wedge = (cq.Workplane("YZ")
             .polyline(pts).close()
             .extrude(wedge_depth)
             )
    
    # Position it on top of the structure
    wedge = wedge.translate((-20, 30, 0))
    
    # Hollow out the middle to make it two flanges
    cutout_width = 6.0
    cutout = (cq.Workplane("YZ")
              .workplane(offset=(wedge_depth - cutout_width)/2)
              .polyline(pts).close()
              .extrude(cutout_width)
              ).translate((-20, 30, 0))
              
    bracket = wedge.cut(cutout)
    
    # Add pin holes
    pin_hole = (cq.Workplane("YZ")
                .center(wedge_width/2, wedge_height*0.6)
                .circle(1.5)
                .extrude(wedge_depth + 10)
                ).translate((-20 - 5, 30, 0)) # -5 to ensure cut through
                
    bracket = bracket.cut(pin_hole)
    
    return bracket

def create_internal_ribs():
    """Adds the complex internal ribbing seen in the cutaway."""
    # A reinforcing rib connecting the drum to the back spine
    rib = (cq.Workplane("XY")
           .rect(20, 4)
           .extrude(drum_height)
           )
    rib = rib.translate((-15, 10, drum_height/2))
    return rib

# --- Assembly ---

# 1. Main Housing
part = create_main_housing()

# 2. Add Spine/Clips
clips = create_spine_and_clips()
part = part.union(clips)

# 3. Add Top Bracket
top_bracket = create_top_mechanism()
part = part.union(top_bracket)

# 4. Refine Transitions (Fillets/Chamfers)
# This is a best-effort approximation of the organic transitions
try:
    part = part.faces("|Z").fillet(0.5)
except:
    pass # Fillets can fail on complex unions

# 5. Specific Feature: The slot on the left spine (middle)
slot_cutter = (cq.Workplane("YZ")
               .rect(10, 4)
               .extrude(15)
               ).translate((-30, 0, drum_height/2))
part = part.cut(slot_cutter)

# 6. Specific Feature: Center alignment tab/rib
center_rib = (cq.Workplane("XY")
              .center(-12, 0)
              .rect(10, 2)
              .extrude(drum_height)
              )
part = part.union(center_rib)


# Final Result
result = part