import cadquery as cq

# Parameters
th = 5
boss_r = 3
boss_offset = 8
slot_w = 6
slot_l = 20
hole_r = 1.5
outer_hook_r = 10
inner_hook_r = 7
open_slot_w = 4
open_slot_d = 6

result = (
    cq.Workplane("XY")
    # Base bosses and central slot profile
    .center(-boss_offset, 0).circle(boss_r)
    .center(2 * boss_offset, 0).circle(boss_r)
    .center(-boss_offset, 0).rect(slot_w, slot_l)
    .extrude(th)
    # Drill holes in bosses and cut central square through
    .faces(">Z").workplane()
    .center(-boss_offset, 0).circle(hole_r).cutThruAll()
    .center(2 * boss_offset, 0).circle(hole_r).cutThruAll()
    .center(-boss_offset, 0).rect(4, 4).cutThruAll()
    # Add hook outer profile
    .faces(">Z").workplane()
    .center(0, slot_l / 2).circle(outer_hook_r).extrude(th)
    # Subtract inner hook to make the hook shape
    .faces(">Z").workplane()
    .center(0, slot_l / 2).circle(inner_hook_r).cutThruAll()
    # Cut opening in the hook
    .faces(">Z").workplane()
    .center(0, slot_l / 2 + outer_hook_r - open_slot_d / 2).rect(open_slot_w, open_slot_d).cutThruAll()
)
