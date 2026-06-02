# -*- coding: utf-8 -*-
"""יוצר ברקוד QR לכתובת העמוד החי."""
import qrcode
from qrcode.constants import ERROR_CORRECT_M

URL = "https://tomhagiladi.github.io/neuro-reflect/"
qr = qrcode.QRCode(version=None, error_correction=ERROR_CORRECT_M, box_size=16, border=3)
qr.add_data(URL)
qr.make(fit=True)
img = qr.make_image(fill_color="#2a2350", back_color="white")
out = r"g:\האחסון שלי\תום הגלעדי - העסק\בינה מלאכותית\הרצאות קורסים וסדנאות\נוירופדגוגיה\סיכומי פגישות צוות נוירופדגוגיה\מפגש-אחרון-חומרים\פרומפט-גרסה-א_QR.png"
img.save(out)
print("saved:", out)
print("url:", URL)
