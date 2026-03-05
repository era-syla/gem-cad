import cadquery as cq
import math

# --- Parameters ---
thickness = 6.0
leg_height = 300.0
leg_base_depth = 300.0
leg_top_depth = 80.0

# Assembly dimensions
stand_width = 220.0  # Internal width between legs

# Slot Configuration
# Back Panel Slots (Vertical)
back_slot_w = 30.0    # Length of the slot
back_slot_inset = 25.0 # Distance from back edge
back_slot_bot_y = 60.0
back_slot_top_y = 230.0

# Shelf Slots (Angled)
shelf_slot_w = 40.0
shelf_angle = -20.0    # Degrees, sloping down
shelf_start_x = 90.0   # Horizontal position of first slot
shelf_start_y = 170.0  # Vertical position of first slot center
shelf_spread_x = 160.0 # Horizontal distance to second slot

# Derived shelf coordinates
shelf_end_x = shelf_start_x + shelf_spread_x
shelf_end_y = shelf_start_y + (shelf_spread_x * math.tan(math.radians(shelf_angle)))


# --- Helper Function: Create Side Leg ---
def create_leg():
    # 1. Outer Profile
    pts = [
        (0, 0),                 # Bottom-Back
        (leg_base_depth, 0),    # Bottom-Front
        (leg_top_depth, leg_height), # Top-Front
        (0, leg_height)         # Top-Back
    ]
    
    leg = cq.Workplane("XY").polyline(pts).close().extrude(thickness)
    
    # 2. Add Fillets to outline edges
    leg = leg.edges("|Z").fillet(5.0)

    # 3. Internal Cutouts (Creating a diagonal truss look)
    # Cutout 1: Top-Back region
    # Points define a triangle leaving a vertical strut at back and diagonal strut
    c1_pts = [
        (25, 100), 
        (75, 270), 
        (25, 270)
    ]
    cut1 = cq.Workplane("XY").polyline(c1_pts).close().extrude(thickness)
    
    # Cutout 2: Bottom-Front region
    c2_pts = [
        (130, 25), 
        (270, 25), 
        (130, 140)
    ]
    cut2 = cq.Workplane("XY").polyline(c2_pts).close().extrude(thickness)
    
    leg = leg.cut(cut1).cut(cut2)

    # 4. Slots for Back Panel (Vertical slots)
    # Slot 1 (Bottom)
    s1 = cq.Workplane("XY").rect(thickness, back_slot_w).extrude(thickness) \
        .translate((back_slot_inset, back_slot_bot_y, 0))
    # Slot 2 (Top)
    s2 = cq.Workplane("XY").rect(thickness, back_slot_w).extrude(thickness) \
        .translate((back_slot_inset, back_slot_top_y, 0))
        
    leg = leg.cut(s1).cut(s2)

    # 5. Slots for Shelf (Angled slots)
    # Create a cutter centered at origin
    slot_cutter = cq.Workplane("XY").rect(shelf_slot_w, thickness).extrude(thickness)
    
    # Position Slot 1
    sc1 = slot_cutter.rotate((0,0,0), (0,0,1), shelf_angle) \
        .translate((shelf_start_x, shelf_start_y, 0))
        
    # Position Slot 2
    sc2 = slot_cutter.rotate((0,0,0), (0,0,1), shelf_angle) \
        .translate((shelf_end_x, shelf_end_y, 0))
        
    leg = leg.cut(sc1).cut(sc2)
    
    return leg

# --- Helper Function: Create Back Panel ---
def create_back_panel():
    # Height determined by slots plus margin
    panel_h = (back_slot_top_y - back_slot_bot_y) + back_slot_w + 40.0
    panel_w = stand_width
    
    # Base Plate
    panel = cq.Workplane("XY").rect(panel_h, panel_w).extrude(thickness)
    
    # Tabs
    # Calculate distance between centers of slots
    slot_dist = back_slot_top_y - back_slot_bot_y
    
    # Create a tab shape
    tab = cq.Workplane("XY").rect(back_slot_w, thickness * 2).extrude(thickness)
    
    # Union tabs at positions corresponding to slot locations
    # Relative to center of panel
    t1 = tab.translate((slot_dist / 2.0, panel_w / 2.0, 0))
    t2 = tab.translate((-slot_dist / 2.0, panel_w / 2.0, 0))
    t3 = tab.translate((slot_dist / 2.0, -panel_w / 2.0, 0))
    t4 = tab.translate((-slot_dist / 2.0, -panel_w / 2.0, 0))
    
    return panel.union(t1).union(t2).union(t3).union(t4)

# --- Helper Function: Create Shelf ---
def create_shelf():
    # Calculate dimensions based on slot geometry
    dx = shelf_end_x - shelf_start_x
    dy = shelf_end_y - shelf_start_y
    slot_dist = math.sqrt(dx**2 + dy**2)
    
    shelf_depth = slot_dist + shelf_slot_w + 40.0
    shelf_width = stand_width
    
    # Base Plate
    shelf = cq.Workplane("XY").rect(shelf_width, shelf_depth).extrude(thickness)
    
    # Tabs
    # Create tab shape (Correct orientation for shelf sides)
    tab = cq.Workplane("XY").rect(thickness * 2, shelf_slot_w).extrude(thickness)
    
    offset_dist = slot_dist / 2.0
    
    # Tabs on right edge
    t1 = tab.translate((shelf_width / 2.0, offset_dist, 0))
    t2 = tab.translate((shelf_width / 2.0, -offset_dist, 0))
    
    # Tabs on left edge
    t3 = tab.translate((-shelf_width / 2.0, offset_dist, 0))
    t4 = tab.translate((-shelf_width / 2.0, -offset_dist, 0))
    
    return shelf.union(t1).union(t2).union(t3).union(t4)


# --- Generate Parts ---
leg_geo = create_leg()
back_panel_geo = create_back_panel()
shelf_geo = create_shelf()

# --- Assembly Arrangement (Exploded View) ---

# 1. Right Leg
right_leg = leg_geo \
    .rotate((0,0,0), (1,0,0), 90) \
    .translate((stand_width/2.0 + 40, 0, 0))

# 2. Left Leg
left_leg = leg_geo \
    .rotate((0,0,0), (1,0,0), 90) \
    .translate((-stand_width/2.0 - 40, 0, 0))

# 3. Back Panel (Oriented vertically, floating left)
# Initial orientation: Flat XY. Height along X, Width along Y.
# Target: Vertical YZ plane.
back_panel = back_panel_geo \
    .rotate((0,0,0), (0,1,0), -90) \
    .translate((-stand_width - 150, 150, 0))

# 4. Shelf (Oriented horizontally, floating right)
# Initial: Flat XY. Width along X, Depth along Y.
shelf = shelf_geo \
    .translate((stand_width + 150, 100, 0))

# --- Combine into Result ---
result = right_leg.union(left_leg).union(back_panel).union(shelf)