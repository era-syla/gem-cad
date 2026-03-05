import cadquery as cq

# --- Parametric Variables ---
# Main Plate
plate_length = 150.0
plate_width = 40.0
plate_thickness = 2.0

# Rails/Rods
rod_length = 160.0
rod_diameter = 2.0
rail_width = 3.0
rail_height = 3.0
rail_offset_z = -15.0  # Distance below the plate
rod_spacing_y = 6.0    # Spacing between the rods

# Wheel/Pulley
wheel_diameter = 25.0
wheel_thickness = 4.0
rim_width = 1.5
rim_depth = 1.0  # How deep the groove is (or how raised the rim is)
hub_diameter = 5.0
axle_hole_diameter = 2.0
wheel_z_offset = rail_offset_z - (wheel_diameter / 2) + 1.0 # Position relative to rails

# --- Geometry Construction ---

# 1. Top Plate
# Simple rectangular box
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Parallel Rails/Rods
# Looking at the image, there appears to be one square rail and two circular rods.
# Let's create the back rail (square profile)
back_rail = (cq.Workplane("XY")
             .workplane(offset=rail_offset_z)
             .moveTo(0, 10) # Offset in Y
             .box(rod_length, rail_width, rail_height)
             )

# Create the two front rods (circular profile)
# Rod 1
rod1 = (cq.Workplane("YZ")
        .workplane(offset=-rod_length/2)
        .moveTo(0, rail_offset_z) # Center Z
        .moveTo(0, 0) # Center Y relative to the wheel plane roughly
        .circle(rod_diameter/2)
        .extrude(rod_length)
        )

# Rod 2 (slightly offset)
rod2 = (cq.Workplane("YZ")
        .workplane(offset=-rod_length/2)
        .moveTo(0, rail_offset_z)
        .moveTo(-5, 0) # Offset in Y (local coordinates of YZ plane)
        .circle(rod_diameter/2)
        .extrude(rod_length)
        )
# Note: The coordinate system of the YZ plane needs careful handling. 
# Let's rebuild the rods on the global XY plane for clarity.

rod1 = (cq.Workplane("XY")
        .workplane(offset=rail_offset_z)
        .moveTo(0, -5) # Y offset
        .circle(rod_diameter/2)
        .extrude(rod_length)
        .translate((-rod_length/2, 0, 0)) # Center the extrusion
        .rotate((0,0,0), (0,1,0), 90) # Rotate to align with X axis
        )
# Actually, CadQuery extrude is normal to plane. 
# Let's stick to standard XY plane placement and translate.

# Re-doing rods for better alignment based on image visual:
# Rod 1 (middle)
rod_middle = (cq.Workplane("YZ")
              .workplane(offset=-rod_length/2)
              .moveTo(0, rail_offset_z) # Z height
              .circle(rod_diameter/2)
              .extrude(rod_length)
             )

# Rod 2 (front)
rod_front = (cq.Workplane("YZ")
              .workplane(offset=-rod_length/2)
              .moveTo(-5, rail_offset_z) # Y=-5, Z=rail_offset_z
              .circle(rod_diameter/2)
              .extrude(rod_length)
             )

# Rail (back)
rail_back = (cq.Workplane("XY")
             .workplane(offset=rail_offset_z - rail_height/2) # Align bottom
             .moveTo(0, 8) # Move back in Y
             .box(rod_length, rail_width, rail_height)
            )

# 3. The Wheel
# The wheel is vertical, oriented along the X-axis.
wheel = (cq.Workplane("XZ")
         .workplane(offset=0) # Centered in Y (or slightly offset if needed)
         .moveTo(0, rail_offset_z) # Center the wheel vertically near the rods
         .circle(wheel_diameter/2)
         .extrude(wheel_thickness)
         .translate((0, -wheel_thickness/2, 0)) # Center the thickness
         )

# Create the rim effect (cutout) on both sides
rim_cutout = (cq.Workplane("XZ")
              .workplane(offset=0)
              .moveTo(0, rail_offset_z)
              .circle((wheel_diameter/2) - rim_width)
              .extrude(wheel_thickness + 0.1) # Over-extrude for clean cut
              .translate((0, -wheel_thickness/2 - 0.05, 0))
              )

# Create the hub (add material back in center)
hub = (cq.Workplane("XZ")
       .workplane(offset=0)
       .moveTo(0, rail_offset_z)
       .circle(hub_diameter/2)
       .extrude(wheel_thickness)
       .translate((0, -wheel_thickness/2, 0))
       )

# Create the axle hole
axle_hole = (cq.Workplane("XZ")
             .workplane(offset=0)
             .moveTo(0, rail_offset_z)
             .circle(axle_hole_diameter/2)
             .extrude(wheel_thickness * 2)
             .translate((0, -wheel_thickness, 0))
             )

# Assemble the wheel components
final_wheel = wheel.cut(rim_cutout).union(hub).cut(axle_hole)

# 4. Small connector/axle support (the block behind the wheel)
axle_block = (cq.Workplane("XY")
              .workplane(offset=rail_offset_z)
              .moveTo(0, 2) # Slightly behind the wheel center
              .box(10, 4, 4)
              )

# --- Final Assembly ---
result = (plate
          .union(rod_middle)
          .union(rod_front)
          .union(rail_back)
          .union(final_wheel)
          .union(axle_block)
          )

# Rotate the whole result to match the isometric-like view of the image roughly
# (Optional, but helps verification)
# result = result.rotate((0,0,0), (0,0,1), -45) 