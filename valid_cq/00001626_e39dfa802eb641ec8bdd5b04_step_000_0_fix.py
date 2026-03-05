import cadquery as cq

# Main base plate
base_length = 120
base_width = 40
base_height = 6

result = cq.Workplane("XY").box(base_length, base_width, base_height)

# Add rail/channel on the left side (extending left)
rail_length = 40
rail_width = 8
rail_height = 10

rail = (cq.Workplane("XY")
        .box(rail_length, rail_width, rail_height)
        .translate((-base_length/2 - rail_length/2, 0, (rail_height - base_height)/2))
       )

result = result.union(rail)

# Add small rail channel detail on right side
rail_right = (cq.Workplane("XY")
              .box(10, rail_width, rail_height)
              .translate((base_length/2 + 5, 0, (rail_height - base_height)/2))
             )

result = result.union(rail_right)

# Add three bolt tower blocks on top
tower_w = 18
tower_d = 18
tower_h = 22
tower_positions = [-35, 0, 35]

for tx in tower_positions:
    tower = (cq.Workplane("XY")
             .box(tower_w, tower_d, tower_h)
             .translate((tx, 0, base_height/2 + tower_h/2))
            )
    result = result.union(tower)

# Cut slots in towers (front and back)
for tx in tower_positions:
    slot_w = 6
    slot_d = 4
    slot_h = tower_h * 0.6
    # front slot
    front_slot = (cq.Workplane("XY")
                  .box(slot_w, slot_d, slot_h)
                  .translate((tx, tower_d/2 - slot_d/2 + 1, base_height/2 + tower_h - slot_h/2))
                 )
    result = result.cut(front_slot)
    # back slot
    back_slot = (cq.Workplane("XY")
                 .box(slot_w, slot_d, slot_h)
                 .translate((tx, -(tower_d/2 - slot_d/2 + 1), base_height/2 + tower_h - slot_h/2))
                )
    result = result.cut(back_slot)
    # side slots
    side_slot_l = (cq.Workplane("XY")
                   .box(slot_d, slot_w, slot_h)
                   .translate((tx - tower_w/2 + slot_d/2 - 1, 0, base_height/2 + tower_h - slot_h/2))
                  )
    result = result.cut(side_slot_l)
    side_slot_r = (cq.Workplane("XY")
                   .box(slot_d, slot_w, slot_h)
                   .translate((tx + tower_w/2 - slot_d/2 + 1, 0, base_height/2 + tower_h - slot_h/2))
                  )
    result = result.cut(side_slot_r)

# Cut threaded holes (represented as cylinders) in towers
for tx in tower_positions:
    hole = (cq.Workplane("XY")
            .cylinder(tower_h, 5)
            .translate((tx, 0, base_height/2 + tower_h/2))
           )
    result = result.cut(hole)

# Add small holes on base plate surface (decorative/mounting holes)
hole_positions_x = [-45, -30, -15, 0, 15, 30, 45]
hole_positions_y = [-12, 12]

for hx in hole_positions_x:
    for hy in hole_positions_y:
        h = (cq.Workplane("XY")
             .cylinder(base_height + 2, 1.5)
             .translate((hx, hy, 0))
            )
        result = result.cut(h)

# Cut a longitudinal slot/channel along the bottom of the base (rail channel)
channel = (cq.Workplane("XY")
           .box(base_length + 10, 6, 4)
           .translate((0, 0, -base_height/2 + 2))
          )
result = result.cut(channel)

# Cut channel groove in the rail
rail_channel = (cq.Workplane("XY")
                .box(rail_length + 2, 4, 6)
                .translate((-base_length/2 - rail_length/2, 0, (rail_height - base_height)/2 - 1))
               )
result = result.cut(rail_channel)