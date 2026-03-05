import cadquery as cq
import math

thk = 5
ring_inner = 25
ring_outer = 30
arm_len = 40
arm_w = 8
block_out_len = 10
block_in_len = 8
pad_w = 4
pad_l = 4
pad_h = 3
inner_block_offset = 10

angles = [90, 210, 330]

# Base ring
result = (
    cq.Workplane("XY")
      .circle(ring_outer)
      .circle(ring_inner)
      .extrude(thk)
)

# Arms, blocks, and pads
for angle in angles:
    a = math.radians(angle)
    # Arm
    arm = (
        cq.Workplane("XY")
          .rect(arm_len, arm_w)
          .extrude(thk)
          .rotate((0,0,0),(0,0,1), angle)
          .translate((math.cos(a)*(ring_inner+arm_len/2),
                      math.sin(a)*(ring_inner+arm_len/2), 0))
    )
    result = result.union(arm)
    # Outer block
    bx = math.cos(a)*(ring_inner + arm_len + block_out_len/2)
    by = math.sin(a)*(ring_inner + arm_len + block_out_len/2)
    block_out = (
        cq.Workplane("XY")
          .box(arm_w, block_out_len, thk)
          .rotate((0,0,0),(0,0,1), angle)
          .translate((bx, by, thk/2))
    )
    result = result.union(block_out)
    pad_out = (
        cq.Workplane("XY")
          .box(pad_w, pad_l, pad_h)
          .translate((bx, by, thk + pad_h/2))
    )
    result = result.union(pad_out)
    # Inner block
    bi = ring_inner - inner_block_offset
    bxi = math.cos(a)*bi
    byi = math.sin(a)*bi
    block_in = (
        cq.Workplane("XY")
          .box(arm_w, block_in_len, thk)
          .rotate((0,0,0),(0,0,1), angle)
          .translate((bxi, byi, thk/2))
    )
    result = result.union(block_in)
    pad_in = (
        cq.Workplane("XY")
          .box(pad_w, pad_l, pad_h)
          .translate((bxi, byi, thk + pad_h/2))
    )
    result = result.union(pad_in)

# Engrave "N" on the arm at 330°
text_angle = 330
a = math.radians(text_angle)
px = math.cos(a)*(ring_inner + arm_len/2)
py = math.sin(a)*(ring_inner + arm_len/2)
result = (
    result.faces(">Z")
          .workplane()
          .transformed(offset=(px, py, 0), rotate=(0, 0, text_angle))
          .text("N", 5, 1, cut=True)
)