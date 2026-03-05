import cadquery as cq
import math

# ------------------------------------------------------------------
# Parametric Constants for the Extruder Mechanism
# ------------------------------------------------------------------

# NEMA 17 Stepper Motor Dimensions
nema17_width = 42.3
nema17_length = 40.0  # approximate body length
nema17_shaft_diam = 5.0
nema17_boss_diam = 22.0
nema17_boss_height = 2.0
nema17_hole_spacing = 31.0
nema17_hole_diam = 3.2

# Main Body Block dimensions
main_body_thickness = 12.0
main_body_width = 65.0
main_body_height = 55.0

# Gear Dimensions (simplified representations)
large_gear_diam = 55.0
large_gear_thickness = 8.0
large_gear_teeth_count = 43

small_gear_diam = 15.0
small_gear_thickness = 10.0
small_gear_teeth_count = 11

# Idler Block
idler_width = 25.0
idler_height = 20.0
idler_thickness = 10.0

# Filament path
filament_diam = 1.75
filament_channel_diam = 3.5

# ------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------

def create_gear(outer_diam, thickness, num_teeth, bore_diam=0):
    """
    Creates a simplified gear representation with actual teeth cuts.
    """
    # Create the base disc
    gear = cq.Workplane("XY").circle(outer_diam / 2.0).extrude(thickness)
    
    # Cut teeth
    tooth_depth = 2.5
    tooth_width_angular = 360.0 / (num_teeth * 2.0)
    
    # Create a cutting tool for one tooth gap
    cutter = (
        cq.Workplane("XY")
        .moveTo(outer_diam/2 - tooth_depth, -1)
        .lineTo(outer_diam/2 + 1, -2.5)
        .lineTo(outer_diam/2 + 1, 2.5)
        .lineTo(outer_diam/2 - tooth_depth, 1)
        .close()
        .extrude(thickness)
    )
    
    # Cut all teeth using polar array
    for i in range(num_teeth):
        angle = i * (360.0 / num_teeth)
        # We need to rotate the cutter and cut
        rotated_cutter = cutter.rotate((0,0,0), (0,0,1), angle)
        gear = gear.cut(rotated_cutter)

    if bore_diam > 0:
        gear = gear.faces("<Z").workplane().circle(bore_diam / 2.0).cutThruAll()
        
    return gear

def create_nema17_mockup():
    """
    Creates a simplified NEMA 17 motor for visualization/boolean operations.
    """
    # Main body chamfered box
    body = (
        cq.Workplane("XY")
        .rect(nema17_width, nema17_width)
        .extrude(nema17_length)
        .edges("|Z")
        .chamfer(1.0)
    )
    
    # Mounting Boss
    boss = (
        cq.Workplane("XY")
        .workplane(offset=nema17_length)
        .circle(nema17_boss_diam / 2.0)
        .extrude(nema17_boss_height)
    )
    
    # Shaft (with flat)
    shaft_len = 24.0
    shaft = (
        cq.Workplane("XY")
        .workplane(offset=nema17_length + nema17_boss_height)
        .circle(nema17_shaft_diam / 2.0)
        .extrude(shaft_len)
    )
    
    # Cut flat on shaft
    flat_cut = (
        cq.Workplane("XY")
        .workplane(offset=nema17_length + nema17_boss_height)
        .moveTo(nema17_shaft_diam/2 - 0.5, -5)
        .lineTo(10, -5)
        .lineTo(10, 5)
        .lineTo(nema17_shaft_diam/2 - 0.5, 5)
        .close()
        .extrude(shaft_len)
    )
    shaft = shaft.cut(flat_cut)
    
    motor = body.union(boss).union(shaft)
    
    # Mounting holes
    for x in [-1, 1]:
        for y in [-1, 1]:
            hole = (
                cq.Workplane("XY")
                .workplane(offset=nema17_length - 5)
                .center(x * nema17_hole_spacing / 2, y * nema17_hole_spacing / 2)
                .circle(nema17_hole_diam / 2)
                .extrude(10)
            )
            motor = motor.cut(hole)
            
    return motor

# ------------------------------------------------------------------
# Component Construction
# ------------------------------------------------------------------

# 1. Main Extruder Body
# This is a complex shape, built up from a base plate sketch
main_body_pts = [
    (0, 0),
    (65, 0),
    (65, 12),
    (50, 12),
    (50, 45),
    (25, 45),
    (25, 35),
    (0, 35)
]

# Base geometry
extruder_body = (
    cq.Workplane("XY")
    .moveTo(0,0)
    .lineTo(65, 0) # Bottom edge
    .lineTo(75, 15) # Angle up right
    .lineTo(75, 45) # Right edge
    .lineTo(45, 60) # Top angle
    .lineTo(0, 60)  # Top left
    .lineTo(-10, 30) # Angled side near motor
    .close()
    .extrude(main_body_thickness)
)

# Add the motor mounting plate area (vertical)
motor_mount_plate = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(-10, 0)
    .rect(55, 55, centered=False)
    .extrude(5)
).translate((-5, 5, 0))

extruder_body = extruder_body.union(motor_mount_plate)

# Add the filament guide block
guide_block = (
    cq.Workplane("XY")
    .workplane(offset=main_body_thickness)
    .moveTo(40, 20)
    .rect(25, 30)
    .extrude(15)
)
extruder_body = extruder_body.union(guide_block)

