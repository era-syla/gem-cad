import cadquery as cq

# Build a vehicle/chassis frame with two axle assemblies connected by a long frame
# This represents a trailer/chassis frame with wheel hubs at each end

def make_chassis():
    # Main frame rails - two parallel tubes running lengthwise
    frame_length = 200
    frame_width = 20
    rail_height = 6
    rail_width = 4

    # Left rail
    left_rail = (cq.Workplane("XY")
                 .box(frame_length, rail_width, rail_height)
                 .translate((0, frame_width/2, 0)))

    # Right rail
    right_rail = (cq.Workplane("XY")
                  .box(frame_length, rail_width, rail_height)
                  .translate((0, -frame_width/2, 0)))

    # Cross members
    cross1 = (cq.Workplane("XY")
              .box(rail_width, frame_width + rail_width*2, rail_height)
              .translate((-frame_length/2 + 15, 0, 0)))

    cross2 = (cq.Workplane("XY")
              .box(rail_width, frame_width + rail_width*2, rail_height)
              .translate((frame_length/2 - 15, 0, 0)))

    cross3 = (cq.Workplane("XY")
              .box(rail_width, frame_width + rail_width*2, rail_height)
              .translate((0, 0, 0)))

    # Diagonal braces
    diag_length = 60
    diag = (cq.Workplane("XY")
            .box(diag_length, rail_width, rail_height)
            .rotate((0,0,0),(0,0,1), 15)
            .translate((-frame_length/4, 0, rail_height)))

    # Front axle assembly
    axle_width = 50
    axle_tube = (cq.Workplane("XY")
                 .cylinder(axle_width, 3)
                 .rotate((0,0,0),(1,0,0), 90)
                 .translate((frame_length/2 - 15, 0, 0)))

    # Rear axle assembly
    axle_tube2 = (cq.Workplane("XY")
                  .cylinder(axle_width, 3)
                  .rotate((0,0,0),(1,0,0), 90)
                  .translate((-frame_length/2 + 15, 0, 0)))

    # Hub assemblies - front left, front right, rear left, rear right
    hub_r = 12
    hub_t = 6

    def make_hub(x, y, z):
        outer = (cq.Workplane("YZ")
                 .circle(hub_r)
                 .extrude(hub_t)
                 .translate((x, y, z)))
        inner = (cq.Workplane("YZ")
                 .circle(hub_r * 0.5)
                 .extrude(hub_t)
                 .translate((x, y, z)))
        hub = outer.cut(inner)
        # Add center bolt
        bolt = (cq.Workplane("YZ")
                .circle(3)
                .extrude(hub_t + 4)
                .translate((x - 2, y, z)))
        return hub.union(bolt)

    front_left_hub = make_hub(frame_length/2 - 15, axle_width/2 + hub_t/2, 0)
    front_right_hub = make_hub(frame_length/2 - 15, -axle_width/2 - hub_t/2, 0)
    rear_left_hub = make_hub(-frame_length/2 + 15, axle_width/2 + hub_t/2, 0)
    rear_right_hub = make_hub(-frame_length/2 + 15, -axle_width/2 - hub_t/2, 0)

    # Combine all parts
    result = (left_rail
              .union(right_rail)
              .union(cross1)
              .union(cross2)
              .union(cross3)
              .union(axle_tube)
              .union(axle_tube2)
              .union(front_left_hub)
              .union(front_right_hub)
              .union(rear_left_hub)
              .union(rear_right_hub))

    return result

result = make_chassis()