import cadquery as cq

# Parametric dimensions
box_width = 30.0    # Width of the rectangular base
box_depth = 50.0    # Length/Depth of the rectangular base
box_height = 40.0   # Height of the rectangular base

stem_diameter = 10.0 # Diameter of the small connecting cylinder
stem_length = 5.0    # Length of the small connecting cylinder

head_diameter = 20.0 # Diameter of the large outer disc/cylinder
head_thickness = 5.0 # Thickness of the large outer disc/cylinder

# Create the main rectangular body
# We center it on X and Y, sitting on Z=0 for convenience, or centered on all axes.
# Let's center it on all axes to make attaching the protrusion easier.
main_body = cq.Workplane("XY").box(box_width, box_depth, box_height)

# Create the protrusion
# We want to attach it to one of the faces. Based on the image, it's on a side face.
# Let's pick the face in the negative Y direction (front face in standard view).
# We attach a workplane to that face.
protrusion = (
    main_body.faces("<Y").workplane()
    # First, the smaller stem
    .circle(stem_diameter / 2)
    .extrude(stem_length)
    # Select the new face at the end of the stem
    .faces(">Y").workplane()
    # Then, the larger head
    .circle(head_diameter / 2)
    .extrude(head_thickness)
)

result = protrusion