import cadquery as cq

# Build a stepped pyramid / pedestal with ogee-style base molding

# Dimensions
base_w = 100
base_h = 4

step1_w = 84
step1_h = 8

ogee_w = 76
ogee_h = 12

step2_w = 60
step2_h = 8

step3_w = 44
step3_h = 8

top_w = 32
top_h = 6

# Start building from bottom up
result = cq.Workplane("XY")

# Layer 1: flat base slab
result = result.box(base_w, base_w, base_h, centered=(True, True, False))

# Layer 2: first step
result = result.faces(">Z").workplane()
result = result.rect(step1_w, step1_w).extrude(step1_h)

# Layer 3: ogee/molding section - simulate with a swept profile
# We'll approximate the ogee with two extrude steps
# Bottom of ogee - slightly smaller, taller
result = result.faces(">Z").workplane()
result = result.rect(ogee_w, ogee_w).extrude(ogee_h * 0.4)

# Middle of ogee - bulge out slightly
result = result.faces(">Z").workplane()
result = result.rect(ogee_w + 4, ogee_w + 4).extrude(ogee_h * 0.2)

# Top of ogee - taper back in
result = result.faces(">Z").workplane()
result = result.rect(ogee_w, ogee_w).extrude(ogee_h * 0.4)

# Layer 4: second step
result = result.faces(">Z").workplane()
result = result.rect(step2_w, step2_w).extrude(step2_h)

# Layer 5: third step
result = result.faces(">Z").workplane()
result = result.rect(step3_w, step3_w).extrude(step3_h)

# Layer 6: top cap
result = result.faces(">Z").workplane()
result = result.rect(top_w, top_w).extrude(top_h)

# Add fillets to soften the ogee area edges
# Select edges on the bulge layer
result = (
    cq.Workplane("XY")
    .box(base_w, base_w, base_h, centered=(True, True, False))
    .faces(">Z").workplane()
    .rect(step1_w, step1_w).extrude(step1_h)
    .faces(">Z").workplane()
    .rect(ogee_w, ogee_w).extrude(ogee_h * 0.4)
    .faces(">Z").workplane()
    .rect(ogee_w + 4, ogee_w + 4).extrude(ogee_h * 0.2)
    .faces(">Z").workplane()
    .rect(ogee_w, ogee_w).extrude(ogee_h * 0.4)
    .faces(">Z").workplane()
    .rect(step2_w, step2_w).extrude(step2_h)
    .faces(">Z").workplane()
    .rect(step3_w, step3_w).extrude(step3_h)
    .faces(">Z").workplane()
    .rect(top_w, top_w).extrude(top_h)
)

result = result