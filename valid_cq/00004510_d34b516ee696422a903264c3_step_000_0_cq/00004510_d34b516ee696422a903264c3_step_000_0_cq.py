import cadquery as cq

# Parameters
base_width = 80
base_length = 120
base_height = 10

tower_width = 30
tower_depth = 50
tower_height = 100
tower_x_offset = 0  # Centered X
tower_y_offset = 20 # Offset from back

flywheel_diam = 70
flywheel_thickness = 15
flywheel_axle_height = 80

eccentric_diam = 30
eccentric_thickness = 10
eccentric_offset = 8 # How much off-center the pin is

piston_housing_width = 25
piston_housing_depth = 25
piston_housing_length = 70
piston_angle = -15 # Tilt angle

shaft_diam = 8
handle_diam = 6
handle_length = 40

# --- Base ---
base = cq.Workplane("XY").box(base_width, base_length, base_height)

# --- Main Tower ---
tower = (cq.Workplane("XY")
         .workplane(offset=base_height/2)
         .center(tower_x_offset, tower_y_offset)
         .box(tower_width, tower_depth, tower_height, centered=(True, True, False))
)

# Add axle hole to tower
tower = (tower.faces(">X").workplane()
         .center(0, tower_height - flywheel_axle_height - tower_height/2)
         .hole(shaft_diam + 1) # Clearance hole
)

# Add side hole (decoration/mounting)
tower = (tower.faces(">Y").workplane()
         .center(0, -30)
         .hole(8)
)

# --- Flywheel Assembly ---
# Axle
axle = (cq.Workplane("YZ")
        .center(tower_y_offset, flywheel_axle_height + base_height/2)
        .circle(shaft_diam/2)
        .extrude(tower_width + 40) # Stick out both sides
        .translate((-(tower_width+40)/2, 0, 0))
)

# Main Flywheel
flywheel = (cq.Workplane("YZ")
            .center(tower_y_offset, flywheel_axle_height + base_height/2)
            .circle(flywheel_diam/2)
            .extrude(flywheel_thickness)
            .translate((tower_width/2 + 2, 0, 0)) # Positioned on right side
)

# Eccentric / Crank Disk (on the left side)
eccentric = (cq.Workplane("YZ")
             .center(tower_y_offset, flywheel_axle_height + base_height/2)
             .circle(eccentric_diam/2)
             .extrude(eccentric_thickness)
             .translate((-tower_width/2 - eccentric_thickness - 2, 0, 0))
)

# Crank Pin
crank_pin = (cq.Workplane("YZ")
             .center(tower_y_offset, flywheel_axle_height + base_height/2 + eccentric_offset) # Off-center
             .circle(4)
             .extrude(eccentric_thickness + 5)
             .translate((-tower_width/2 - eccentric_thickness - 2, 0, 0))
)

# Handle (on the flywheel side)
handle = (cq.Workplane("YZ")
          .center(tower_y_offset, flywheel_axle_height + base_height/2)
          # Create a handle extending from the axle
          .circle(handle_diam/2)
          .extrude(handle_length)
          .translate((tower_width/2 + flywheel_thickness + 5, 0, 0))
)

# --- Angled Cylinder/Piston Assembly ---

# Piston Housing Block
piston_housing_base = (cq.Workplane("XY")
    .box(piston_housing_width, piston_housing_depth, piston_housing_length)
    .rotate((0,0,0), (1,0,0), piston_angle) # Tilt it
    .translate((0, -20, 45)) # Position it
)

# Cut the inner bore
piston_housing = (piston_housing_base
                  .faces(">Z").workplane() # Select top face relative to local coords (sort of)
                  .hole(18, depth=piston_housing_length - 5)
)

# Add the slot cut at the top
piston_housing = (piston_housing
                  .faces(">Z").workplane()
                  .rect(10, 30)
                  .cutBlind(-20)
)

# Connecting Rod / Piston shaft
# Simplify as a cylinder inside the housing connecting to the crank
con_rod = (cq.Workplane("XY")
           .circle(5)
           .extrude(60)
           .rotate((0,0,0), (1,0,0), piston_angle)
           .translate((0, -20, 50))
)

# Connection head (loop around crank pin)
con_head = (cq.Workplane("YZ")
            .center(tower_y_offset, flywheel_axle_height + base_height/2 + eccentric_offset)
            .circle(8)
            .extrude(8)
            .translate((-tower_width/2 - eccentric_thickness - 2, 0, 0))
            .cut(crank_pin) # Ensure hole exists
)

# Lower adjustment bolt (simulated)
bolt_head = (cq.Workplane("XY")
             .polygon(6, 12) # Hex head
             .extrude(8)
             .rotate((0,0,0), (1,0,0), piston_angle)
             .translate((0, -42, 20))
)
bolt_shaft = (cq.Workplane("XY")
             .circle(4) 
             .extrude(15)
             .rotate((0,0,0), (1,0,0), piston_angle)
             .translate((0, -42, 20))
)


# Combine all parts
result = (base
          .union(tower)
          .union(axle)
          .union(flywheel)
          .union(eccentric)
          .union(crank_pin)
          .union(handle)
          .union(piston_housing)
          .union(con_rod)
          .union(con_head)
          .union(bolt_head)
          .union(bolt_shaft)
)