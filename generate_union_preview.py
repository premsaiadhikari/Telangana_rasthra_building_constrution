from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1200, 1200
img = Image.new('RGBA', (W, H), (255, 255, 255, 0))
d = ImageDraw.Draw(img)

cx, cy = W // 2, H // 2
r = 540
# blue outer circle
for rr in range(r, r - 40, -1):
    d.ellipse((cx - rr, cy - rr, cx + rr, cy + rr), outline=(21, 46, 92, 255), width=28)
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(14, 36, 80, 255))
d.ellipse((cx - r + 24, cy - r + 24, cx + r - 24, cy + r - 24), outline=(190, 140, 60, 255), width=28)

# fonts
try:
    font_big = ImageFont.truetype('arial.ttf', 58)
    font_small = ImageFont.truetype('arial.ttf', 38)
    font_bar = ImageFont.truetype('arial.ttf', 42)
except Exception:
    font_big = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_bar = ImageFont.load_default()

# top arc title
text_top = 'TELANGANA RASHTRA BUILDING CONSTRUCTION WORKERS UNION'
for idx, ch in enumerate(text_top):
    ang = 180 + (360 * idx / len(text_top))
    x = cx + math.cos(math.radians(ang)) * 370
    y = cy + math.sin(math.radians(ang)) * 370
    bbox = d.textbbox((0, 0), ch, font=font_big)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text((x - w/2, y - h/2), ch, font=font_big, fill=(245, 245, 245, 255))

# lower arc text
text_bottom = 'BUILDING TODAY • STRENGTHENING TOMORROW'
for idx, ch in enumerate(text_bottom):
    ang = 360 - (360 * idx / len(text_bottom))
    x = cx + math.cos(math.radians(ang)) * 360
    y = cy + math.sin(math.radians(ang)) * 360
    bbox = d.textbbox((0, 0), ch, font=font_small)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    d.text((x - w/2, y - h/2), ch, font=font_small, fill=(245, 245, 245, 255))

# building silhouettes
blocks = [
    (150, 260, 260, 420, (120, 152, 194, 255)),
    (260, 190, 370, 440, (84, 99, 145, 255)),
    (360, 240, 470, 420, (82, 115, 164, 255)),
    (500, 200, 620, 440, (123, 143, 180, 255)),
    (620, 260, 720, 430, (76, 94, 132, 255)),
]
for bx, by, ex, ey, col in blocks:
    d.rectangle((bx, by, ex, ey), fill=col)
    for wx in range(bx + 12, ex - 10, 24):
        for wy in range(by + 18, ey - 10, 26):
            d.rectangle((wx, wy, wx + 12, wy + 16), fill=(196, 214, 236, 220))

# cranes
beam_color = (224, 164, 62, 255)
for x1, y1, x2, y2 in [
    (190, 250, 520, 250),
    (520, 250, 660, 250),
    (210, 310, 540, 310),
    (240, 360, 600, 360),
    (100, 390, 700, 390),
    (250, 450, 650, 450),
]:
    d.line((x1, y1, x2, y2), fill=beam_color, width=10)
for xs, ys, xe, ye in [(300, 180, 300, 500), (500, 180, 500, 500), (350, 180, 430, 180), (410, 180, 530, 180)]:
    d.line((xs, ys, xe, ye), fill=beam_color, width=10)
for x in [270, 320, 370, 420, 470, 520, 570]:
    d.line((x, 200, x, 500), fill=(226, 173, 82, 255), width=4)

# equipment
for x in [180, 310]:
    d.rectangle((x, 670, x + 95, 740), fill=(215, 163, 40, 255))
for x in [250, 300, 325]:
    d.line((x, 670, x + 50, 610), fill=(210, 185, 110, 255), width=10)
for wx, wy in [(680, 760), (840, 760)]:
    d.ellipse((wx - 40, wy - 30, wx + 40, wy + 30), fill=(45, 55, 60, 255))
for x in [708, 790, 842]:
    d.rectangle((x, 620, x + 55, 700), fill=(230, 230, 230, 255))

# lower badge
# outer badge
x1, y1, x2, y2 = 200, 820, 1000, 1080
d.rounded_rectangle((x1, y1, x2, y2), radius=80, fill=(13, 35, 79, 255), outline=(197, 144, 64, 255), width=24)
# map shape
points = [(410, 900), (500, 860), (590, 900), (620, 980), (560, 1045), (500, 1010), (440, 1048), (380, 980)]
d.polygon(points, fill=(183, 121, 44, 255), outline=(20, 35, 75, 255), width=10)
# gear details
for gx, gy in [(290, 935), (690, 935)]:
    d.ellipse((gx - 80, gy - 80, gx + 80, gy + 80), fill=(13, 35, 79, 255), outline=(197, 144, 64, 255), width=18)
    d.ellipse((gx - 35, gy - 35, gx + 35, gy + 35), fill=(13, 35, 79, 255), outline=(197, 144, 64, 255), width=10)
    for a in range(0, 360, 45):
        ang = math.radians(a)
        x1a = gx + math.cos(ang) * 70
        y1a = gy + math.sin(ang) * 70
        x2a = gx + math.cos(ang) * 90
        y2a = gy + math.sin(ang) * 90
        d.line((x1a, y1a, x2a, y2a), fill=(197, 144, 64, 255), width=8)

msg = 'BUILDING TODAY • STRENGTHENING TOMORROW'
bbox = d.textbbox((0, 0), msg, font=font_bar)
text_w = bbox[2] - bbox[0]
d.text((W / 2 - text_w / 2, 1020), msg, font=font_bar, fill=(245, 245, 245, 255))

# worker silhouettes
for i in range(10):
    x = 220 + i * 60
    d.ellipse((x, 760, x + 20, 780), fill=(245, 220, 180, 255))
    d.line((x + 10, 780, x + 7, 835), fill=(228, 171, 75, 255), width=8)
    d.line((x + 7, 785, x - 10, 820), fill=(228, 171, 75, 255), width=8)
    d.line((x + 7, 785, x + 20, 818), fill=(228, 171, 75, 255), width=8)

img.save('assets/images/union-preview.png', format='PNG')
print('generated assets/images/union-preview.png')
