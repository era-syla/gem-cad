import cadquery as cq

# --- Parameters ---

# Inner Spike Assembly
spike_tip_z = 50.0
spike_belly_r = 9.0
spike_belly_z = 32.0
needle_r = 1.0
needle_top_z = 5.0
needle_bot_z = -40.0
base_r = 9.0
base_height = 2.0
finial_z = -46.0

# Outer Housing
housing_bot_z = 10.0
housing_cyl_r = 28.0
housing_rim_step_z = 38.0
housing_rim_r = 34.0
housing_top_z = 45.0
housing_throat_r = 14.0
housing_bot_inner_r = 18.0

# --- Modeling ---

# 1. Create the Central Spike/Needle Assembly
# Defined as a profile in the XZ plane revolved around Z
inner_profile = (
    cq.Workplane("XZ")
    .moveTo(0, spike_tip_z)  # Start at top tip
    .spline(
        [(spike_belly_r, spike_belly_z), (needle_r, needle_top_z)],
        includeCurrent=True
    )  # Curve for the ogive
    .lineTo(needle_r, needle_bot_z)  # Straight needle shaft
    .lineTo(base_r, needle_bot_z)    # Base top face
    .lineTo(base_r, needle_bot_z - base_height) # Base side
    .spline(
        [(base_r * 0.4, needle_bot_z - base_height - 2), (0, finial_z)],
        includeCurrent=True
    ) # Decorative bottom finial
    .close() # Close back to (0, spike_tip_z) along the axis
)

inner_solid = inner_profile.revolve()

# 2. Create the Outer Housing
# Defined as a separate profile in the XZ plane
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(housing_bot_inner_r, housing_bot_z) # Start bottom inner
    .spline(
        [(housing_throat_r, (housing_bot_z + housing_top_z) / 2), 
         (housing_throat_r + 6, housing_top_z)], 
        includeCurrent=True
    ) # Inner converging-diverging curve
    .spline(
        [(housing_rim_r - 2, housing_top_z + 2), (housing_rim_r, housing_top_z - 1)],
        includeCurrent=True
    ) # Top rounded rim
    .lineTo(housing_rim_r, housing_rim_step_z) # Rim vertical side
    .lineTo(housing_cyl_r, housing_rim_step_z) # Step in
    .lineTo(housing_cyl_r, housing_bot_z)      # Main cylinder side
    .close() # Close bottom face
)

outer_solid = outer_profile.revolve()

# Combine the two solids into the final result
result = inner_solid.union(outer_solid)

# Export or display (for verifying in a script runner)
# if 'show_object' in globals():
#     show_object(result)