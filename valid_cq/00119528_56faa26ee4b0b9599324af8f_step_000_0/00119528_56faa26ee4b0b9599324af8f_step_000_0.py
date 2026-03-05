import cadquery as cq

# --- Model Parameters ---
# Base dimensions
base_l = 280
base_w = 150
base_h = 8

# Main Shaft dimensions
shaft_h = 95  # Height from top of base
shaft_dia = 6
shaft_len = 240

# Support Pillars
support_w = 18
support_d = 18
support_spacing = 130 # Distance between pillars

# Flywheel
flywheel_dia = 150
flywheel_rim_w = 15
flywheel_rim_t = 4
flywheel_pos = 40 # Offset from center along shaft

# Fan
fan_dia = 90
fan_pos = -100 # Offset from center
fan_hub_dia = 16

# Cylinders
piston_dia = 24
displacer_dia = 34
cyl_h = 45

# --- Helper Functions ---

def create_base():
    # Main plate with chamfered edges
    b = (cq.Workplane("XY")
         .box(base_l, base_w, base_h)
         .edges("|Z").fillet(6)
         )
    # Mounting holes at corners
    holes = (b.faces(">Z").workplane()
             .rect(base_l - 20, base_w - 20, forConstruction=True)
             .vertices()
             .hole(6)
             )
    return holes

def create_support_pillar():
    # Vertical column
    pillar = (cq.Workplane("XY")
              .box(support_w, support_d, shaft_h)
              .translate((0, 0, shaft_h/2 + base_h/2))
              )
    # Top bearing housing
    bearing = (cq.Workplane("XZ")
               .workplane(offset=-support_d/2)
               .center(0, shaft_h + base_h/2)
               .circle(12)
               .extrude(support_d)
               )
    # Bottom flange
    flange = (cq.Workplane("XY")
              .circle(18)
              .extrude(4)
              .translate((0, 0, base_h/2))
              )
    # Flange bolts
    flange = (flange.faces(">Z").workplane()
              .polarArray(15, 0, 360, 4)
              .circle(1.5)
              .cutThruAll()
              )
    return pillar.union(bearing).union(flange)

def create_flywheel():
    # Center of shaft
    center_z = shaft_h + base_h/2
    
    # Rim
    rim = (cq.Workplane("YZ")
           .center(0, center_z)
           .circle(flywheel_dia/2)
           .circle(flywheel_dia/2 - flywheel_rim_t)
           .extrude(flywheel_rim_w)
           .translate((flywheel_pos, 0, 0))
           )
    
    # Hub
    hub = (cq.Workplane("YZ")
           .center(0, center_z)
           .circle(10)
           .extrude(flywheel_rim_w)
           .translate((flywheel_pos, 0, 0))
           )
    
    # Spokes (Simple cross pattern)
    spoke_v = (cq.Workplane("XY")
               .box(4, flywheel_dia - 2, flywheel_rim_w)
               .rotate((0,0,0), (1,0,0), 90)
               .translate((flywheel_pos + flywheel_rim_w/2, 0, center_z))
               )
    spoke_h = (cq.Workplane("XY")
               .box(4, flywheel_dia - 2, flywheel_rim_w)
               .rotate((0,0,0), (1,0,0), 0) # Flat? No, needs to be vertical cross
               .rotate((0,0,0), (0,1,0), 90) # Rotate to YZ plane alignment
               # Actually simpler to just build another box in YZ orientation relative
               )
    # Better spoke construction: rotated boxes
    spoke1 = (cq.Workplane("XY")
              .box(4, flywheel_dia-2, flywheel_rim_w)
              .rotate((0,0,0),(1,0,0), 90)
              .translate((flywheel_pos + flywheel_rim_w/2, 0, center_z))
              )
    spoke2 = (cq.Workplane("XY")
              .box(flywheel_dia-2, 4, flywheel_rim_w)
              .rotate((0,0,0),(1,0,0), 90)
              .translate((flywheel_pos + flywheel_rim_w/2, 0, center_z))
              )
              
    return rim.union(hub).union(spoke1).union(spoke2)

