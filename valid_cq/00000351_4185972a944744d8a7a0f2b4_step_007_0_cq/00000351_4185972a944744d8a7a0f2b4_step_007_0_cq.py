import cadquery as cq

# -- Part 1: Main Flanged Hub (Center) --
# Dimensions
hub_height = 40
hub_od = 15
hub_id = 10
flange_od = 35
flange_thickness = 5
flange_hole_circle_dia = 25
flange_hole_dia = 3
flange_hole_count = 4

# Hub geometry
main_hub = (
    cq.Workplane("XY")
    .circle(flange_od / 2)
    .extrude(flange_thickness)
    .faces(">Z")
    .workplane()
    .circle(hub_od / 2)
    .extrude(hub_height - flange_thickness)
    .faces(">Z")
    .workplane()
    .hole(hub_id)  # Central bore
)

# Flange mounting holes
hub_assembly = (
    main_hub.faces("<Z")
    .workplane()
    .polarArray(flange_hole_circle_dia/2, 0, 360, flange_hole_count)
    .circle(flange_hole_dia / 2)
    .cutThruAll()
)

# -- Part 2: Large Washer/Spacer (Below Hub) --
washer_od = 35
washer_id = 16  # Slightly larger than hub_od for clearance
washer_thickness = 3

washer = (
    cq.Workplane("XY")
    .circle(washer_od / 2)
    .circle(washer_id / 2)
    .extrude(washer_thickness)
    .translate((0, 0, -15)) # Positioning for exploded view
)

# -- Part 3: Top Cap Plate (Left, Top) --
plate_od = 50
plate_thickness = 5
plate_center_hole = 16
plate_mount_hole_circle = 38
plate_mount_hole_dia = 3

top_plate = (
    cq.Workplane("XY")
    .circle(plate_od / 2)
    .extrude(plate_thickness)
    .faces(">Z")
    .workplane()
    .hole(plate_center_hole)
    .faces(">Z")
    .workplane()
    .polarArray(plate_mount_hole_circle/2, 0, 360, 2)
    .hole(plate_mount_hole_dia)
    .translate((-50, 20, 0)) # Position
)

# -- Part 4: Spoked Wheel / Cage (Left, Middle) --
wheel_od = 45
wheel_id = 12
wheel_rim_width = 3
wheel_hub_dia = 18
wheel_thickness = 5
spoke_width = 4

spoked_wheel_outer = cq.Workplane("XY").circle(wheel_od/2).extrude(wheel_thickness)
spoked_wheel_cutout = (
    cq.Workplane("XY")
    .polarArray(16, 0, 360, 4)
    .rect(10, 10) # rough approximation for the cutouts
    .extrude(wheel_thickness)
)
# A simpler approximation of the complex cutout shape
spoked_wheel = (
    cq.Workplane("XY")
    .circle(wheel_od / 2)
    .circle(wheel_od / 2 - wheel_rim_width)
    .extrude(wheel_thickness)
    .union(
        cq.Workplane("XY").circle(wheel_hub_dia/2).circle(wheel_id/2).extrude(wheel_thickness)
    )
)
# Add spokes
spoke = cq.Workplane("XY").rect(wheel_od, spoke_width).extrude(wheel_thickness)
spoke2 = cq.Workplane("XY").rect(spoke_width, wheel_od).extrude(wheel_thickness)

spoked_wheel = spoked_wheel.union(spoke).union(spoke2).cut(cq.Workplane("XY").circle(wheel_id/2).extrude(wheel_thickness))

# Add mounting holes
spoked_wheel = (
    spoked_wheel.faces(">Z")
    .workplane()
    .polarArray(32/2, 45, 360, 4)
    .hole(2.5)
    .translate((-50, -20, 0))
)

# -- Part 5: Hex Nut (Top Center) --
nut_size = 30 # flat to flat
nut_thickness = 5
nut_thread_dia = 15

hex_nut = (
    cq.Workplane("XY")
    .polygon(6, nut_size)
    .extrude(nut_thickness)
    .faces(">Z")
    .workplane()
    .hole(nut_thread_dia)
    .translate((10, 30, 40))
)

