import cadquery as cq

# --- Parametric Dimensions ---
total_length = 40.0
width = 14.0
body_height = 16.0
flange_height = 6.0
flange_length = 15.0
body_length = total_length - flange_length
fillet_radius = 8.5  # Controls the slope curve

hole_upper_dia = 5.0
hole_upper_z = 11.5
hole_lower_dia = 3.5
hole_lower_z = 5.0

slit_z = 5.0
slit_thickness = 0.6
slit_depth = body_length - 4.0

cutout_width = 5.0
cutout_height = 8.0

text_size = 10.0
text_depth = 0.5
gap_between_parts = 4.0

# --- Helper Function for Base Geometry ---
def make_base_geometry():
    """Creates the generic geometry for the right side (+X) part."""
    
    # 1. Create Main Body
    # Origin is at the inner mating face (X=0)
    body = cq.Workplane("XY").box(body_length, width, body_height, centered=(False, True, False))
    
    # 2. Create Flange
    flange = (cq.Workplane("XY")
              .workplane(offset=0)
              .center(body_length + flange_length/2, 0)
              .box(flange_length, width, flange_height, centered=(True, True, False))
             )
    
    part = body.union(flange)
    
    # 3. Fillet the transition from body to flange
    # Select the top edge at the end of the body block
    try:
        part = part.edges(cq.selectors.NearestToPointSelector((body_length, 0, body_height))).fillet(fillet_radius)
    except ValueError:
        pass # Handle cases where radius might be too large for exact geometry
        
    # 4. Create Bottom Cutout (Inner hook/clamp area)
    part = (part.faces("<Z").workplane(centerOption="ProjectedOrigin")
            .center(cutout_width/2, 0)
            .rect(cutout_width, width)
            .cutBlind(cutout_height)
           )
           
    # 5. Create Rod/Screw Holes on the Front Face
    # Drilling through the width (Y-axis)
    part = (part.faces("<Y").workplane(centerOption="ProjectedOrigin")
            .moveTo(body_length/2, hole_upper_z).circle(hole_upper_dia/2).cutBlind(width)
            .moveTo(body_length/2, hole_lower_z).circle(hole_lower_dia/2).cutBlind(width)
           )
           
    # 6. Create the Slit (Flexure cut)
    part = (part.faces("<Y").workplane(centerOption="ProjectedOrigin")
            .moveTo(slit_depth/2, slit_z)
            .rect(slit_depth, slit_thickness)
            .cutBlind(width)
           )
           
    # 7. Create Countersunk Mounting Hole on Flange
    part = (part.faces(">Z").workplane(centerOption="ProjectedOrigin")
            .moveTo(body_length + flange_length/2, 0)
            .cskHole(3.5, 7.0, 82)
           )
           
    # 8. Create Small Alignment Tab on Front Face
    tab_size = 1.5
    part = (part.faces("<Y").workplane(centerOption="ProjectedOrigin")
            .moveTo(tab_size/2, slit_z)
            .rect(tab_size, tab_size)
            .extrude(0.8)
           )
           
    return part

# --- Build Assembly ---

# 1. Generate Base Geometry
base_geo = make_base_geometry()

# 2. Create Right Part ('R')
# Add text to the generic base
part_R = (base_geo.faces(">Z").workplane(centerOption="ProjectedOrigin")
          .moveTo(body_length/2 - 1, 0) # Slightly offset center due to fillet
          .text("R", text_size, -text_depth)
         )
part_R = part_R.translate((gap_between_parts/2, 0, 0))

# 3. Create Left Part ('L')
# Mirror the generic base first
part_L_base = base_geo.mirror("YZ")

# Add text to the mirrored part
# Note: Coordinate system logic for text placement on mirrored part
part_L = (part_L_base.faces(">Z").workplane(centerOption="ProjectedOrigin")
          .moveTo(-body_length/2 + 1, 0)
          .text("L", text_size, -text_depth)
         )
part_L = part_L.translate((-gap_between_parts/2, 0, 0))

# 4. Combine into final result
result = part_R.union(part_L)

# If running in CQ-Editor, this line displays the model
# show_object(result)