# -*- coding: utf-8 -*-
"""יוצר קובץ Word להדפסה: כרטיסי 'פתק להקראה' בעמוד אחד, מעוצבים, מוכנים לחיתוך."""
import copy
from docx import Document
from docx.shared import Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NOTE = (
    "שלום ג'מיני. אני מורה / מנהלת / סגנית (וכו') שזה עתה סיימתי קורס "
    "בנוירופדגוגיה ובבינה מלאכותית. אני רוצה לנהל איתך שיחה קולית רפלקטיבית "
    "על מי שאני היום כמורה, לאור מה שלקחתי מהתהליך שעברנו בקורס.\n\n"
    "אני מבקשת שתעזור לי לזקק זאת — שאלה אחת בכל פעם, בנחת — ולחלץ את ה-“why” "
    "שמניע אותי (ברוח התיאוריה “Start With Why” של סיימון סינק), "
    "בהקשר של קורס הנוירופדגוגיה.\n\n"
    "בוא נתחיל. שאל אותי את השאלה הראשונה."
)
ACCENT = RGBColor(0x5b, 0x3e, 0x8e)
INK = RGBColor(0x2a, 0x24, 0x3a)

def set_rtl(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    bidi = OxmlElement('w:bidi'); bidi.set(qn('w:val'), '1'); pPr.append(bidi)

def rtl_run(run):
    rPr = run._element.get_or_add_rPr()
    rtl = OxmlElement('w:rtl'); rtl.set(qn('w:val'), '1'); rPr.append(rtl)

def set_cell_border(cell, color="C9BCE6", sz="12", dash="dashed"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        e = OxmlElement('w:' + edge)
        e.set(qn('w:val'), dash); e.set(qn('w:sz'), sz)
        e.set(qn('w:space'), '0'); e.set(qn('w:color'), color)
        borders.append(e)
    tcPr.append(borders)

def shade_cell(cell, fill="FAF8FE"):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear')
    sh.set(qn('w:color'), 'auto'); sh.set(qn('w:fill'), fill); tcPr.append(sh)

def add_card(cell):
    cell.paragraphs[0]._p.getparent().remove(cell.paragraphs[0]._p)
    # title
    p = cell.add_paragraph(); set_rtl(p); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(4); p.paragraph_format.space_before = Pt(2)
    r = p.add_run("🎙️  שיחה רפלקטיבית עם הבינה"); rtl_run(r)
    r.font.name = "Heebo"; r.font.size = Pt(11.5); r.font.bold = True; r.font.color.rgb = ACCENT
    # body
    for i, block in enumerate(NOTE.split("\n\n")):
        bp = cell.add_paragraph(); set_rtl(bp); bp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        bp.paragraph_format.space_after = Pt(3); bp.paragraph_format.line_spacing = 1.18
        br = bp.add_run(block); rtl_run(br)
        br.font.name = "Heebo"; br.font.size = Pt(10.5); br.font.color.rgb = INK
    # footer tag
    fp = cell.add_paragraph(); set_rtl(fp); fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
    fp.paragraph_format.space_before = Pt(3)
    fr = fp.add_run("✂ — — — — — — — — — — — — — — — — — — — —")
    fr.font.size = Pt(8); fr.font.color.rgb = RGBColor(0xB0, 0xA4, 0xCC)
    shade_cell(cell); set_cell_border(cell)

doc = Document()
sec = doc.sections[0]
sec.page_height = Mm(297); sec.page_width = Mm(210)
sec.top_margin = Mm(10); sec.bottom_margin = Mm(10)
sec.left_margin = Mm(10); sec.right_margin = Mm(10)

# heading
h = doc.add_paragraph(); set_rtl(h); h.alignment = WD_ALIGN_PARAGRAPH.CENTER
h.paragraph_format.space_after = Pt(6)
hr = h.add_run("פתקי הקראה — שיחה רפלקטיבית קולית · גזרו וחלקו"); rtl_run(hr)
hr.font.name = "Heebo"; hr.font.size = Pt(12); hr.font.bold = True
hr.font.color.rgb = RGBColor(0x1f, 0x8a, 0x8a)

ROWS, COLS = 3, 2
table = doc.add_table(rows=ROWS, cols=COLS)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
table.autofit = False
for row in table.rows:
    row.height = Mm(86)
    for cell in row.cells:
        cell.width = Mm(93)
        add_card(cell)

out = r"C:\Users\tomha\neuro-reflect-build\פתק-הקראה-להדפסה.docx"
doc.save(out)
print("saved:", out)
print("cards:", ROWS * COLS)
