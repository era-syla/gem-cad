import cadquery as cq

# --- Parametric Dimensions ---
# Based on general AR-15 Lower Receiver Reference Dimensions
# Note: This is a simplified parametric representation for visualization,
# not a precise machining file.

# Overall Dimensions
overall_length = 195.0
mag_well_width = 35.0  # Exterior
mag_well_length = 60.0 # Exterior
mag_well_height = 55.0
receiver_width = 22.5  # Main body width behind mag well
receiver_height = 40.0
buffer_tower_od = 30.0
buffer_tower_id = 25.4 # approx 1 inch
buffer_tower_height = 45.0
trigger_guard_width = 16.0

# Wall Thicknesses
wall_thickness = 3.0

# Pin Locations (relative to different datums, simplified here)
pivot_pin_dia = 6.35
takedown_pin_dia = 6.35
safety_selector_dia = 9.5
trigger_pin_dia = 4.0
hammer_pin_dia = 4.0

# --- Helper Functions ---

def create_mag_well():
    # The front blocky part
    mw = (
        cq.Workplane("XY")
        .box(mag_well_length, mag_well_width, mag_well_height)
        .edges("|Z")
        .fillet(3.0)
    )
    
    # Interior cutout (magazine cavity)
    mw_cutout = (
        cq.Workplane("XY")
        .box(mag_well_length - wall_thickness*2, mag_well_width - wall_thickness*2, mag_well_height + 10)
    )
    
    # Front pivot pin ears
    ears_length = 12.0
    ears = (
        cq.Workplane("XY")
        .center(mag_well_length/2 + ears_length/2 - 2, 0)
        .box(ears_length, 12.0, 15.0) # Simplified shape
        .edges("|Y").fillet(5.9)
    )
    
    # Pivot pin hole
    ears = ears.faces(">X").workplane().hole(pivot_pin_dia, 20.0)

    return mw.cut(mw_cutout).union(ears)

def create_fire_control_group():
    # Main body behind mag well
    fcg_length = 90.0
    fcg = (
        cq.Workplane("XY")
        .center(-mag_well_length/2 - fcg_length/2 + 5, 0) # Overlap slightly
        .box(fcg_length, receiver_width, receiver_height)
    )
    
    # Fire control pocket (internal)
    pocket = (
        cq.Workplane("XY")
        .center(-mag_well_length/2 - fcg_length/2 + 5, 0)
        .workplane(offset=5) # Floor thickness
        .box(fcg_length - 15, receiver_width - wall_thickness*2, receiver_height)
    )
    
    # Add Trigger/Hammer pin holes
    # Positioning is approximate relative to the box center
    fcg = fcg.faces(">Y").workplane() \
        .center(-15, 5) \
        .circle(trigger_pin_dia/2).cutThruAll() \
        .center(18, 0) \
        .circle(hammer_pin_dia/2).cutThruAll() \
        .center(15, -5) \
        .circle(safety_selector_dia/2).cutThruAll()

    return fcg.cut(pocket)

def create_buffer_tower():
    # The round part at the back
    # Located relative to the rear of the FCG
    fcg_rear_x = -mag_well_length/2 - 90.0 + 5 
    
    tower_center = (fcg_rear_x, 0)
    
    tower = (
        cq.Workplane("XY")
        .center(tower_center[0], tower_center[1])
        .workplane(offset=10) # Lifted slightly
        .circle(buffer_tower_od/2)
        .extrude(buffer_tower_height)
    )
    
    # Threaded hole for buffer tube
    tower_hole = (
        cq.Workplane("XY")
        .center(tower_center[0], tower_center[1])
        .workplane(offset=10)
        .circle(buffer_tower_id/2)
        .extrude(buffer_tower_height + 10)
    )
    
    # Takedown pin lug area (below buffer tower)
    lug = (
        cq.Workplane("XY")
        .center(tower_center[0] + 8, 0)
        .box(25, 12.0, 20.0)
        .edges("|Y").fillet(5)
    )
    
    # Takedown pin hole
    lug = lug.faces(">Y").workplane().hole(takedown_pin_dia, 20.0)

    return tower.cut(tower_hole).union(lug)

def create_trigger_guard_features():
    # The thin loop at the bottom
    # Simplified path
    path = (
        cq.Workplane("XZ")
        .center(0, -mag_well_height/2)
        .moveTo(-10, 0)
        .lineTo(-60, -8)
        .lineTo(-80, 0)
    )
    # Just a visual placeholder for the trigger guard bow area
    # In a stripped lower, this is often open or integral
    # We will make the "integral" style (winter trigger guard)
    
    guard_shape = (
        cq.Workplane("XY")
        .center(-45, 0)
        .workplane(offset=-mag_well_height/2 + 2)
        .box(60, trigger_guard_width, 4)
    )
    
    return guard_shape

def add_magazine_catch_slot(part):
    # Slot on the side
    slot = (
        cq.Workplane("YZ")
        .workplane(offset=mag_well_length/2 - 15)
        .center(0, 5)
        .rect(30, 8)
        .extrude(mag_well_width, both=True)
    )
    return part.cut(slot)

def add_bolt_catch_features(part):
    # Boss on the side
    boss = (
        cq.Workplane("XY")
        .center(-mag_well_length/2 + 5, mag_well_width/2)
        .box(15, 8, 20)
        .edges("|Z").fillet(2)
    )
    return part.union(boss)

# --- Assembly Construction ---

# 1. Magazine Well
mag_well = create_mag_well()

# 2. Fire Control Group Section
fcg = create_fire_control_group()

# 3. Buffer Tower
tower = create_buffer_tower()

# 4. Trigger Guard (Integral style)
guard = create_trigger_guard_features()

# Combine main bodies
main_body = mag_well.union(fcg).union(tower).union(guard)

# Refine Junctions and Details
# Fillet the junction between mag well and FCG
try:
    main_body = main_body.edges(cq.selectors.BoxSelector(
        (-40, -15, -20), (-20, 15, 20)
    )).fillet(5.0)
except:
    pass # Fallback if selector misses

# Add details
main_body = add_magazine_catch_slot(main_body)
main_body = add_bolt_catch_features(main_body)

# Add pistol grip mount stud
grip_mount = (
    cq.Workplane("XZ")
    .center(0, -10) # Centered on XZ plane
    .workplane(offset=-receiver_height/2 + 5) # Bottom of FCG
    .center(-70, 0) # Move back towards rear
    .moveTo(0, 0)
    .lineTo(10, -20)
    .lineTo(35, -20)
    .lineTo(35, 0)
    .close()
    .extrude(receiver_width/2.0, both=True) # Extrude width
)

# Rotate grip mount to angle slightly if needed, but simple extrusion works for visual
main_body = main_body.union(grip_mount)

# Final cleanup cuts to make it look "machined"
# Bolt release plunger hole
bolt_plunger = (
    cq.Workplane("YZ")
    .workplane(offset=-mag_well_length/2 + 5)
    .center(5, 15)
    .circle(2)
    .extrude(20)
)
main_body = main_body.cut(bolt_plunger)

# --- Final Result ---
result = main_body