import cadquery as cq

# --- Parameters ---
hex_radius = 130.0
plate_thickness = 4.0
tri_side = 90.0
tall_ext_height = 600.0
short_ext_height = 350.0
rail_height = 500.0
rod_height = 520.0

# --- Helper Functions ---

def create_2060_profile(length):
    """Creates a simplified 20x60mm V-slot extrusion."""
    w, h = 20, 60
    # Base block
    prof = cq.Workplane("XY").rect(w, h).extrude(length)
    # Chamfer edges for visual effect
    prof = prof.edges("|Z").chamfer(1.0)
    # Cut simplified grooves
    groove_w = 6
    groove_d = 5
    
    # Create a cutter for the grooves
    cutter = cq.Workplane("XY").rect(groove_w, groove_d).extrude(length)
    
    # Face cuts (front and back)
    for y_offset in [-20, 0, 20]:
        prof = prof.cut(cutter.translate((w/2, y_offset, 0)))
        prof = prof.cut(cutter.translate((-w/2, y_offset, 0)))
    
    # Side cuts
    side_cutter = cq.Workplane("XY").rect(groove_d, groove_w).extrude(length)
    prof = prof.cut(side_cutter.translate((0, h/2, 0)))
    prof = prof.cut(side_cutter.translate((0, -h/2, 0)))
    
    return prof

def create_triangular_profile(length):
    """Creates a simplified triangular extrusion (Delta tower style)."""
    s = 50.0 # Side length
    
    # Base triangle with rounded corners
    prof = (cq.Workplane("XY")
            .polygon(3, s)
            .extrude(length)
            .edges("|Z").fillet(4.0))
    
    # Central hole
    prof = prof.cut(cq.Workplane("XY").circle(8).extrude(length))
    
    # Grooves on the three faces
    # Since specific geometry is complex, we'll cut a slot on one face and rotate/copy or just leave as prism
    # for this visual approximation, the prism with fillet is sufficient.
    
    return prof

def create_linear_rail(length):
    """Creates a simplified linear guide rail."""
    w, t = 12.0, 8.0
    rail = cq.Workplane("XY").rect(w, t).extrude(length)
    
    # Add mounting holes
    holes = (cq.Workplane("XY")
             .rarray(1, 25, 1, int(length/25))
             .circle(1.75)
             .extrude(length)) # Extrude cylinder to cut
    
    # Orient properly to cut through Y (thickness)
    # Easier: Make holes on the face
    rail = rail.faces(">Y").workplane().rarray(1, 25, 1, int(length/25)).circle(1.75).cutThruAll()
    
    return rail

# --- Part Creation & Positioning ---

# 1. Hexagonal Base Plate (Heated Bed)
hex_plate = (cq.Workplane("XY")
             .polygon(6, hex_radius * 2) # polygon takes diameter
             .extrude(plate_thickness)
             .translate((-180, -100, 0)))

# 2. Triangular Plate 1 (Lower)
tri_plate_1 = (cq.Workplane("XY")
               .polygon(3, tri_side)
               .extrude(plate_thickness)
               .translate((-60, -40, 0)))

# 3. Triangular Plate 2 (Upper / Floating)
tri_plate_2 = (cq.Workplane("XY")
               .polygon(3, tri_side)
               .extrude(plate_thickness)
               .translate((60, 60, 250))) # Positioned up high

# 4. Tall Central Extrusion (Triangular)
tall_extrusion = (create_triangular_profile(tall_ext_height)
                  .translate((60, 60, 30))) # Sits on base block

# 5. Base Mount Block (Delta Vertex)
base_vertex = (cq.Workplane("XY")
               .polygon(3, 80)
               .extrude(30)
               .edges("|Z").fillet(8)
               .faces(">Z").workplane()
               .polygon(3, 55).cutBlind(-15) # Socket for extrusion
               .translate((60, 60, 0)))

# 6. Left Wide Extrusion
left_ext = (create_2060_profile(short_ext_height)
            .translate((10, 60, 0)))

# 7. Right Wide Extrusion
right_ext = (create_2060_profile(short_ext_height)
             .translate((110, 60, 0)))

# 8. Linear Rail
rail = (create_linear_rail(rail_height)
        .rotate((0,0,0), (1,0,0), 90) # Stand upright
        .translate((60, 40, 30))) # In front of tall extrusion

# 9. Linear Rod
rod = (cq.Workplane("XY")
       .circle(3)
       .extrude(rod_height)
       .translate((85, 80, 0)))

# 10. Carriage Block (on Rail)
carriage = (cq.Workplane("XY")
            .rect(20, 20)
            .extrude(10)
            .edges("|Z").fillet(2)
            .rotate((0,0,0), (1,0,0), 90) # Match rail orientation
            .translate((60, 36, 150)))

# 11. Small Hardware (Screw)
screw = (cq.Workplane("XY")
         .circle(2.5).extrude(15)
         .faces(">Z").workplane().circle(4.5).extrude(3) # Head
         .rotate((1,0,0), (0,0,0), 90) # Lay flat
         .translate((40, 0, 2)))

# 12. Small Square Chip/Plate
small_chip = (cq.Workplane("XY")
              .rect(15, 15).extrude(2)
              .translate((90, -10, 0)))

# --- Assembly ---

result = (hex_plate
          .add(tri_plate_1)
          .add(tri_plate_2)
          .add(base_vertex)
          .add(tall_extrusion)
          .add(left_ext)
          .add(right_ext)
          .add(rail)
          .add(rod)
          .add(carriage)
          .add(screw)
          .add(small_chip)
          )