# -- Part 6: Motor Mount Bracket (Right, Bottom) --
mount_boss_dia = 45
mount_width = 45
mount_length = 70 # Total length including the square part
mount_thickness = 10
mount_bore = 22
side_hole_dia = 3

# Base circle
bracket_base = cq.Workplane("XY").circle(mount_boss_dia/2).extrude(mount_thickness)

# Rectangular extension
rect_ext = (
    cq.Workplane("XY")
    .center(mount_length/2 - mount_boss_dia/2, 0)
    .rect(mount_length - mount_boss_dia/2, mount_width)
    .extrude(mount_thickness)
)

bracket = bracket_base.union(rect_ext)

# Center Bore
bracket = bracket.faces(">Z").workplane().hole(mount_bore)

# Mounting holes on face
bracket = (
    bracket.faces(">Z")
    .workplane()
    .polarArray(35/2, 45, 360, 4)
    .hole(3.5)
)

# Side mounting holes
bracket = (
    bracket.faces(">X")
    .workplane()
    .pushPoints([(0, 0), (0, -mount_width/2 + 5)]) # Approximate positions
    .hole(side_hole_dia, depth=10)
    .translate((50, -20, 0))
)

# -- Part 7: Bearing Ring (Top Left) --
bearing_od = 22
bearing_id = 16
bearing_width = 6

bearing = (
    cq.Workplane("XY")
    .circle(bearing_od/2)
    .circle(bearing_id/2)
    .extrude(bearing_width)
    .translate((-20, 50, 0))
)

# -- Part 8: Smaller Locking Ring (Right Middle) --
lock_ring_od = 25
lock_ring_id = 15
lock_ring_thk = 4

lock_ring = (
    cq.Workplane("XY")
    .circle(lock_ring_od/2)
    .circle(lock_ring_id/2)
    .extrude(lock_ring_thk)
    .translate((40, 20, 0))
)

# -- Part 9: Bottom Plate with Grooves (Bottom Center) --
bot_plate_od = 50
bot_plate_thk = 8
bot_plate_id = 18

bot_plate = (
    cq.Workplane("XY")
    .circle(bot_plate_od/2)
    .extrude(bot_plate_thk)
    .faces(">Z")
    .workplane()
    .hole(bot_plate_id)
)

# Side grooves/notches
notch = cq.Workplane("XZ").rect(5, 5).extrude(100) # Cutter
bot_plate = (
    bot_plate.cut(notch.translate((0, bot_plate_od/2, bot_plate_thk/2)))
    .cut(notch.translate((0, -bot_plate_od/2, bot_plate_thk/2)))
)
bot_plate = bot_plate.translate((0, -50, -20))

# -- Part 10: Small Bushings/Collars (Center Stack) --
bushing_od = 14
bushing_id = 8
bushing_h = 6
flange_b_od = 18
flange_b_h = 2

bushing = (
    cq.Workplane("XY")
    .circle(flange_b_od/2)
    .extrude(flange_b_h)
    .faces(">Z")
    .workplane()
    .circle(bushing_od/2)
    .extrude(bushing_h)
    .faces(">Z")
    .workplane()
    .hole(bushing_id)
    .translate((0, 0, -30))
)

bushing_small = (
    cq.Workplane("XY")
    .circle(12/2)
    .extrude(2)
    .faces(">Z")
    .workplane()
    .circle(8/2)
    .extrude(4)
    .faces(">Z")
    .workplane()
    .hole(5)
    .translate((0, 0, -40))
)

# -- Part 11: Small Screws (Scattered) --
def make_screw():
    s = (
        cq.Workplane("XY")
        .circle(3) # Head
        .extrude(3)
        .faces(">Z")
        .workplane()
        .circle(1.5) # Shaft
        .extrude(6)
    )
    return s

screw1 = make_screw().translate((-20, -10, 0))
screw2 = make_screw().translate((60, 20, 0))


# Combine all parts into result
result = (
    hub_assembly
    .union(washer)
    .union(top_plate)
    .union(spoked_wheel)
    .union(hex_nut)
    .union(bracket)
    .union(bearing)
    .union(lock_ring)
    .union(bot_plate)
    .union(bushing)
    .union(bushing_small)
    .union(screw1)
    .union(screw2)
)