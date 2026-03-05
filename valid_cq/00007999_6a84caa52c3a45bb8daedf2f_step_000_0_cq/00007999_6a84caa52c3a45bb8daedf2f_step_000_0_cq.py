import cadquery as cq

# --- Parameters ---
# Overall dimensions
total_length = 1000.0  # Total length of the assembly
black_section_length = 200.0  # Length of the black section (handle/grip?)
profile_size = 30.0    # Width and height of the square profile
wall_thickness = 2.0   # Thickness of the tube walls

# Derived dimensions
grey_section_length = total_length - black_section_length

# --- Modeling ---

# Create the main profile sketch for the tube
# We'll create a single hollow tube first, or two separate joined tubes.
# Given the color difference, it might be modeled as two parts, but for a single 'result' variable,
# a Union is appropriate. Or perhaps it's a single tube painted differently. 
# Let's model it as a single continuous square tube for simplicity, as physically it looks like one piece.
# However, to represent the visual distinction, we could model two butt-joined tubes.

# Method 1: Single continuous tube (geometry-wise)
# sketch = (
#     cq.Sketch()
#     .rect(profile_size, profile_size)
#     .rect(profile_size - 2*wall_thickness, profile_size - 2*wall_thickness, mode='s')
# )
# tube = cq.Workplane("XY").placeSketch(sketch).extrude(total_length)


# Method 2: Two separate sections unioned together. This is better for parametric control if they were different sizes.
# Here they look identical in profile. Let's stick to a single tube geometry as it's the most robust interpretation of a structural beam.
# To make it interesting and robust, let's ensure it's hollow.

def create_square_tube(length, width, thickness):
    """Helper to create a square tube."""
    return (
        cq.Workplane("XY")
        .rect(width, width)
        .rect(width - 2*thickness, width - 2*thickness)
        .extrude(length)
    )

# Since the prompt asks for a single result object and the image shows a single linear element
# with two colors (which CadQuery code doesn't strictly render, but we can model the geometry),
# I will model the entire length as one solid hollow tube.
# The visual distinction suggests a "handle" or a painted end.

# Let's create the geometry.
# Center the cross-section on the Z-axis for cleaner code.

# 1. Create the outer profile
outer_rect = cq.Workplane("XY").rect(profile_size, profile_size)

# 2. Create the inner profile for subtraction
inner_rect = cq.Workplane("XY").rect(profile_size - 2*wall_thickness, profile_size - 2*wall_thickness)

# 3. Extrude the main tube
# We will extrude the outer shape and then cut the inner shape.
main_body = (
    cq.Workplane("XY")
    .rect(profile_size, profile_size)
    .extrude(total_length)
)

cutout = (
    cq.Workplane("XY")
    .rect(profile_size - 2*wall_thickness, profile_size - 2*wall_thickness)
    .extrude(total_length)
)

result = main_body.cut(cutout)

# Note on the image: The black part looks like a solid plug or a handle grip slid over the tube,
# but upon closer inspection of the far right end, it's clearly a hollow tube.
# The black part on the left seems to have the same outer dimension.
# Therefore, a single continuous hollow tube is the most accurate geometric representation.
# The color difference is a rendering attribute, not geometry.

# However, to be precise about the "black part" possibly being a separate component (like an insert or grip),
# if we assume it's just a tube, the code above is sufficient.
# If we assume the black part is a slightly larger sleeve, the image doesn't show a step in diameter.
# So, simple tube is best.

# Final check of the generated code logic.
# Creating a Workplane, drawing the outer rectangle, drawing the inner rectangle in subtraction mode, then extruding.
# This is the most "CadQuery" idiomatic way.

result = (
    cq.Workplane("XY")
    .rect(profile_size, profile_size)
    .rect(profile_size - 2*wall_thickness, profile_size - 2*wall_thickness) # Subtract inner rect
    .extrude(total_length)
)