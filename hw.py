import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

def add_jitter(img, max_jitter=1):
    rows, cols = img.shape[:2]
    # 创建坐标网格
    x, y = np.meshgrid(np.arange(cols), np.arange(rows))
    # 生成较小的随机抖动
    dx = np.random.randint(-max_jitter, max_jitter+1, size=(rows, cols)).astype(np.float32)
    dy = np.random.randint(-max_jitter, max_jitter+1, size=(rows, cols)).astype(np.float32)
    # 计算新的映射坐标
    map_x = (x + dx).astype(np.float32)
    map_y = (y + dy).astype(np.float32)
    # 重映射图像
    img_jitter = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return img_jitter

def add_noise(img, mean=0, var=5):  # 减小噪声方差
    sigma = var ** 0.5
    gauss = np.random.normal(mean, sigma, img.shape).astype(np.uint8)
    img_noise = cv2.add(img, gauss)
    return img_noise

def random_transform(img):
    rows, cols = img.shape[:2]
    # 减小仿射变换范围
    pts1 = np.float32([[0, 0], [cols, 0], [0, rows]])
    random_shift = 3  # 减小随机偏移量
    pts2 = pts1 + np.random.randint(-random_shift, random_shift+1, pts1.shape).astype(np.float32)
    M = cv2.getAffineTransform(pts1, pts2)
    img_transformed = cv2.warpAffine(img, M, (cols, rows), borderValue=(255, 255, 255))
    return img_transformed

def wrap_text(text, font, max_width, draw):
    lines = []
    words = text.split('\n')
    for word in words:
        line = ''
        for char in word:
            bbox = draw.textbbox((0, 0), line + char, font=font)
            line_width = bbox[2] - bbox[0]
            if line_width <= max_width:
                line += char
            else:
                lines.append(line)
                line = char
        lines.append(line)
    return lines

# 读取代码文件内容
with open('./input.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# 设置图像大小
img_width = 1668
img_height = 2388

# 选择字体和大小
font_path = "./rabiohead.ttf"  # 替换为你的字体路径
font_size = 80  # 增大字体大小
font = ImageFont.truetype(font_path, font_size)

# 准备绘制参数
bbox = font.getbbox('hg')
line_height = bbox[3] - bbox[1] + 10  # 行高，增加行间距
max_text_width = img_width - 100  # 左右各留50像素边距

# 处理文本换行
# 创建一个临时的绘图对象，用于计算文本宽度
dummy_img = Image.new('RGB', (img_width, img_height), (255, 255, 255))
dummy_draw = ImageDraw.Draw(dummy_img)
lines = wrap_text(text, font, max_text_width, dummy_draw)

# 初始化变量
pages = []
current_line = 0
total_lines = len(lines)
page_number = 1

while current_line < total_lines:
    # 创建白色背景的空白图像
    img = np.full((img_height, img_width, 3), 255, dtype=np.uint8)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    
    y_text = 50  # 初始y坐标
    
    while y_text < img_height - 50 and current_line < total_lines:
        line = lines[current_line]
        draw.text((50, y_text), line, font=font, fill=(0, 0, 0))
        y_text += line_height
        current_line += 1
    
    # 将PIL图像转换回OpenCV图像
    img = np.array(img_pil)
    
    # 添加手写效果
    img = add_jitter(img, max_jitter=1)  # 减小抖动
    # img = add_noise(img, var=1)          # 减小噪声
    img = cv2.GaussianBlur(img, (3, 3), 0)
    img = random_transform(img)          # 减小仿射变换范围
    
    # 保存结果
    cv2.imwrite(f'page_{page_number}.png', img)
    page_number += 1

print(f"总共生成了 {page_number - 1} 张图片。")