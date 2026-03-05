import cadquery as cq

# --- Parameters ---
# Base Plate
plate_length = 80.0
plate_width = 30.0
plate_thickness = 4.0

# Mounting Holes
hole_dia = 4.5
cbore_dia = 9.0
cbore_depth = 2.0
hole_spacing = 65.0  # Distance between hole centers

# Raised Housing (Main Body)
housing_length = 45.0
housing_width = 16.0
housing_height = 8.0  # Height above the plate surface
wall_thickness = 1.5
chamfer_size = 3.0    # Chamfer on the ends of the housing

# Internal Ribs
rib_thickness = 1.5

# --- Modeling ---

# 1. Base Plate
# Create the main rectangular base
result = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Mounting Holes
# Add counterbored holes on either end
result = (result
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .cboreHole(hole_dia, cbore_dia, cbore_depth)
)

# 3. Raised Housing Profile
# We need to sketch the outer shape of the housing. 
# It's a rectangle with chamfered corners at the ends.
# Since simple chamfering a rectangle might be tricky to align perfectly with the ribs later,
# sketching the profile is robust.

def housing_profile(length, width, chamfer):
    # Calculate key coordinates
    dx = length / 2
    dy = width / 2
    chamfer_x = dx - chamfer
    chamfer_y = dy - chamfer # This logic assumes 45 deg chamfer affecting width? 
                             # Actually, looking at the image, the chamfer cuts the corner off.
    
    # Let's create a rectangle and fillet/chamfer it in 2D
    s = (cq.Sketch()
         .rect(length, width)
         .vertices()
         .chamfer(chamfer)
    )
    return s

# Extrude the solid block for the housing first
housing_solid = (cq.Workplane("XY")
                 .workplane(offset=plate_thickness/2)
                 .placeSketch(housing_profile(housing_length, housing_width, chamfer_size))
                 .extrude(housing_height)
                )

# 4. Hollow out the Housing (Shelling)
# Instead of complex sketches, we can shell the solid from the top face
# Select the top face and shell inwards
housing_shelled = (housing_solid
                   .faces(">Z")
                   .shell(-wall_thickness)
                  )

# 5. Internal Ribs
# The image shows two transverse ribs dividing the space into three compartments.
# We'll create simple rectangular ribs that intersect the shelled housing.
rib_height = housing_height
# Distance of ribs from center. The center compartment looks roughly square-ish.
# Let's estimate the side compartments are smaller.
rib_offset = 8.0 

rib_1 = (cq.Workplane("XY")
         .workplane(offset=plate_thickness/2 + rib_height/2)
         .center(-rib_offset, 0)
         .box(rib_thickness, housing_width, rib_height) # Width is oversized to ensure intersection
        )

rib_2 = (cq.Workplane("XY")
         .workplane(offset=plate_thickness/2 + rib_height/2)
         .center(rib_offset, 0)
         .box(rib_thickness, housing_width, rib_height)
        )

# 6. Combine Everything
# Union the base plate, the shelled housing, and the ribs.
# Note: The shelling operation creates a new solid. 
# We need to ensure the ribs don't protrude outside the housing.
# The easiest way is to intersect the ribs with the *original unshelled* solid shape, 
# then union that with the shelled shape. Or just size them carefully.
# Given the chamfer shape, a simple box for the rib might poke out if the chamfer is large.
# Let's use intersection for robustness.

ribs_combined = rib_1.union(rib_2)
# Clip ribs to the outer bounds of the housing (using the solid block from step 3)
ribs_clipped = housing_solid.intersect(ribs_combined)

result = result.union(housing_shelled).union(ribs_clipped)

# Optional: Add small fillets to the base of the housing for realism/strength (often seen in molded parts)
# result = result.faces("|Z").edges().fillet(0.5) 

# Export/Render
if 'show_object' in globals():
    show_object(result)