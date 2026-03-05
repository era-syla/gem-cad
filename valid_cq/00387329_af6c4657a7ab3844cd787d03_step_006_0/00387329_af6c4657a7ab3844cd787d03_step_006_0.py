import cadquery as cq

# ==============================================================================
# Parametric Dimensions
# ==============================================================================
# Main Tube (SHS)
tube_size = 40.0
tube_height = 250.0
tube_wall = 3.0

# Tongue Plate (welded/attached to tube)
tongue_width = 90.0
tongue_height = 160.0
tongue_thick = 8.0

# Base Plate
base_width = 140.0
base_height = 140.0
base_thick = 10.0

# Accessory Plates
acc_plate_w = 80.0
acc_plate_h = 35.0
acc_plate_th = 6.0

# Feature Sizes
slot_len = 35.0
slot_width = 8.0
hole_dia = 6.0

# ==============================================================================
# Component 1: Main Column Assembly
# ==============================================================================

# 1. Vertical Tube
tube = (cq.Workplane("XY")
        .rect(tube_size, tube_size)
        .extrude(tube_height)
        .faces(">Z").shell(-tube_wall)
        .translate((0, 0, 100))  # Lift up to allow tongue insertion
       )

# 2. Connection Block (visual transition between tube and plate)
connector = (cq.Workplane("XY")
             .rect(tube_size, tube_size)
             .extrude(20)
             .translate((0, 0, 100))
            )

# 3. Tongue Plate
tongue = (cq.Workplane("XY")
          .box(tongue_width, tongue_thick, tongue_height)
          .translate((0, 0, tongue_height / 2))
         )

# Add 3 Vertical Slots to the lower part of the tongue
tongue = (tongue.faces(">Y").workplane()
          .pushPoints([(-25, -30), (0, -30), (25, -30)])
          .slot2D(slot_len, slot_width, 90)  # 90 degrees = vertical
          .cutThruAll()
         )

# Add 4 mounting holes to the upper part of the tongue
tongue = (tongue.faces(">Y").workplane()
          .pushPoints([(-30, 50), (-10, 50), (10, 50), (30, 50)])
          .circle(hole_dia / 2)
          .cutThruAll()
         )

# Combine into main assembly
main_assembly = tube.union(connector).union(tongue)


# ==============================================================================
# Component 2: Base Plate
# ==============================================================================
base_plate = (cq.Workplane("XY")
              .box(base_width, base_thick, base_height)
              .translate((0, 0, -base_height / 2 - 20))  # Position below the tongue
             )

# Row of adjustment holes at the top
base_plate = (base_plate.faces(">Y").workplane()
              .pushPoints([(x, base_height / 2 - 15) for x in range(-50, 51, 15)])
              .circle(hole_dia / 2)
              .cutThruAll()
             )

# Mounting holes at the 4 corners
base_plate = (base_plate.faces(">Y").workplane()
              .rect(base_width - 30, base_height - 30, forConstruction=True)
              .vertices()
              .circle(4.0)
              .cutThruAll()
             )


# ==============================================================================
# Component 3: Side Plate (Horizontal Slots)
# ==============================================================================
slot_plate = (cq.Workplane("XZ")
              .box(acc_plate_w, acc_plate_th, acc_plate_h)
             )

# Two horizontal slots
slot_plate = (slot_plate.faces(">Y").workplane()
              .pushPoints([(10, 8), (10, -8)])
              .slot2D(30, 5, 0)  # 0 degrees = horizontal
              .cutThruAll()
             )

# Two circular holes
slot_plate = (slot_plate.faces(">Y").workplane()
              .pushPoints([(-25, 8), (-25, -8)])
              .circle(3.0)
              .cutThruAll()
             )

# Position relative to main assembly (Exploded view)
slot_plate_final = slot_plate.translate((-80, -20, 60))


# ==============================================================================
# Component 4: Side Plate (Hole Pattern)
# ==============================================================================
hole_plate = (cq.Workplane("XZ")
              .box(acc_plate_w, acc_plate_th, acc_plate_h)
             )

# 2x3 Grid of holes
hole_plate = (hole_plate.faces(">Y").workplane()
              .rarray(15, 12, 3, 2)
              .circle(3.0)
              .cutThruAll()
             )

# Position relative to main assembly
hole_plate_final = hole_plate.translate((-60, 20, 120))


# ==============================================================================
# Component 5: Pin
# ==============================================================================
pin = (cq.Workplane("YZ")
       .circle(5)
       .extrude(30)
       .translate((-80, -30, 30))
      )


# ==============================================================================
# Final Assembly
# ==============================================================================
result = (main_assembly
          .union(base_plate)
          .union(slot_plate_final)
          .union(hole_plate_final)
          .union(pin)
         )