# Add Idler Hinge mount
idler_hinge = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(65, 10)
    .circle(6)
    .extrude(main_body_thickness + 10)
)
extruder_body = extruder_body.union(idler_hinge)

# 2. Hotend Mount (The clamp-like structure at the bottom right)
hotend_mount = (
    cq.Workplane("XZ")
    .workplane(offset=-10) # Position in Y roughly
    .moveTo(50, 0)
    .circle(12)
    .extrude(20) # Extrude in Y
).translate((0, 5, 5)) 

# Create the slot for the hotend (Groove Mount)
hotend_cutout = (
    cq.Workplane("XY")
    .center(50, 0)
    .circle(8)
    .extrude(50)
)
# Add a side opening
hotend_side_cut = (
    cq.Workplane("XY")
    .moveTo(50, 0)
    .rect(10, 50)
    .extrude(50)
).translate((5,0,0))

# Refine main body with cuts
extruder_body = extruder_body.cut(hotend_cutout).cut(hotend_side_cut)


# 3. Idler Arm (The swinging part with bearings)
idler_arm = (
    cq.Workplane("XY")
    .moveTo(65, 10)
    .lineTo(40, 10)
    .lineTo(35, 25)
    .lineTo(45, 40)
    .lineTo(70, 40)
    .close()
    .extrude(10)
).translate((0,0, main_body_thickness + 2))

# Idler hinge hole
idler_arm = idler_arm.faces("<Z").workplane().center(65, 10).circle(3.5).cutThruAll()

# Bearing cutout in idler
bearing_cutout = (
    cq.Workplane("YZ")
    .workplane(offset=40)
    .move(25, 5) # Z, Y relative to plane
    .circle(11/2) # 608 bearing approx
    .extrude(10)
)

# 4. Gears

# Large Gear (Hobbed Bolt Gear)
large_gear = create_gear(large_gear_diam, large_gear_thickness, large_gear_teeth_count, bore_diam=8.0)
# Position the large gear
large_gear = large_gear.translate((25, 25, -large_gear_thickness - 2)) 

# Small Gear (Motor Gear)
small_gear = create_gear(small_gear_diam, small_gear_thickness, small_gear_teeth_count, bore_diam=5.0)
# Rotate and position small gear to mesh
small_gear = small_gear.translate((-10, 25, 55)) # Approximate position on motor shaft

# 5. NEMA 17 Motor
motor = create_nema17_mockup()
# Orient and position motor
motor = motor.rotate((0,0,0), (1,0,0), 180) # Flip upside down relative to XY plane
motor = motor.translate((-10, 25, 50 + nema17_length)) # Position above plate

# 6. Final Assembly and Boolean Operations

# Cut motor mounting holes in main body
motor_mount_holes = (
    cq.Workplane("XY")
    .workplane(offset=50) # Above body
    .center(-10, 25) # Center of motor
    .rect(31, 31) # Hole spacing
    .vertices()
    .circle(1.7) # 3.4mm holes
    .extrude(-60) # Cut downwards
)

# Large gear shaft hole through body
main_shaft_hole = (
    cq.Workplane("XY")
    .center(25, 25) # Center of large gear axis
    .circle(11.5) # Bearing OD (608)
    .extrude(30)
)

# Filament Path
filament_path = (
    cq.Workplane("XZ") # Side view plane
    .workplane(offset=-25) # Move to Y center of filament path
    .moveTo(45, 60) # Top
    .lineTo(45, -10) # Bottom
    .polyline([(45, 60), (45, -10)]) # Just a line to sweep or cylinder
)
filament_cyl = (
    cq.Workplane("XY")
    .center(40, 25) # Approx location between gears/idler
    .circle(filament_channel_diam/2)
    .extrude(100)
    .translate((0,0,-20))
)

# Cut the body
final_body = extruder_body.cut(motor_mount_holes).cut(main_shaft_hole).cut(filament_cyl)

# Combine all parts into one assembly object for the result
# Note: In a real CAD workflow, we would keep these as an assembly.
# Here we union them just to produce a single 'result' variable for viewing,
# although they are mechanically separate parts.
result = final_body.union(large_gear).union(small_gear).union(motor).union(idler_arm)

# Add some detailed features to make it look like the image

# Hex nut trap on the body
nut_trap = (
    cq.Workplane("XY")
    .workplane(offset=5)
    .center(55, 45)
    .polygon(6, 7.0) # M4 nut size approx
    .extrude(5)
)
result = result.cut(nut_trap)

# Add the hobbed bolt (simplified)
hobbed_bolt = (
    cq.Workplane("XY")
    .center(25, 25)
    .circle(4)
    .extrude(60)
    .translate((0,0,-10))
)
result = result.union(hobbed_bolt)

# Spring tensioner screws on idler
spring_screws = (
    cq.Workplane("YZ")
    .workplane(offset=70)
    .move(5, 10)
    .circle(2)
    .extrude(40)
)
# Add simplified spring representation
springs = (
    cq.Workplane("YZ")
    .workplane(offset=60)
    .move(15, 10)
    .circle(3)
    .extrude(10)
)
result = result.union(springs)

# Export or Render
if 'show_object' in globals():
    show_object(result)