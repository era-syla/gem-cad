import cadquery as cq

def make_bracket():
    # Dimensions
    plate_w = 8       # vertical plate width
    plate_h = 120     # vertical plate height
    plate_t = 6       # plate thickness
    
    arm_w = 80        # arm horizontal length
    arm_h = 14        # arm height/thickness
    arm_t = 10        # arm depth
    
    gap = 60          # gap between upper and lower arms
    
    # Vertical back plate (L-shaped cross section)
    # Main plate
    back_plate = (
        cq.Workplane("XY")
        .box(plate_t, plate_w, plate_h)
    )
    
    # L-shape flange on back plate (perpendicular flange)
    flange = (
        cq.Workplane("XY")
        .box(plate_w, plate_t, plate_h)
        .translate((plate_w/2 - plate_t/2, plate_w/2 - plate_t/2, 0))
    )
    
    # Combine back plate with flange
    vert = back_plate.union(flange)
    
    # Upper arm
    upper_arm = (
        cq.Workplane("XY")
        .box(arm_w, arm_t, arm_h)
        .translate((arm_w/2 + plate_t/2, 0, plate_h/2 - arm_h/2 - 5))
    )
    
    # Lower arm
    lower_arm = (
        cq.Workplane("XY")
        .box(arm_w, arm_t, arm_h)
        .translate((arm_w/2 + plate_t/2, 0, plate_h/2 - arm_h/2 - 5 - gap - arm_h))
    )
    
    # Combine everything
    bracket = vert.union(upper_arm).union(lower_arm)
    
    # Add holes to upper arm - 5 holes along the arm
    num_holes = 5
    hole_dia = 6
    hole_spacing = (arm_w - 15) / (num_holes - 1)
    
    for i in range(num_holes):
        x_pos = plate_t/2 + 8 + i * hole_spacing
        z_pos = plate_h/2 - arm_h/2 - 5
        bracket = (
            bracket
            .faces(">Y")
            .workplane()
            .center(x_pos - plate_t/2 - arm_w/2 - plate_t/2, z_pos)
            .circle(hole_dia/2)
            .cutThruAll()
        )
    
    # Add holes to lower arm
    for i in range(num_holes):
        x_pos = plate_t/2 + 8 + i * hole_spacing
        z_pos = plate_h/2 - arm_h/2 - 5 - gap - arm_h
        bracket = (
            bracket
            .faces(">Y")
            .workplane()
            .center(x_pos - plate_t/2 - arm_w/2 - plate_t/2, z_pos)
            .circle(hole_dia/2)
            .cutThruAll()
        )
    
    return bracket

# Build single bracket from scratch more simply
def make_single_bracket():
    t = 6   # thickness
    H = 130 # total height
    W = 90  # arm length
    arm_h = 12  # arm cross-section height
    arm_d = 12  # arm depth
    
    # Vertical plate
    vp = cq.Workplane("XY").box(t, arm_d, H)
    
    # Top arm
    ta = cq.Workplane("XY").box(W, arm_d, arm_h).translate((W/2 + t/2, 0, H/2 - arm_h/2))
    
    # Bottom arm
    ba = cq.Workplane("XY").box(W, arm_d, arm_h).translate((W/2 + t/2, 0, -H/2 + arm_h/2))
    
    # L-angle flange behind vertical plate
    fl = cq.Workplane("XY").box(20, t, H).translate((-t/2 - 10 + t/2, arm_d/2 - t/2, 0))
    
    bracket = vp.union(ta).union(ba).union(fl)
    
    # Drill holes in top arm
    n = 5
    for i in range(n):
        xo = t/2 + 10 + i * (W - 20) / (n - 1)
        bracket = bracket.faces(">Y").workplane().center(xo - W/2 - t/2, H/2 - arm_h/2).circle(3).cutThruAll()
    
    # Drill holes in bottom arm
    for i in range(n):
        xo = t/2 + 10 + i * (W - 20) / (n - 1)
        bracket = bracket.faces(">Y").workplane().center(xo - W/2 - t/2, -H/2 + arm_h/2).circle(3).cutThruAll()
    
    return bracket

b1 = make_single_bracket()
b2 = make_single_bracket().translate((110, 20, 0))

result = b1.union(b2)