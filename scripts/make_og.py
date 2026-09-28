"""Share preview image (1200x630) in the PRIE_NOTE_V1_DARK style.
Usage: python scripts/make_og.py <folder with Pretendard-ExtraBold/SemiBold/Medium .otf>  -> og.png"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

fonts = sys.argv[1]
F = lambda w, s: ImageFont.truetype(os.path.join(fonts, f'Pretendard-{w}.otf'), s)
BG, TEXT, SUB, DIM, LIME, LINE = '#070708', '#F5F5F2', '#8E8E93', '#58585D', '#C8FF3D', '#26262A'

im = Image.new('RGB', (1200, 630), BG)
d = ImageDraw.Draw(im)
x = 80
# brand row
d.text((x, 70), 'ADsP', font=F('ExtraBold', 30), fill=TEXT)
w = d.textlength('ADsP', font=F('ExtraBold', 30))
d.ellipse((x + w + 12, 84, x + w + 24, 96), fill=LIME)
d.text((x + w + 36, 70), '무료 문제풀이', font=F('SemiBold', 30), fill=SUB)
# badge
bx = 1200 - 80 - 150
d.rounded_rectangle((bx, 66, bx + 150, 110), radius=10, outline=LIME, width=2)
d.text((bx + 75, 88), '제51회 대비', font=F('SemiBold', 24), fill=TEXT, anchor='mm')
# title
d.text((x, 180), 'ADsP 문제, 무료로', font=F('ExtraBold', 88), fill=TEXT)
d.text((x, 290), '근거까지 확인하며', font=F('ExtraBold', 88), fill=TEXT)
# sub
d.text((x, 420), '10문제 실력 진단 · 모의고사 · 합격 예측 · 오답노트', font=F('Medium', 34), fill=SUB)
# footer
d.line((x, 520, 1200 - 80, 520), fill=LINE, width=2)
d.text((x, 545), '로그인 없이 · 자체 제작 예상문제', font=F('Medium', 26), fill=DIM)
d.text((1200 - 80, 545), '@prie.note', font=F('SemiBold', 26), fill=SUB, anchor='ra')

out = os.path.join(os.path.dirname(__file__), '..', 'og.png')
im.save(out, optimize=True)
print(os.path.normpath(out), os.path.getsize(out))
