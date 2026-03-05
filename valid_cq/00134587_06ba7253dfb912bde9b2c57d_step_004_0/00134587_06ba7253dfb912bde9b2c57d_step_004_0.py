import cadquery as cq
import math

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
# Main Frame Dimensions
frame_w = 1200.0
frame_d = 1200.0
frame_h = 2500.0
tube_size = 60.0

# Hopper Dimensions
hopper_h_box = 800.0
hopper_h_funnel = 500.0
hopper_outlet_d = 150.0

# Side Tank Dimensions
side_tank_d = 500.0
side_tank_h = 800.0
side_cone_h = 300.0

# Conveyor Dimensions
conv_len = 4500.0
conv_diam = 150.0
conv_angle = 45.0  # Degrees from vertical Z axis towards X

# Control Box
box_size = 700.0

# -----------------------------------------------------------------------------
# Geometry Creation Helpers
# -----------------------------------------------------------------------------

def create_frame():
    """Creates the main support structure."""
    # Vertical Legs
    leg = cq.Workplane("XY").rect(tube_size, tube_size).extrude(frame_h)
    
    legs = (
        leg.translate((frame_w/2, frame_d/2, 0))
        .union(leg.translate((-frame_w/2, frame_d/2, 0)))
        .union(leg.translate((-frame_w/2, -frame_d/2, 0)))
        .union(leg.translate((frame_w/2, -frame_d/2, 0)))
    )
    
    # Horizontal Profiles
    x_bar = cq.Workplane("XY").rect(frame_w + tube_size, tube_size).extrude(tube_size)
    y_bar = cq.Workplane("XY").rect(tube_size, frame_d - tube_size).extrude(tube_size)
    
    # Top Frame Ring
    z_top = frame_h - tube_size
    top_frame = (
        x_bar.translate((0, frame_d/2, z_top))
        .union(x_bar.translate((0, -frame_d/2, z_top)))
        .union(y_bar.translate((frame_w/2, 0, z_top)))
        .union(y_bar.translate((-frame_w/2, 0, z_top)))
    )
    
    # Mid Support Ring
    z_mid = frame_h * 0.5
    mid_frame = (
        x_bar.translate((0, frame_d/2, z_mid))
        .union(x_bar.translate((0, -frame_d/2, z_mid)))
        .union(y_bar.translate((frame_w/2, 0, z_mid)))
        .union(y_bar.translate((-frame_w/2, 0, z_mid)))
    )
    
    return legs.union(top_frame).union(mid_frame)

def create_hopper():
    """Creates the central main hopper with inspection port."""
    z_mid = frame_h * 0.5 + tube_size
    
    # Main cubic body
    body = (
        cq.Workplane("XY")
        .rect(frame_w - tube_size*2, frame_d - tube_size*2)
        .extrude(hopper_h_box)
        .translate((0, 0, z_mid))
    )
    
    # Bottom funnel (loft from rectangle to circle)
    funnel = (
        cq.Workplane("XY")
        .workplane(offset=z_mid)
        .rect(frame_w - tube_size*2, frame_d - tube_size*2)
        .workplane(offset=-hopper_h_funnel)
        .circle(hopper_outlet_d / 2.0)
        .loft(combine=True)
    )
    
    # Side Inspection Port
    port = (
        cq.Workplane("XZ")
        .circle(150)
        .extrude(50)
        .translate((0, z_mid + hopper_h_box/2, frame_d/2 - tube_size))
    )
    
    return body.union(funnel).union(port)

def create_conveyor():
    """Creates the inclined screw conveyor with motor assembly."""
    # Start at the bottom of the hopper funnel
    start_z = (frame_h * 0.5 + tube_size) - hopper_h_funnel
    start_pt = cq.Vector(0, 0, start_z)
    
    # Main Tube (Rotated to incline)
    tube = (
        cq.Workplane("XY")
        .circle(conv_diam / 2.0)
        .extrude(conv_len)
        .rotate((0,0,0), (0,1,0), conv_angle) # Tilt towards +X
        .translate(start_pt)
    )
    
    # Calculate Tip Position for Motor
    rad = math.radians(conv_angle)
    tip_vec = cq.Vector(math.sin(rad), 0, math.cos(rad)).multiply(conv_len)
    tip_pos = start_pt.add(tip_vec)
    
    # Motor Gearbox
    gearbox = (
        cq.Workplane("XY")
        .rect(250, 250)
        .extrude(300)
        .rotate((0,0,0), (0,1,0), conv_angle)
        .translate(tip_pos)
    )
    
    # Motor Cylinder
    motor_cyl = (
        cq.Workplane("XY")
        .circle(100)
        .extrude(300)
        .rotate((0,0,0), (1,0,0), 90) # Perpendicular to flow
        .rotate((0,0,0), (0,1,0), conv_angle)
        .translate(tip_pos)
        .translate((0, 0, 150)) # Offset relative to gearbox center
    )
    
    return tube.union(gearbox).union(motor_cyl)

def create_side_unit():
    """Creates the side tank and overhead beam support."""
    # I-Beam Rail
    beam_len = 1800.0
    w = 120.0 # Flange width
    h = 140.0 # Beam height
    t_web = 10.0
    t_flange = 10.0
    
    # Define I-Beam profile points
    pts = [
        (-w/2, -h/2), (w/2, -h/2), (w/2, -h/2+t_flange), 
        (t_web/2, -h/2+t_flange), (t_web/2, h/2-t_flange),
        (w/2, h/2-t_flange), (w/2, h/2), (-w/2, h/2),
        (-w/2, h/2-t_flange), (-t_web/2, h/2-t_flange),
        (-t_web/2, -h/2+t_flange), (-w/2, -h/2+t_flange)
    ]
    
    ibeam = (
        cq.Workplane("YZ")
        .polyline(pts).close()
        .extrude(beam_len)
        .translate((-beam_len/2 - 200, 0, frame_h + h/2))
    )
    
    # Side Tank Body
    tank_x = -frame_w/2 - 350
    tank_z_base = frame_h * 0.6
    
    cyl = (
        cq.Workplane("XY")
        .circle(side_tank_d / 2.0)
        .extrude(side_tank_h)
        .translate((tank_x, 0, tank_z_base))
    )
    
    cone = (
        cq.Workplane("XY")
        .workplane(offset=tank_z_base)
        .circle(side_tank_d / 2.0)
        .workplane(offset=-side_cone_h)
        .circle(50)
        .loft()
        .translate((tank_x, 0, 0))
    )
    
    # Connecting Duct
    duct = (
        cq.Workplane("XY")
        .circle(60)
        .extrude(abs(tank_x))
        .rotate((0,0,0), (0,1,0), 90)
        .translate((tank_x, 0, tank_z_base + side_tank_h - 200))
    )
    
    return ibeam.union(cyl).union(cone).union(duct)

def create_control_box():
    """Creates the electrical cabinet on the ground."""
    return (
        cq.Workplane("XY")
        .rect(box_size, box_size)
        .extrude(box_size)
        .translate((-frame_w/2 - 100, frame_d/2 + 100, 0))
    )

# -----------------------------------------------------------------------------
# Main Assembly
# -----------------------------------------------------------------------------

part_frame = create_frame()
part_hopper = create_hopper()
part_conveyor = create_conveyor()
part_side_unit = create_side_unit()
part_controls = create_control_box()

# Combine all components
result = (
    part_frame
    .union(part_hopper)
    .union(part_conveyor)
    .union(part_side_unit)
    .union(part_controls)
)