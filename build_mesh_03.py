import cadquery as cq
import math

# ==================== 参数化设计变量 (单位: mm) ====================
BASE_DIAMETER = 70.0          # 底部圆柱初始直径 (7cm)
BASE_HEIGHT = 2.0             # 底部圆柱高度 (2mm)
HOLE_DIAMETER = 35.0          # 中心孔直径 (3.5cm)
WALL_THICKNESS = 2.0          # 封闭墙与锥形顶厚度 (2mm)
WALL_HEIGHT = 80.0            # 封闭墙高度 (8cm)
CAP_HEIGHT = 15.0             # 锥形封顶高度 (自定义参数)
PERFORATION_DIAMETER = 2.0    # 滤网网孔直径 (2mm)
HOLE_SPACING = 4.0            # 孔两两间圆心距离 (4mm)

# 计算衍生半径
r_in = HOLE_DIAMETER / 2.0
r_out = r_in + WALL_THICKNESS
r_base = BASE_DIAMETER / 2.0
r_mid = (r_in + r_out) / 2.0

# ==================== 1. 构建主体几何 (旋转截面法) ====================
# 在 XZ 平面绘制1/2截面轮廓，通过旋转直接生成底环、直墙与锥顶组合体，规避 Shell 掏空报错
poly_points = [
    (r_in, 0),
    (r_base, 0),
    (r_base, BASE_HEIGHT),
    (r_out, BASE_HEIGHT),
    (r_out, BASE_HEIGHT + WALL_HEIGHT),
    (0, BASE_HEIGHT + WALL_HEIGHT + CAP_HEIGHT + WALL_THICKNESS),
    (0, BASE_HEIGHT + WALL_HEIGHT + CAP_HEIGHT),
    (r_in, BASE_HEIGHT + WALL_HEIGHT)
]

body = (
    cq.Workplane("XZ")
    .polyline(poly_points)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# ==================== 2. 阵列生成打孔工具体 ====================
hole_solids = []

# 直墙部分打孔
z_wall_start = BASE_HEIGHT + HOLE_SPACING / 2.0
z_wall_end = BASE_HEIGHT + WALL_HEIGHT - HOLE_SPACING / 2.0
num_wall_rows = int((z_wall_end - z_wall_start) / HOLE_SPACING) + 1
num_holes_wall_row = int((2 * math.pi * r_mid) / HOLE_SPACING)

for row in range(num_wall_rows):
    z = z_wall_start + row * HOLE_SPACING
    angle_step = 360.0 / num_holes_wall_row
    # 交错排列排孔，使受力更均匀
    angle_offset = (row % 2) * (angle_step / 2.0)
    
    for h in range(num_holes_wall_row):
        angle = h * angle_step + angle_offset
        # 创建沿X轴正向的单侧切削圆柱，通过绕Z轴旋转覆盖圆周
        cyl = cq.Solid.makeCylinder(PERFORATION_DIAMETER / 2.0, BASE_DIAMETER, cq.Vector(0, 0, z), cq.Vector(1, 0, 0))
        cyl = cyl.rotate(cq.Vector(0, 0, z), cq.Vector(0, 0, z + 1), angle)
        hole_solids.append(cyl)

# 锥顶部分打孔
z_cone_start = BASE_HEIGHT + WALL_HEIGHT + HOLE_SPACING / 2.0
z_cone_end = BASE_HEIGHT + WALL_HEIGHT + CAP_HEIGHT - HOLE_SPACING / 2.0
num_cone_rows = int((z_cone_end - z_cone_start) / HOLE_SPACING) + 1

for row in range(num_cone_rows):
    z = z_cone_start + row * HOLE_SPACING
    # 根据高度按比例线性缩小当前锥层半径
    r_cone = r_mid * ((BASE_HEIGHT + WALL_HEIGHT + CAP_HEIGHT - z) / CAP_HEIGHT)
    if r_cone < PERFORATION_DIAMETER:
        continue
        
    num_holes_cone_row = int((2 * math.pi * r_cone) / HOLE_SPACING)
    if num_holes_cone_row < 1:
        num_holes_cone_row = 1
        
    angle_step = 360.0 / num_holes_cone_row
    angle_offset = (row % 2) * (angle_step / 2.0)
    
    for h in range(num_holes_cone_row):
        angle = h * angle_step + angle_offset
        cyl = cq.Solid.makeCylinder(PERFORATION_DIAMETER / 2.0, BASE_DIAMETER, cq.Vector(0, 0, z), cq.Vector(1, 0, 0))
        cyl = cyl.rotate(cq.Vector(0, 0, z), cq.Vector(0, 0, z + 1), angle)
        hole_solids.append(cyl)

# ==================== 3. 稳健布尔切除与导出 ====================
if hole_solids:
    # 将所有打孔实体合并为一个复合体，执行单次高效布尔切除
    hole_compound = cq.Compound.makeCompound(hole_solids)
    result = body.cut(hole_compound)
else:
    result = body

# 导出为标准工业 3MF 格式
cq.exporters.export(result, "output_model.3mf")
