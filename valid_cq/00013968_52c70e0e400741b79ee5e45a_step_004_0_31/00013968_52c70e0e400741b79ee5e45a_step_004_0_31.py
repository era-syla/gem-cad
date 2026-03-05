import cadquery as cq

# --- Parameters ---
text_string = "IBM"
font_size = 50.0
model_thickness = 5.0

# The classic logo has 8 horizontal solid bars separated by 7 gaps
number_of_bars = 8

# Ratio of the height of a solid bar to the height of a gap
# Adjusted to visually match the standard proportions
bar_to_gap_ratio = 1.6 

# --- Base Text Generation ---
# Using a bold serif font to best approximate the classic slab-serif look
base_text = cq.Workplane("XY").text(
    text_string,
    font_size,
    model_thickness,
    font="Times New Roman",
    kind="bold",
    halign="center",
    valign="center"
)

# --- Geometry Calculations ---
# Extract bounding box to perfectly fit the gaps over the generated text
bbox = base_text.val().BoundingBox()
ymin = bbox.ymin
ymax = bbox.ymax
xmin = bbox.xmin
xmax = bbox.xmax

total_height = ymax - ymin
total_width = xmax - xmin
x_center = (xmin + xmax) / 2.0

number_of_gaps = number_of_bars - 1

# Calculate the precise height of the gaps and bars
gap_height = total_height / (number_of_bars * bar_to_gap_ratio + number_of_gaps)
bar_height = gap_height * bar_to_gap_ratio

# --- Create Cutting Tool ---
# Compute the center coordinate for each horizontal gap
gap_centers = []
for i in range(number_of_gaps):
    y_center = ymin + bar_height + (gap_height / 2.0) + i * (bar_height + gap_height)
    gap_centers.append((x_center, y_center))

# Generate the intersecting tool body by extruding rectangles at each gap center
# Z is offset negatively and extruded beyond thickness to guarantee clean Boolean cuts
cutting_tool = (
    cq.Workplane("XY")
    .workplane(offset=-2.0)
    .pushPoints(gap_centers)
    .rect(total_width + 20.0, gap_height)
    .extrude(model_thickness + 4.0)
)

# --- Final Boolean Operation ---
# Subtract the gaps from the base text to form the 8-bar logo
result = base_text.cut(cutting_tool)