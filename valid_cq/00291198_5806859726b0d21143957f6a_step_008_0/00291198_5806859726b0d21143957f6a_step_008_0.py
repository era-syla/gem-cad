import cadquery as cq

# --- Parameters ---
# Rod dimensions
rod_length = 200.0
rod_diameter = 5.0

# Housing (the eye/head) dimensions
housing_radius = 9.0  # Radius of the spherical outer profile
housing_height = 13.0 # Height of the flattened sphere

# Stud/Ball joint dimensions
stud_diameter = 8.0     # Diameter of the pin passing through
stud_post_diameter = 7.0 # Diameter of the bottom threaded section
stud_post_length = 12.0  # Length of the bottom section
head_diameter = 13.0    # Top cap diameter
head_height = 2.5       # Top cap thickness
slot_width = 1.8
slot_depth = 1.2

# Connection dimensions
flange_diameter = 9.5
flange_thickness = 2.5
neck_length = 6.0       # Length of transition from housing to flange
neck_start_radius = 4.5 # Radius at housing side
neck_end_radius = 3.5   # Radius at flange side

# --- Modeling ---

# 1. Create the Housing (Rod End Eye)
# Modeled as a sphere with top and bottom cut off to form the ring shape
housing = (cq.Workplane("XY")
           .sphere(housing_radius)
           .cut(cq.Workplane("XY").workplane(offset=housing_height/2).rect(50, 50).extrude(50))
           .cut(cq.Workplane("XY").workplane(offset=-housing_height/2).rect(50, 50).extrude(-50))
           )

# 2. Create the Stud Assembly
# The central pin
stud_body = (cq.Workplane("XY")
             .circle(stud_diameter/2)
             .extrude(housing_height/2)
             .mirror("XY", union=True))

# The bottom post
stud_post = (cq.Workplane("XY")
             .workplane(offset=-housing_height/2)
             .circle(stud_post_diameter/2)
             .extrude(-stud_post_length))

# The top head
stud_head = (cq.Workplane("XY")
             .workplane(offset=housing_height/2)
             .circle(head_diameter/2)
             .extrude(head_height))

# The screw slot cut
slot_cut = (cq.Workplane("XY")
            .workplane(offset=housing_height/2 + head_height)
            .rect(head_diameter + 2, slot_width)
            .extrude(-slot_depth))

# Combine stud parts
stud = stud_body.union(stud_post).union(stud_head).cut(slot_cut)

# 3. Create the Rod Connection (Neck, Flange, Rod)
# We build this along the X-axis (YZ plane)
# Start slightly inside the housing to ensuring overlapping geometry for union
start_offset = housing_radius * 0.7 

# Neck: Lofted transition from housing to flange
neck = (cq.Workplane("YZ")
        .workplane(offset=start_offset)
        .circle(neck_start_radius)
        .workplane(offset=neck_length)
        .circle(neck_end_radius)
        .loft(combine=True))

# Flange: Washer-like feature
flange_pos = start_offset + neck_length
flange = (cq.Workplane("YZ")
          .workplane(offset=flange_pos)
          .circle(flange_diameter/2)
          .extrude(flange_thickness))

# Main Rod: Long cylinder
rod_pos = flange_pos + flange_thickness
rod = (cq.Workplane("YZ")
       .workplane(offset=rod_pos)
       .circle(rod_diameter/2)
       .extrude(rod_length))

# --- Final Assembly ---
result = housing.union(stud).union(neck).union(flange).union(rod)