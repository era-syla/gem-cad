import cadquery as cq

# --- Parametric Dimensions ---
# Base Dimensions
base_width = 130
base_length = 200
base_height = 30
base_fillet = 20

# Frame Dimensions
frame_width = 65
frame_web_thickness = 14
frame_height = 300
throat_depth = 80  # Distance from ram center to column
column_back_y = -120

# Ram Dimensions
ram_size = 30
ram_length = 260
ram_z_offset = 80

# Pinion/Handle Dimensions
pinion_z = 250
handle_rod_diam = 12
handle_length = 220

# --- 1. Base Construction ---
# Create the main slab of the base with rounded corners
base = (cq.Workplane("XY")
        .moveTo(0, -40)
        .rect(base_width, base_length)
        .extrude(base_height)
        .edges("|Z").fillet(base_fillet)
        .edges(">Z").fillet(3)
       )

# Cut the recess for the anvil plate
base = base.faces(">Z").workplane().circle(62).cutBlind(-5)

# --- 2. Anvil Plate ---
# Create the circular slotted plate
anvil = (cq.Workplane("XY")
         .circle(60)
         .extrude(15)
        )

# Cut slots of varying sizes
for i, width in enumerate([12, 18, 24, 30]):
    angle = i * 90
    slot = (cq.Workplane("XY")
            .moveTo(60, 0)
            .rect(70, width)
            .extrude(15)
            .rotate((0,0,0), (0,0,1), angle)
           )
    anvil = anvil.cut(slot)

# Center hole
anvil = anvil.faces(">Z").workplane().circle(6).cutThruAll()
# Position anvil on base
anvil = anvil.translate((0, 0, base_height))

# --- 3. Main Frame (C-Frame) ---
# Define the outer profile of the casting on the YZ plane
frame_pts = [
    (35, frame_height + 20),   # Top Front
    (35, 210),                 # Head Bottom Front
    (-25, 140),                # Throat inner curve point
    (-35, base_height),        # Leg Front Bottom
    (column_back_y, base_height), # Leg Back Bottom
    (column_back_y, 180),      # Back Vertical end
    (-60, frame_height + 20)   # Top Back
]

frame_solid = (cq.Workplane("YZ")
               .polyline(frame_pts).close()
               .extrude(frame_width/2, both=True)
              )

# Apply fillets to smooth the outer shape
frame_solid = frame_solid.edges("|X").fillet(25)

# --- Web Recesses (I-Beam Effect) ---
# Define a smaller cutter profile to remove material from sides
cutter_pts = [
    (column_back_y + 15, base_height + 15),
    (column_back_y + 15, 180),
    (-60 + 15, frame_height + 20 - 15),
    (35 - 15, frame_height + 20 - 15),
    (35 - 15, 210 + 10),
    (-25 + 10, 140 + 5),
    (-35 + 10, base_height + 15)
]

# Create the cutter tool
pocket_depth = (frame_width - frame_web_thickness) / 2
cutter = (cq.Workplane("YZ")
          .polyline(cutter_pts).close()
          .extrude(pocket_depth)
          .edges("|X").fillet(15) # Round the corners of the pocket
         )

# Cut the pockets from both sides
frame_solid = frame_solid.cut(cutter.translate((frame_web_thickness/2, 0, 0)))
frame_solid = frame_solid.cut(cutter.translate((-frame_web_thickness/2 - pocket_depth, 0, 0)))

# --- 4. Head & Mechanism Housing ---
# Pinion Housing Cylinder
housing = (cq.Workplane("YZ")
           .moveTo(0, pinion_z)
           .circle(30)
           .extrude(frame_width + 12, both=True)
          )
frame_solid = frame_solid.union(housing)

# Pinion Shaft Bore
frame_solid = frame_solid.faces(">X").workplane().moveTo(0, pinion_z).circle(15).cutThruAll()

# Ram Guide (Square Hole)
frame_solid = (frame_solid.faces(">Z").workplane()
               .moveTo(0, 0)
               .rect(ram_size, ram_size)
               .cutBlind(-(frame_height - 100))
              )

# --- 5. Ram (Rack) ---
ram = (cq.Workplane("XY")
       .rect(ram_size, ram_size)
       .extrude(ram_length)
       .translate((0, 0, 90))
      )

# Cut Rack Teeth
# Create a series of cuts on the back face of the ram
tooth_cutter = (cq.Workplane("XY")
                .rect(ram_size + 5, 5) # Slightly wider than ram, 5mm high
                .extrude(4) # Depth of tooth
               )

for i in range(30):
    z_pos = 100 + i * 8
    # Position cutter on back face (Y negative)
    cut_op = tooth_cutter.rotate((0,0,0), (1,0,0), 90).translate((0, -ram_size/2, z_pos))
    ram = ram.cut(cut_op)

# --- 6. Handle Assembly ---
# Pinion Shaft Extension
shaft = (cq.Workplane("YZ")
         .workplane(offset=frame_width/2)
         .moveTo(0, pinion_z)
         .circle(14)
         .extrude(45)
        )

# Hub
hub_center_x = frame_width/2 + 45
hub = (cq.Workplane("YZ")
       .workplane(offset=hub_center_x - 10)
       .moveTo(0, pinion_z)
       .circle(20)
       .extrude(25)
      )

# Handle Rod (sliding through hub)
handle_rod = (cq.Workplane("XZ")
              .moveTo(hub_center_x + 12, pinion_z)
              .circle(handle_rod_diam/2)
              .extrude(handle_length, both=True)
             )

# Handle End Caps
cap1 = (cq.Workplane("XZ").workplane(offset=handle_length - 5)
        .moveTo(hub_center_x + 12, pinion_z).circle(10).extrude(15))
cap2 = (cq.Workplane("XZ").workplane(offset=-handle_length - 10)
        .moveTo(hub_center_x + 12, pinion_z).circle(10).extrude(15))

# --- Final Assembly ---
result = (base
          .union(frame_solid)
          .union(anvil)
          .union(ram)
          .union(shaft)
          .union(hub)
          .union(handle_rod)
          .union(cap1)
          .union(cap2)
         )