import cadquery as cq

# Parameters for the geometry
hex_circumdiameter = 100.0  # Diameter across the corners of the hexagon
plate_thickness = 5.0       # Thickness of the plate
center_hole_diameter = 15.0 # Diameter of the central hole
slot_length = 30.0          # Total length of the radial slots
slot_width = 6.0            # Width of the radial slots
slot_offset_radius = 28.0   # Distance from plate center to slot center

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Create the base hexagonal prism
    .polygon(6, hex_circumdiameter)
    .extrude(plate_thickness)
    
    # Cut the central circular hole
    .faces(">Z").workplane()
    .circle(center_hole_diameter / 2.0)
    .cutThruAll()
    
    # Cut the radial slots using a polar array
    .faces(">Z").workplane()
    .polarArray(slot_offset_radius, 0, 360, 6)
    .slot2D(slot_length, slot_width, 0) # 0 angle aligns with radial direction in polar array
    .cutThruAll()
)