def create_fan():
    center_z = shaft_h + base_h/2
    
    # Hub
    hub = (cq.Workplane("YZ")
           .center(0, center_z)
           .circle(fan_hub_dia/2)
           .extrude(15)
           .translate((fan_pos, 0, 0))
           )
           
    # Function to create a single blade
    def make_blade(angle):
        # Create a curved blade using a tube segment
        blade_r_outer = 45
        blade_r_inner = 43
        blade_width = 30
        
        # Tube sector
        tube = (cq.Workplane("YZ")
                .center(0, center_z)
                .circle(blade_r_outer)
                .circle(blade_r_inner)
                .extrude(blade_width)
                .translate((fan_pos, 0, 0))
                )
        
        # Cutbox to isolate a sector (top sector)
        # Position box to intersect top part
        keeper = (cq.Workplane("YZ")
                  .center(0, center_z)
                  .rect(30, 30) # Width, Height
                  .extrude(blade_width + 10) # Length along X
                  .translate((fan_pos - 5, 0, blade_r_outer)) # Move up
                  )
        
        blade = tube.intersect(keeper)
        
        # Spoke connecting hub to blade
        spoke = (cq.Workplane("YZ")
                 .center(0, center_z)
                 .rect(2, blade_r_outer)
                 .extrude(10)
                 .translate((fan_pos + 10, 0, blade_r_outer/2))
                 )
        
        assembly = blade.union(spoke)
        
        # Rotate around shaft axis
        # Axis start: (fan_pos, 0, center_z), Axis end: (fan_pos+1, 0, center_z)
        return assembly.rotate((fan_pos, 0, center_z), (fan_pos+1, 0, center_z), angle)

    fan = hub
    for i in range(4):
        fan = fan.union(make_blade(i * 90))
        
    return fan

def create_engine_block():
    # Power Cylinder (Finned)
    cyl1 = cq.Workplane("XY").circle(piston_dia/2).extrude(cyl_h)
    # Add Fins
    for i in range(8):
        fin = (cq.Workplane("XY")
               .workplane(offset=15 + i*3.5)
               .circle(piston_dia/2 + 5)
               .extrude(1)
               )
        cyl1 = cyl1.union(fin)
    cyl1 = cyl1.translate((0, 25, base_h/2))
    
    # Displacer Cylinder (Smooth)
    cyl2 = (cq.Workplane("XY")
            .circle(displacer_dia/2)
            .extrude(cyl_h + 15)
            .translate((0, -25, base_h/2))
            )
            
    # Base pads for cylinders
    pads = (cq.Workplane("XY")
            .rect(40, 90)
            .extrude(3)
            .translate((0, 0, base_h/2))
            )
            
    # Connecting Rods (Simplified vertical rods)
    rod1 = (cq.Workplane("XY")
            .circle(2.5)
            .extrude(shaft_h - 10)
            .translate((0, 25, base_h/2 + cyl_h))
            )
    rod2 = (cq.Workplane("XY")
            .circle(2.5)
            .extrude(shaft_h - 15)
            .translate((0, -25, base_h/2 + cyl_h + 10))
            )
            
    # Mechanism on shaft (Cams/Eccentrics)
    cams = (cq.Workplane("YZ")
            .center(0, shaft_h + base_h/2)
            .circle(14)
            .extrude(20)
            .translate((-10, 0, 0))
            )
            
    return cyl1.union(cyl2).union(pads).union(rod1).union(rod2).union(cams)

def create_gears_and_box():
    # Large gear on right side
    gear = (cq.Workplane("YZ")
            .center(0, shaft_h + base_h/2)
            .circle(28)
            .extrude(5)
            .translate((support_spacing/2 - 12, 0, 0))
            )
    
    # Electrical Box
    box = (cq.Workplane("XY")
           .box(40, 30, 15)
           .edges("|Z").fillet(2)
           .translate((base_l/2 - 35, 0, base_h/2 + 7.5))
           )
    lid = (cq.Workplane("XY")
           .box(32, 22, 3)
           .edges("|Z").fillet(1)
           .translate((base_l/2 - 35, 0, base_h/2 + 15 + 1.5))
           )
           
    return gear.union(box).union(lid)

# --- Assembly ---

# Base
base = create_base()

# Supports
s1 = create_support_pillar().translate((-support_spacing/2, 0, 0))
s2 = create_support_pillar().translate((support_spacing/2, 0, 0))

# Main Shaft
shaft = (cq.Workplane("YZ")
         .center(0, shaft_h + base_h/2)
         .circle(shaft_dia/2)
         .extrude(shaft_len)
         .translate((-shaft_len/2, 0, 0))
         )

# Components
flywheel = create_flywheel()
fan = create_fan()
engine = create_engine_block()
details = create_gears_and_box()

# Combine all
result = (base
          .union(s1)
          .union(s2)
          .union(shaft)
          .union(flywheel)
          .union(fan)
          .union(engine)
          .union(details)
          )