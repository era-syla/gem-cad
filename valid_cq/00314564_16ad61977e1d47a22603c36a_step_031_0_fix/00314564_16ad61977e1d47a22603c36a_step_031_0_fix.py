import cadquery as cq

length = 100.0
profile_width = 32.0
profile_height = 60.0
slot_count = 6
slot_width = 3.0
slot_depth = 3.0
wall_thickness = (profile_width - slot_count * slot_width) / (slot_count + 1)

# Compute X positions of slot centers on the Y+ face
start = -profile_width/2 + wall_thickness + slot_width/2
pitch = slot_width + wall_thickness
xs = [start + i * pitch for i in range(slot_count)]

result = (
    cq.Workplane("XY")
      .box(length, profile_width, profile_height)
      .faces(">Y")
      .workplane()
      .pushPoints([(x, 0) for x in xs])
      .rect(length + 2, profile_height + 2)
      .cutBlind(-slot_depth)
)