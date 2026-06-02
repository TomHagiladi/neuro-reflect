# -*- coding: utf-8 -*-
"""יוצר שקף 'שיקולי המנחה' כתמונה דרך gpt-image-2."""
import sys
sys.path.insert(0, r'C:\Users\tomha\claude code\integrations\chatgpt-api')
from openai_utils import generate_image, save_image

PROMPT = r"""
A clean, modern educational presentation slide, landscape 16:9, flat minimalist design.
Warm-academic palette: deep purple and teal accents on a soft off-white background. Subtle neural-network dots in the far background, very faint.

Layout = a horizontal SPECTRUM with a long arrow across the middle, and two labeled poles at each end, plus a highlighted choice marker near the left pole.

The slide must render the following HEBREW text EXACTLY, right-to-left, with correct Hebrew spelling and no garbled letters. Do not invent or alter any words.

TITLE (top center, bold, large):
שיקולי המנחה — איך לעצב את חוויית ה-AI?

RIGHT POLE (a rounded box on the right side):
בוט מוביל בשרשרת שאלות
כולם בתלם מוגדר

LEFT POLE (a rounded box on the left side):
פרומפט פתיחה אחד
כל אחד מתבדר למסע שלו

HIGHLIGHTED MARKER (a glowing pin near the left pole, in teal):
הבחירה שלנו — מתבדר אך מעוגן

BOTTOM CAPTION (centered, smaller):
בכל מקרה מרוויחים את השיחה

Elegant, lots of whitespace, professional, legible large Hebrew typography. No English text anywhere on the slide.
"""

img = generate_image(PROMPT, model="gpt-image-2", size="1536x1024", quality="high")
out = r"g:\האחסון שלי\תום הגלעדי - העסק\בינה מלאכותית\הרצאות קורסים וסדנאות\נוירופדגוגיה\סיכומי פגישות צוות נוירופדגוגיה\מפגש-אחרון-חומרים\שקף-שיקולי-מנחה.png"
save_image(img, out)
print("saved:", out)
