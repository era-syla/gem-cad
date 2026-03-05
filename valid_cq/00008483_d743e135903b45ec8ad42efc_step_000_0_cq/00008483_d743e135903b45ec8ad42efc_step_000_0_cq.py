import cadquery as cq

# Parametric dimensions
base_diameter = 50.0       # Diameter of the large bottom disc
base_thickness = 5.0       # Thickness of the large bottom disc
taper_base_diameter = 35.0 # Diameter where the taper starts on the base
taper_top_diameter = 18.0  # Diameter of the tapered section at the top (slightly wider than the cylinder)
taper_height = 8.0         # Height of the conical/tapered section
cylinder_diameter = 15.0   # Diameter of the top vertical cylinder
cylinder_height = 15.0     # Height of the top cylinder extending from the taper

# Step 1: Create the base disc
# We start by drawing a circle on the XY plane and extruding it
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_thickness)

# Step 2: Create the tapered transition section
# We create a new workplane on top of the base
# To create a taper (cone), we sketch the base circle and extrude with a taper angle,
# or simply loft two circles. Here, lofting is safer for explicit dimension control.
taper_start_plane = base.faces(">Z").workplane()
taper = (taper_start_plane
         .circle(taper_base_diameter / 2)
         .workplane(offset=taper_height)
         .circle(taper_top_diameter / 2)
         .loft(combine=True))

# Step 3: Create the top cylinder
# We select the top face of the newly created geometry
top_cylinder = (taper.faces(">Z").workplane()
                .circle(cylinder_diameter / 2)
                .extrude(cylinder_height))

# Combine everything into the final result
result = top_cylinder

# Note: The provided image shows a small flat step or collar between the taper 
# and the vertical cylinder. The dimensions above create a slight shelf 
# (taper_top_diameter > cylinder_diameter) to replicate this visual feature.