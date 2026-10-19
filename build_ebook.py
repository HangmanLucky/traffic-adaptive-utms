# -*- coding: utf-8 -*-
"""
Ebook generator - Automation Skills Portfolio series
Civil Engineering Technology (Transportation): Adaptive Urban Traffic Management System
Author: Sipho Lucky Sibanda
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Sans", FD + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold", FD + "DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Oblique", FD + "DejaVuSans-Oblique.ttf"))
pdfmetrics.registerFont(TTFont("Cond-Bold", FD + "DejaVuSansCondensed-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Cond", FD + "DejaVuSansCondensed.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FD + "DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", FD + "DejaVuSansMono-Bold.ttf"))

# Palette - amber "traffic signal" identity on dark asphalt
BASE      = colors.HexColor("#0F1114")
BASE2     = colors.HexColor("#171A1E")
BASE_LINE = colors.HexColor("#2A2E34")
AMBERACC  = colors.HexColor("#FFC107")
AMBERACC_LT = colors.HexColor("#FFE9A8")
DEEPAMBER = colors.HexColor("#8A5F00")
GREEN     = colors.HexColor("#2ECC71")
RED       = colors.HexColor("#E63946")
CYAN      = colors.HexColor("#2FB8C4")
INK       = colors.HexColor("#1D1F22")
MUTED     = colors.HexColor("#6B7278")
MUTED_LT  = colors.HexColor("#C9CFD5")
PANEL     = colors.HexColor("#F6F1E3")
ROWBAND   = colors.HexColor("#FBF8EF")
GRIDLINE  = colors.HexColor("#E8E0C8")

PAGE_W, PAGE_H = A4
MARGIN_L, MARGIN_R = 22 * mm, 20 * mm
MARGIN_TOP, MARGIN_BOT = 26 * mm, 24 * mm
AVAIL_W = PAGE_W - MARGIN_L - MARGIN_R

DOC_TITLE = "ADAPTIVE URBAN TRAFFIC MANAGEMENT SYSTEM"
AUTHOR = "Sipho Lucky Sibanda"
OUTFILE = os.path.join(HERE, "Traffic_Technical_Manual.pdf")
IMG_DIAGRAM = os.path.join(HERE, "..", "images", "architecture_diagram.png")
IMG_HMI = os.path.join(HERE, "..", "images", "hmi-dashboard.png")

# The architecture diagram is stored as SVG in the repo; ReportLab needs a raster
# image, so render a PNG from the SVG on demand (requires: pip install cairosvg).
if not os.path.exists(IMG_DIAGRAM):
    import cairosvg
    cairosvg.svg2png(url=IMG_DIAGRAM.replace(".png", ".svg"),
                     write_to=IMG_DIAGRAM, output_width=2200)

body = ParagraphStyle("body", fontName="Sans", fontSize=10.2, leading=15,
                       textColor=INK, spaceAfter=8, alignment=TA_JUSTIFY)
lead = ParagraphStyle("lead", parent=body, fontSize=12.5, leading=18, textColor=DEEPAMBER, spaceAfter=10)
kicker = ParagraphStyle("kicker", fontName="Mono", fontSize=8.5, leading=11, textColor=DEEPAMBER, spaceAfter=2)
h1 = ParagraphStyle("h1", fontName="Cond-Bold", fontSize=19, leading=22, textColor=colors.HexColor("#4A3300"), spaceAfter=2)
h2 = ParagraphStyle("h2", fontName="Cond-Bold", fontSize=13.5, leading=16, textColor=colors.HexColor("#4A3300"), spaceBefore=14, spaceAfter=6)
caption = ParagraphStyle("caption", fontName="Sans-Oblique", fontSize=8.3, leading=11, textColor=MUTED, alignment=TA_CENTER, spaceBefore=4, spaceAfter=10)
bullet = ParagraphStyle("bullet", parent=body, alignment=TA_LEFT, leftIndent=12, bulletIndent=0, spaceAfter=5)
chip_num = ParagraphStyle("chip_num", fontName="Cond-Bold", fontSize=17, leading=20, textColor=colors.HexColor("#1D1F22"), alignment=TA_CENTER)
toc_entry = ParagraphStyle("toc_entry", fontName="Sans", fontSize=10.5, leading=16, textColor=INK)
toc_num = ParagraphStyle("toc_num", fontName="Mono-Bold", fontSize=10.5, leading=16, textColor=DEEPAMBER)
cell_hdr = ParagraphStyle("cell_hdr", fontName="Sans-Bold", fontSize=8.6, leading=11, textColor=colors.white)
cell_txt = ParagraphStyle("cell_txt", fontName="Sans", fontSize=8.6, leading=12, textColor=INK)
code_style = ParagraphStyle("code", fontName="Mono", fontSize=7.5, leading=11.0, textColor=AMBERACC_LT)
callout_title = lambda c: ParagraphStyle("ct", fontName="Sans-Bold", fontSize=9.6, leading=12, textColor=c, spaceAfter=3)
callout_body = ParagraphStyle("cb", fontName="Sans", fontSize=9.4, leading=13.4, textColor=INK)

def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def P(text, style=body):
    return Paragraph(text, style)

def chapter_head(num, title, kicker_text="ADAPTIVE TRAFFIC CONTROL"):
    chip = Table([[Paragraph(str(num).zfill(2), chip_num)]], colWidths=[17 * mm], rowHeights=[17 * mm])
    chip.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), AMBERACC),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("ALIGN", (0, 0), (-1, -1), "CENTER")]))
    title_block = [P(kicker_text, kicker), P(title, h1)]
    row = Table([[chip, title_block]], colWidths=[22 * mm, AVAIL_W - 22 * mm])
    row.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("LEFTPADDING", (0, 0), (0, 0), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
    rule = HRFlowable(width="100%", thickness=1.3, color=AMBERACC, spaceBefore=8, spaceAfter=16)
    return [row, rule]

def subhead(text):
    return P(text, h2)

def bullets(items):
    return [P("&#8226;&nbsp;&nbsp;" + it, bullet) for it in items]

def code_block(code_text, cap=None):
    lines = code_text.strip("\n").split("\n")
    esc_lines = []
    for ln in lines:
        stripped = ln.lstrip(" ")
        n = len(ln) - len(stripped)
        esc_lines.append("&nbsp;" * n + esc(stripped) if stripped else "&nbsp;")
    para = Paragraph("<br/>".join(esc_lines), code_style)
    cell = Table([[para]], colWidths=[AVAIL_W])
    cell.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BASE2), ("BOX", (0, 0), (-1, -1), 0.75, BASE_LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9)]))
    out = [cell]
    out.append(P(cap, caption) if cap else Spacer(1, 10))
    return out

def data_table(headers, rows, col_widths=None):
    data = [[Paragraph(h, cell_hdr) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), cell_txt) for c in r])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4A3300")), ("GRID", (0, 0), (-1, -1), 0.5, GRIDLINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5), ("LEFTPADDING", (0, 0), (-1, -1), 6)]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), ROWBAND))
    t.setStyle(TableStyle(style))
    return t

def callout(title, text, kind="info"):
    color = {"info": CYAN, "warning": AMBERACC, "critical": RED, "ok": GREEN}[kind]
    label = {"info": "NOTE", "warning": "ENGINEERING NOTE", "critical": "HONEST LIMITATION", "ok": "DESIGN NOTE"}[kind]
    content = [P("%s &mdash; %s" % (label, title), callout_title(DEEPAMBER if kind == "warning" else color)),
               P(text, callout_body)]
    inner = Table([[content]], colWidths=[AVAIL_W - 16])
    inner.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0)]))
    outer = Table([["", inner]], colWidths=[5, AVAIL_W - 5])
    outer.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, 0), color), ("BACKGROUND", (1, 0), (1, 0), PANEL),
        ("LEFTPADDING", (1, 0), (1, 0), 12), ("RIGHTPADDING", (1, 0), (1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return [outer, Spacer(1, 10)]

def full_image(path, cap, max_h_mm=95):
    from PIL import Image as PILImage
    iw, ih = PILImage.open(path).size
    ratio = ih / float(iw)
    w = AVAIL_W
    h = w * ratio
    max_h = max_h_mm * mm
    if h > max_h:
        h = max_h
        w = h / ratio
    img = Image(path, width=w, height=h)
    img.hAlign = "CENTER"
    return [img, P(cap, caption)]

def draw_cover(c, doc):
    c.saveState()
    c.setFillColor(BASE); c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setStrokeColor(BASE_LINE); c.setLineWidth(0.4)
    step = 12 * mm
    x = 0
    while x < PAGE_W:
        c.line(x, 0, x, PAGE_H); x += step
    y = 0
    while y < PAGE_H:
        c.line(0, y, PAGE_W, y); y += step
    c.setStrokeColor(AMBERACC); c.setLineWidth(1.1)
    c.rect(10 * mm, 10 * mm, PAGE_W - 20 * mm, PAGE_H - 20 * mm, fill=0, stroke=1)
    cx, cy = PAGE_W - 48 * mm, 30 * mm
    c.setFillColor(colors.HexColor("#0a0b0d")); c.setStrokeColor(colors.HexColor("#555b62")); c.setLineWidth(1.2)
    c.roundRect(cx - 7*mm, cy, 14*mm, 36*mm, 3*mm, fill=1, stroke=1)
    c.setFillColor(RED);      c.circle(cx, cy + 29*mm, 3.6*mm, fill=1, stroke=0)
    c.setFillColor(AMBERACC); c.circle(cx, cy + 18*mm, 3.6*mm, fill=1, stroke=0)
    c.setFillColor(GREEN);    c.circle(cx, cy + 7*mm,  3.6*mm, fill=1, stroke=0)
    c.setFillColor(AMBERACC); c.setFont("Mono", 10.5)
    c.drawString(24 * mm, PAGE_H - 42 * mm, "AUTOMATION SKILLS PORTFOLIO   ·   CIVIL / TRANSPORTATION")
    c.setFillColor(colors.white); c.setFont("Cond-Bold", 24)
    for i, line in enumerate(["ADAPTIVE URBAN TRAFFIC", "MANAGEMENT SYSTEM"]):
        c.drawString(24 * mm, PAGE_H - 62 * mm - i * 11.5 * mm, line)
    c.setFont("Cond", 13.5); c.setFillColor(MUTED_LT)
    c.drawString(24 * mm, PAGE_H - 90 * mm, "with Vehicle Loop Sensor Optimization")
    c.setStrokeColor(BASE_LINE); c.setLineWidth(0.8)
    c.line(24 * mm, 46 * mm, PAGE_W - 24 * mm, 46 * mm)
    c.setFont("Mono", 9.5); c.setFillColor(AMBERACC)
    c.drawString(24 * mm, 38 * mm, "TECHNICAL PROJECT MANUAL  ·  REV. A")
    c.setFont("Sans-Bold", 13); c.setFillColor(colors.white)
    c.drawString(24 * mm, 31 * mm, "By " + AUTHOR)
    c.setFont("Sans", 8.6); c.setFillColor(MUTED_LT)
    c.drawString(24 * mm, 25.5 * mm, "Platform: Siemens S7-1500 (SCL) / CODESYS-portable Structured Text")
    c.drawString(24 * mm, 21 * mm, "Simulation & Portfolio Engineering Build  ·  Not for Traffic Cabinet Deployment")
    c.restoreState()

def draw_body(c, doc):
    c.saveState()
    c.setFillColor(BASE); c.rect(0, PAGE_H - 15 * mm, PAGE_W, 15 * mm, fill=1, stroke=0)
    c.setFillColor(AMBERACC); c.setFont("Mono", 7.6)
    c.drawString(MARGIN_L, PAGE_H - 9.5 * mm, DOC_TITLE)
    c.setFillColor(colors.white); c.setFont("Sans", 7.4)
    c.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 9.5 * mm, "By " + AUTHOR)
    c.setStrokeColor(AMBERACC); c.setLineWidth(0.8)
    c.line(0, PAGE_H - 15 * mm, PAGE_W, PAGE_H - 15 * mm)
    c.setFillColor(MUTED); c.setFont("Mono", 7.8)
    c.drawString(MARGIN_L, 13 * mm, "ADAPTIVE-UTMS")
    c.drawCentredString(PAGE_W / 2, 13 * mm, "Page %d" % c.getPageNumber())
    c.drawRightString(PAGE_W - MARGIN_R, 13 * mm, "Simulation / Portfolio Build")
    c.setStrokeColor(AMBERACC); c.setLineWidth(1)
    c.line(PAGE_W - MARGIN_R, 17 * mm, PAGE_W - MARGIN_R, 21 * mm)
    c.line(PAGE_W - MARGIN_R - 4 * mm, 17 * mm, PAGE_W - MARGIN_R, 17 * mm)
    c.restoreState()


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
story = [PageBreak()]

story += chapter_head("i", "Document Control &amp; Disclaimer", "FRONT MATTER")
story.append(P(
    "This document is a self-authored technical project manual produced as part of a "
    "personal engineering portfolio. It describes the design, control philosophy, and "
    "simulated validation of an adaptive, loop-actuated urban traffic signal controller, "
    "built to demonstrate actuated phase sequencing, fairness-aware green allocation, "
    "pedestrian safety logic, and emergency vehicle preemption for automation, controls, "
    "and civil/transportation engineering roles.", body))
story.append(P(
    "The system described here was developed and tested in simulation only (PLCSIM-style "
    "forcing of inputs and desktop review). No part of this project has been installed, "
    "commissioned, or verified on a physical traffic cabinet or live road, and it must not "
    "be treated as a certified traffic signal controller.", body))
story += callout(
    "Portfolio project, not a certified signal controller",
    "A real traffic signal controller is paired with an independent hardware conflict "
    "monitor, yellow and all-red intervals calculated per ITE guidance from actual "
    "approach speed and geometry, and formal approval from the responsible road "
    "authority. Figures, thresholds, and I/O in this manual are engineering-realistic but "
    "illustrative.", "critical")
data = [
    ["Document Title", "Adaptive Urban Traffic Management System \u2014 Technical Manual"],
    ["Author", AUTHOR],
    ["Revision", "A"],
    ["Document Type", "Portfolio Technical Manual (Simulation)"],
    ["Target Platform", "Siemens S7-1500 (TIA Portal / SCL) \u2014 CODESYS-portable"],
    ["Related Repository", "traffic-adaptive-utms"],
    ["Series", "Automation Skills Portfolio \u2014 Civil Engineering Technology"],
]
t = Table(data, colWidths=[45 * mm, AVAIL_W - 45 * mm])
t.setStyle(TableStyle([
    ("FONTNAME", (0, 0), (0, -1), "Sans-Bold"), ("FONTNAME", (1, 0), (1, -1), "Sans"),
    ("FONTSIZE", (0, 0), (-1, -1), 9.4), ("TEXTCOLOR", (0, 0), (0, -1), colors.HexColor("#4A3300")),
    ("TEXTCOLOR", (1, 0), (1, -1), INK), ("GRID", (0, 0), (-1, -1), 0.4, GRIDLINE),
    ("BACKGROUND", (0, 0), (0, -1), PANEL), ("TOPPADDING", (0, 0), (-1, -1), 6),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 6), ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
story.append(t)
story.append(PageBreak())

story += chapter_head("ii", "Contents", "FRONT MATTER")
toc = [
    ("01", "Industry Context: Actuated vs. Fixed-Time Signals"),
    ("02", "System Architecture &amp; Intersection Overview"),
    ("03", "Hardware &amp; Instrumentation Specification"),
    ("04", "I/O List"),
    ("05", "Control Philosophy: Gap-Out, Fairness &amp; Preemption"),
    ("06", "PLC Logic Walkthrough"),
    ("07", "HMI Design &amp; the Live Intersection Map"),
    ("08", "Alarm Philosophy &amp; Fail-Safe Design"),
    ("09", "Testing, Commissioning &amp; FAT Procedures"),
    ("10", "Limitations, Real-World Deltas &amp; Future Work"),
    ("A", "Appendix A &mdash; I/O Quick Reference"),
    ("B", "Appendix B &mdash; Full Structured Text Listing"),
    ("C", "Appendix C &mdash; Glossary"),
    ("&mdash;", "About the Author"),
]
rows = [[P(n, toc_num), P(tl, toc_entry)] for n, tl in toc]
tt = Table(rows, colWidths=[14 * mm, AVAIL_W - 14 * mm])
tt.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, GRIDLINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
story.append(tt)
story.append(PageBreak())

story += chapter_head("iii", "Executive Summary", "FRONT MATTER")
story.append(P(
    "This is the sixth deliberate discipline shift in the wider automation portfolio, "
    "moving from process and power systems toward real-time public infrastructure - a "
    "field where the people most affected by a control decision are not operators at all, "
    "but every driver and pedestrian passing through the intersection. A fixed-time "
    "signal gives every approach the same green regardless of whether anyone is actually "
    "there, wasting cycle time on an empty street while the opposite approach queues.", lead))
story.append(P(
    "<b>FB_Traffic_Intersection_Control</b> implements a genuinely actuated controller: "
    "in-pavement loop detectors extend green only while vehicles keep arriving (a "
    "<b>vehicle extension gap</b>), a green ends early when that gap expires with no "
    "further demand (<b>gap-out</b>), and a hard <b>maximum green</b> ceiling prevents any "
    "single stream from holding the intersection indefinitely. A <b>longest-wait "
    "register</b> per direction drives a fairness override, cutting a green short - once "
    "its own minimums are met - when the opposite approach has waited too long.", body))
story.append(P(
    "Two safety behaviours sit underneath all of that and cannot be overridden by "
    "efficiency logic: a <b>pedestrian clearance interval</b> that no vehicle-side "
    "decision may shortcut, and <b>emergency vehicle preemption</b> that transitions "
    "safely through all-red rather than snapping abruptly, then recovers from a clean "
    "all-red state rather than resuming mid-phase.", body))
story.append(P(
    "What follows documents the traffic engineering context, architecture, hardware "
    "assumptions, full I/O list, control philosophy, complete annotated code, HMI design, "
    "alarm philosophy, and the functional test procedure used to validate the logic in "
    "simulation.", body))
story.append(PageBreak())

story += chapter_head(1, "Industry Context: Actuated vs. Fixed-Time Signals")
story.append(P(
    "Traffic signals fall broadly into two families. <b>Fixed-time</b> (pre-timed) "
    "controllers run the same cycle regardless of conditions - simple, predictable, and "
    "well-suited to a coordinated corridor with very regular traffic patterns. "
    "<b>Actuated</b> controllers read detectors and adapt in real time, which is "
    "dramatically more efficient at an isolated intersection with variable or "
    "unpredictable demand.", body))
story.append(subhead("The vocabulary of actuated control"))
story += bullets([
    "<b>Minimum green</b> &mdash; the shortest green any phase may show, once started, "
    "regardless of demand. It exists so a driver is never given a green that vanishes "
    "before they can reasonably react to it.",
    "<b>Vehicle extension (gap)</b> &mdash; each new detector actuation restarts a short "
    "timer; as long as vehicles keep arriving within that gap, the green is extended.",
    "<b>Gap-out</b> &mdash; when the gap timer expires with no new actuation, the stream "
    "has effectively dried up and the green may terminate.",
    "<b>Maximum green</b> &mdash; a hard ceiling that ends the green even if actuations "
    "never stop, protecting the cross street from indefinite delay.",
])
story += callout(
    "Why these terms matter beyond this project",
    "These are the same terms a NEMA-style traffic cabinet controller's programming "
    "interface uses directly. Implementing them faithfully - rather than inventing a "
    "bespoke \"smart traffic\" vocabulary - is deliberate: it makes this project's logic "
    "legible to anyone who has configured a real signal controller.", "info")
story.append(subhead("Pedestrians and emergency vehicles are not edge cases"))
story.append(P(
    "A real intersection must accommodate pedestrians crossing at their own, much slower "
    "speed, and emergency vehicles that legitimately need right-of-way immediately. Both "
    "are routinely treated as exceptions bolted onto a vehicle-focused design, and both "
    "are, in this project, first-class parts of the logic rather than afterthoughts.", body))
story.append(PageBreak())

story += chapter_head(2, "System Architecture &amp; Intersection Overview")
story.append(P(
    "Four approaches (North, South, East, West) each carry an in-pavement loop detector "
    "and an emergency-vehicle preemption receiver. Two signal head groups - North-South "
    "and East-West - are driven by a single PLC function block, alongside pedestrian call "
    "buttons for each crossing direction.", body))
story += full_image(IMG_DIAGRAM,
    "Figure 2.1 &mdash; Control architecture. Dashed lines represent PLC input signal and "
    "configuration paths; solid lines represent the controller's signal head outputs.",
    max_h_mm=82)
story.append(subhead("Control hierarchy"))
story += bullets([
    "<b>Field layer</b> &mdash; four loop detectors, four EVP receivers, two pedestrian "
    "call buttons, two signal head groups.",
    "<b>Control layer</b> &mdash; a single PLC function block, "
    "<b>FB_Traffic_Intersection_Control</b>, hosted on a Siemens S7-1500 (or CODESYS-based "
    "traffic cabinet controller), running phase sequencing, fairness, pedestrian safety, "
    "and preemption.",
    "<b>Supervisory layer</b> &mdash; a traffic management HMI displaying the live "
    "intersection state and each direction's accumulated wait.",
])
story.append(KeepTogether([
    subhead("Why two phases (NS/EW), not four or eight"),
    P("A real intersection with protected left turns typically runs a NEMA dual-ring, "
      "multi-phase structure. This project deliberately models just two phases so the "
      "actuated-control, fairness, and preemption logic - where the real engineering "
      "interest lies - stays legible rather than being buried under phase-count "
      "bookkeeping. Chapter 10 names this plainly as a scope boundary.", body)]))
story.append(PageBreak())

story += chapter_head(3, "Hardware &amp; Instrumentation Specification")
story.append(P(
    "As with the rest of this portfolio, the logic here is platform-portable but written "
    "against a concrete reference platform so timings are grounded rather than arbitrary.", body))
story.append(data_table(
    ["Component", "Representative Spec", "Role"],
    [
        ["Traffic Cabinet Controller", "Siemens SIMATIC S7-1500", "Executes FB_Traffic_Intersection_Control"],
        ["Inductive Loop Detector", "In-pavement wire loop + detector card, per approach", "Vehicle presence/actuation"],
        ["EVP Receiver", "Optical or GPS-based preemption receiver, per approach", "Emergency vehicle request"],
        ["Pedestrian Push Button", "ADA-compliant, per crossing direction", "Pedestrian demand + WALK request"],
        ["Signal Heads", "LED R/Y/G + pedestrian WALK indication", "Right-of-way indication"],
        ["Conflict Monitor", "Independent hardware safety device (not modelled here)", "Forces flash on conflicting-green fault"],
    ],
    col_widths=[46 * mm, 70 * mm, AVAIL_W - 46 * mm - 70 * mm]))
story.append(Spacer(1, 8))
story += callout(
    "Yellow and all-red intervals are calculated, not chosen",
    "This project's 3-second yellow and 2-second all-red are illustrative defaults. On a "
    "real installation both are calculated per ITE guidance from the intersection's "
    "approach speed and geometry - a faster approach needs a longer yellow, and a wider "
    "intersection needs a longer all-red for the last vehicle to clear. Getting these "
    "wrong is a genuine safety defect, not a tuning preference.", "ok")
story.append(PageBreak())

story += chapter_head(4, "I/O List")
story.append(P(
    "The table below is the working I/O list for FB_Traffic_Intersection_Control (see also "
    "<b>docs/IO_List.md</b> in the repository, and Appendix A of this manual).", body))
story.append(subhead("Inputs"))
story.append(data_table(
    ["Tag", "Description", "Signal"],
    [
        ["DI_Loop_N / _S / _E / _W", "In-pavement vehicle presence loop, per approach", "Digital x4"],
        ["DI_PedCall_NS / DI_PedCall_EW", "Pedestrian call buttons", "Digital x2"],
        ["DI_EVP_N / _S / _E / _W", "Emergency vehicle preemption requests", "Digital x4"],
        ["DI_System_Enable", "Master enable", "Digital"],
    ],
    col_widths=[56 * mm, 80 * mm, AVAIL_W - 56 * mm - 80 * mm]))
story.append(Spacer(1, 10))
story.append(subhead("Outputs"))
story.append(data_table(
    ["Tag", "Description", "Signal"],
    [
        ["DO_NS_Green / _Yellow / _Red", "North-South signal head", "Digital x3"],
        ["DO_EW_Green / _Yellow / _Red", "East-West signal head", "Digital x3"],
        ["DO_NS_WalkSignal / DO_EW_WalkSignal", "Pedestrian WALK indications", "Digital x2"],
        ["CurrentPhase", "Current signal phase (enumeration)", "Internal / HMI tag"],
        ["WaitTime_NS_s / WaitTime_EW_s", "Longest-wait registers per direction", "REAL x2"],
        ["Alarm_PreemptionActive / SystemStatus", "Alarm + status text", "Digital / STRING"],
    ],
    col_widths=[56 * mm, 80 * mm, AVAIL_W - 56 * mm - 80 * mm]))
story.append(PageBreak())


story += chapter_head(5, "Control Philosophy: Gap-Out, Fairness &amp; Preemption")
story.append(P(
    "Four ideas define this controller's behaviour, layered so each one can only restrict "
    "what the one before it permits - never override a safety minimum.", body))
story.append(subhead("5.1 &nbsp; Actuated green: three independent ways to end it"))
story.append(P(
    "Once a green has satisfied both its minimum green and its pedestrian clearance "
    "interval, three separate conditions can end it: reaching <b>maximum green</b> "
    "(the hard ceiling), <b>gapping out</b> with no demand left on that approach, or "
    "the <b>fairness override</b> (5.2). They are evaluated in that order of "
    "specificity, and none of them can fire before the non-negotiable minimums have "
    "been met.", body))
story.append(subhead("5.2 &nbsp; Longest-wait fairness: why a gap-out controller still needs it"))
story.append(P(
    "A plain actuated controller has a subtle weakness: a steady stream of vehicles on "
    "one street can keep resetting the gap timer, holding that green until maximum green "
    "expires - and maximum green is typically long. Meanwhile, the cross street's drivers "
    "wait the entire time. The <b>longest-wait register</b> closes that gap: it "
    "accumulates only while a direction has genuine demand and is not currently green, "
    "and once it crosses a threshold, it ends the current green early - after minimums "
    "are met - rather than letting the stream run to its ceiling.", body))
story += callout(
    "The wait register is not a free-running clock",
    "It only accumulates while that direction has real demand <i>and</i> is not "
    "currently green. A direction with no vehicles or pedestrians waiting accumulates "
    "nothing, so an idle street never builds up a phantom wait that could trigger a "
    "needless fairness override against a busy one.", "ok")
story.append(subhead("5.3 &nbsp; Pedestrian clearance is a floor, not a preference"))
story.append(P(
    "Once a WALK indication has been given, the pedestrian clearance timer must complete "
    "before the phase may end - regardless of gap-out, max green, or fairness. A "
    "pedestrian already in the crosswalk is not part of the vehicle detection picture, "
    "and the logic treats their safety as a hard constraint rather than a variable to "
    "optimise against.", body))
story.append(subhead("5.4 &nbsp; Emergency preemption: fast, but never abrupt"))
story.append(P(
    "When an emergency vehicle request arrives, the controller doesn't snap instantly to "
    "green for the requesting direction - that would trap vehicles mid-intersection "
    "exactly as the cross traffic is released. It forces a safe all-red transition "
    "first, then holds green for the requesting direction until the request clears, then "
    "recovers through a clean all-red rather than resuming mid-phase. It also waits for "
    "an active pedestrian clearance interval to finish before beginning that transition.", body))
story.append(PageBreak())

story += chapter_head(6, "PLC Logic Walkthrough")
story.append(P(
    "This chapter walks through <b>FB_Traffic_Intersection_Control</b> section by section. "
    "The full listing is reproduced in Appendix B.", body))

story.append(KeepTogether([subhead("6.1 &nbsp; Demand detection and the longest-wait registers")] + code_block(
"""DemandNS := DI_Loop_N OR DI_Loop_S OR DI_PedCall_NS;
DemandEW := DI_Loop_E OR DI_Loop_W OR DI_PedCall_EW;

T_WaitNS(IN := DemandNS AND (CurrentPhase <> PH_NS_GREEN), PT := MaxWait_PT);
T_WaitEW(IN := DemandEW AND (CurrentPhase <> PH_EW_GREEN), PT := MaxWait_PT);
WaitTime_NS_s := TIME_TO_REAL(T_WaitNS.ET) / 1000.0;
WaitTime_EW_s := TIME_TO_REAL(T_WaitEW.ET) / 1000.0;""",
    "Listing 6.1 &mdash; The literal \"which lane has waited longest\" counters.")))

story.append(KeepTogether([subhead("6.2 &nbsp; Ending a green: three reasons, evaluated only after minimums")] + code_block(
"""IF T_MinGreen.Q AND T_PedClearance.Q THEN
    IF T_MaxGreen.Q THEN
        CurrentPhase := PH_NS_YELLOW;                                  // Ceiling reached
    ELSIF T_Gap.Q AND (NOT DemandNS) THEN
        CurrentPhase := PH_NS_YELLOW;                                  // Gapped out, no demand left
    ELSIF T_Gap.Q AND DemandEW AND (WaitTime_EW_s >= TIME_TO_REAL(MaxWait_PT)/1000.0) THEN
        CurrentPhase := PH_NS_YELLOW;                                  // Fairness override
    END_IF
END_IF""", "Listing 6.2 &mdash; Both minimums (vehicle AND pedestrian) gate everything below them.")))

story.append(KeepTogether([subhead("6.3 &nbsp; Resting instead of cycling through an empty phase")] + code_block(
"""PH_ALLRED_1:
    T_Clearance(IN := TRUE, PT := AllRedTime_PT);
    IF T_Clearance.Q THEN
        T_Clearance(IN := FALSE);
        IF DemandEW THEN
            CurrentPhase := PH_EW_GREEN;
        ELSIF DemandNS THEN
            CurrentPhase := PH_NS_GREEN;   // Nobody waiting across - rest in green
        END_IF
        // If neither has demand, remains in PH_ALLRED_1 until a call arrives.
    END_IF""", "Listing 6.3 &mdash; No wasted cycle through a phase nobody is waiting on.")))

story.append(KeepTogether([subhead("6.4 &nbsp; Emergency preemption, with the pedestrian guard")] + code_block(
"""IF Alarm_PreemptionActive AND (CurrentPhase <> PH_PREEMPT_TRANSITION)
   AND (CurrentPhase <> PH_PREEMPT_HOLD) THEN
    PreemptDirection_IsNS := EVP_Requested_NS;
    IF PedActiveThisPhase THEN
        ; // Never cut a pedestrian clearance interval short, even for an emergency vehicle
    ELSE
        ReturnPhaseAfterPreempt := CurrentPhase;
        CurrentPhase := PH_PREEMPT_TRANSITION;
        T_Clearance(IN := TRUE, PT := YellowTime_PT + AllRedTime_PT);
    END_IF
END_IF""", "Listing 6.4 &mdash; The transition begins only once any active pedestrian clearance has completed.")))
story.append(PageBreak())


story += chapter_head(7, "HMI Design &amp; the Live Intersection Map")
story.append(P(
    "The HMI mockup (<b>hmi/index.html</b> in the repository) is a top-down view of the "
    "intersection itself: roads, crosswalks, animated cars, in-pavement loop pads that "
    "light up when a car sits on them, and signal heads reflecting the live phase - "
    "matching what a traffic management centre operator would expect to see for a single "
    "monitored intersection.", body))
story += full_image(IMG_HMI,
    "Figure 7.1 &mdash; NS serving traffic: the NS signal heads show green, EW shows red "
    "with an EW car waiting on its loop pad (lit cyan) and its wait register accumulating "
    "in the side panel.", max_h_mm=92)
story.append(subhead("Design decisions"))
story += bullets([
    "<b>Amber on dark asphalt</b> &mdash; a seventh distinct visual identity in this "
    "portfolio, deliberately built around real traffic-signal red/amber/green on a neutral "
    "grey-black rather than another tinted \"console\" palette, since the signal colours "
    "themselves are the subject matter.",
    "<b>The loop pads are shown, not hidden</b> &mdash; dashed cyan outlines that fill "
    "when occupied, making the actuation mechanism visible rather than an invisible "
    "input behind the signal heads.",
    "<b>Cars actually stop and go</b> &mdash; each approach's cars queue at the stop "
    "line on red and proceed on green, so the loop pad occupancy and the demand registers "
    "are produced by the simulation rather than faked independently.",
    "<b>An emergency preemption event is scripted into the demo</b> &mdash; so the "
    "all-red transition and hold-green recovery from Chapter 5.4 is something a viewer "
    "sees happen, not just a line in the documentation.",
])
story.append(PageBreak())

story += chapter_head(8, "Alarm Philosophy &amp; Fail-Safe Design")
story.append(P(
    "This controller carries a single alarm deliberately - a signal controller's real "
    "safety envelope is enforced by what it structurally refuses to do, not by a long "
    "list of annunciated conditions an operator might miss.", body))
story.append(data_table(
    ["Condition", "Meaning", "Expected Response"],
    [["Alarm_PreemptionActive", "An emergency vehicle has requested right-of-way",
      "Informational - system self-manages; confirm it clears once the vehicle has passed"]],
    col_widths=[50 * mm, 62 * mm, AVAIL_W - 50 * mm - 62 * mm]))
story.append(Spacer(1, 10))
story.append(subhead("Fail-safe defaults, summarised"))
story += bullets([
    "System disabled &rarr; the sequencer forces <code>PH_ALLRED_1</code> immediately, "
    "rather than holding whichever green was last active.",
    "Minimum green and pedestrian clearance are checked <i>before</i> any early-termination "
    "reason, so no efficiency feature can shorten a green below its safety floor.",
    "Preemption transitions through all-red and recovers through all-red - it never "
    "switches directly from one green to the other.",
])
story.append(PageBreak())

story += chapter_head(9, "Testing, Commissioning &amp; FAT Procedures")
story.append(P(
    "The function block was validated against twelve functional test cases, anchored by "
    "one test specifically proving the fairness override fires inside a green's normal "
    "operating range. The full procedure is in <b>docs/Testing_Procedures.md</b>; the "
    "matrix is reproduced below.", body))
story.append(data_table(
    ["#", "Test Case", "Expected Result"],
    [
        ["1", "Minimum green enforced", "Green holds until MinGreen_PT regardless of demand loss"],
        ["2-3", "Gap-out and vehicle extension", "Gap expires with no actuation; a new actuation resets it"],
        ["4", "Maximum green is a hard ceiling", "Green ends at the ceiling despite continuous demand"],
        ["5", "Rest instead of cycling an empty phase", "Returns to the active side rather than serving an empty one"],
        ["6", "Longest-wait fairness override", "A busy green ends early once the other side's wait crosses the ceiling"],
        ["7", "Pedestrian clearance cannot be cut short", "Phase holds until the clearance timer completes"],
        ["8-9", "EVP interrupts; still respects ped clearance", "Transitions via all-red; waits out an active pedestrian interval"],
        ["10", "Preemption recovery", "Returns via all-red, not directly to a green"],
        ["11", "Simultaneous EVP requests", "NS takes priority per the defined order"],
        ["12", "System disable", "Forces a safe all-red"],
    ],
    col_widths=[12 * mm, 66 * mm, AVAIL_W - 12 * mm - 66 * mm]))
story.append(Spacer(1, 10))
story += callout(
    "Why Test 6 is the one that demonstrates \"intelligence\"",
    "Tests 1 through 4 describe a conventional actuated signal - genuinely useful, but not "
    "distinct from any standard traffic cabinet controller. Test 6 is where the longest-"
    "wait registers do something a plain gap-out/max-green controller wouldn't: cut a "
    "green short, inside its normal operating range, specifically because the other "
    "direction's accumulated wait crossed a fairness threshold.", "warning")
story.append(PageBreak())

story += chapter_head(10, "Limitations, Real-World Deltas &amp; Future Work")
story.append(P(
    "Naming the gap between a strong simulation and a certifiable traffic signal "
    "controller is part of the engineering, consistent with every other project in this "
    "portfolio.", body))
story.append(subhead("What a real installation would add"))
story += bullets([
    "<b>An independent hardware conflict monitor</b> &mdash; a separate safety device "
    "that forces a flashing state on any conflicting-green fault, entirely independent "
    "of this software.",
    "<b>A full NEMA dual-ring, multi-phase structure</b> &mdash; protected left turns, "
    "overlaps, and concurrent phase timing this two-phase scope deliberately omits "
    "(Chapter 2).",
    "<b>Calculated yellow and all-red intervals</b> &mdash; derived per ITE guidance from "
    "actual approach speed and geometry rather than fixed illustrative defaults.",
    "<b>Detector fault handling</b> &mdash; a stuck-on or dead loop is a real, common "
    "failure mode; this project assumes its detectors report truthfully.",
])
story.append(subhead("10.1 &nbsp; Hazard &amp; safeguard register (HAZOP-style)"))
story.append(data_table(
    ["Hazard", "Cause", "Safeguard in This Design"],
    [
        ["Conflicting greens shown simultaneously", "A logic or output fault", "Named gap - requires an independent hardware conflict monitor"],
        ["Pedestrian struck during a cut-short phase", "An efficiency feature shortening green below clearance", "Pedestrian clearance gates every early-termination reason"],
        ["Cross-street starvation", "A steady stream resetting the gap timer indefinitely", "Longest-wait fairness override plus a hard maximum green"],
        ["Stuck detector holding a green forever", "A failed loop reporting permanent occupancy", "Named gap - maximum green bounds the damage, but detector fault detection is not modelled"],
    ],
    col_widths=[46 * mm, 52 * mm, AVAIL_W - 46 * mm - 52 * mm]))
story.append(Spacer(1, 8))
story.append(subhead("Where this project could go next"))
story += bullets([
    "Extend to a full dual-ring structure with protected left-turn phases.",
    "Add detector fault detection (a loop that never clears, or never actuates).",
    "Coordinate two adjacent intersections with a shared offset, rather than treating "
    "each as an isolated controller.",
])
story.append(PageBreak())


# ---- Appendix A: I/O Quick Reference ---------------------------------------
story += chapter_head("A", "Appendix A &mdash; I/O Quick Reference", "APPENDIX")
story.append(data_table(
    ["Tag", "Dir.", "Type", "Notes"],
    [
        ["DI_Loop_N / _S / _E / _W", "IN", "BOOL x4", "Per-approach loop"],
        ["DI_PedCall_NS / DI_PedCall_EW", "IN", "BOOL x2", "Pedestrian calls"],
        ["DI_EVP_N / _S / _E / _W", "IN", "BOOL x4", "Preemption requests"],
        ["DI_System_Enable", "IN", "BOOL", "Master enable"],
        ["DO_NS_Green / Yellow / Red", "OUT", "BOOL x3", "NS signal head"],
        ["DO_EW_Green / Yellow / Red", "OUT", "BOOL x3", "EW signal head"],
        ["DO_NS_WalkSignal / DO_EW_WalkSignal", "OUT", "BOOL x2", "Pedestrian WALK"],
        ["CurrentPhase", "OUT", "ENUM", "8-state sequencer"],
        ["WaitTime_NS_s / WaitTime_EW_s", "OUT", "REAL x2", "Longest-wait registers"],
        ["Alarm_PreemptionActive", "OUT", "BOOL", "EVP in progress"],
        ["SystemStatus", "OUT", "STRING", "HMI display"],
    ],
    col_widths=[66 * mm, 14 * mm, 24 * mm, AVAIL_W - 66 * mm - 14 * mm - 24 * mm]))
story.append(PageBreak())

# ---- Appendix B: Full ST Listing (read directly from the repo source) -----
story += chapter_head("B", "Appendix B &mdash; Full Structured Text Listing", "APPENDIX")
story.append(P(
    "Complete, unedited listing of <b>src/Traffic_Intersection_Control.st</b>, read "
    "directly from the repository source so this appendix cannot drift from the code.", body))

ST_PATH = os.path.join(HERE, "..", "src", "Traffic_Intersection_Control.st")
with open(ST_PATH, "r", encoding="utf-8") as f:
    st_lines = f.read().rstrip("\n").split("\n")

chunks, cur = [], []
for ln in st_lines:
    cur.append(ln)
    if (len(cur) >= 36 and ln.strip() == "") or len(cur) >= 44:
        chunks.append(cur); cur = []
if cur:
    chunks.append(cur)

for idx, ch in enumerate(chunks):
    cap = ("Listing B.1 &mdash; FB_Traffic_Intersection_Control source (part %d of %d)."
           % (idx + 1, len(chunks)))
    story += code_block("\n".join(ch), cap)
story.append(PageBreak())

# ---- Appendix C: Glossary --------------------------------------------------
story += chapter_head("C", "Appendix C &mdash; Glossary", "APPENDIX")
story.append(data_table(
    ["Term", "Meaning"],
    [
        ["Actuated signal", "A signal whose timing responds to real-time detector input"],
        ["Fixed-time signal", "A signal running a pre-set cycle regardless of conditions"],
        ["Minimum green", "The shortest green any phase may show once started"],
        ["Maximum green", "A hard ceiling on green duration regardless of demand"],
        ["Gap / vehicle extension", "A timer restarted by each vehicle actuation, extending the green"],
        ["Gap-out", "Ending a green when the gap timer expires with no new actuation"],
        ["All-red", "A short interval where every approach shows red, clearing the intersection"],
        ["EVP", "Emergency Vehicle Preemption"],
        ["Loop detector", "An in-pavement wire loop that senses a vehicle's presence by inductance change"],
        ["Conflict monitor", "An independent hardware device forcing a safe flash on any conflicting-green fault"],
        ["NEMA / ITE", "Traffic control equipment standard / transportation engineering guidance body"],
    ],
    col_widths=[40 * mm, AVAIL_W - 40 * mm]))
story.append(PageBreak())

# ---- About the Author -------------------------------------------------------
story += chapter_head("&mdash;", "About the Author", "CLOSING")
story.append(P(
    "<b>Sipho Lucky Sibanda</b> is an automation and controls engineer building a "
    "multi-disciplinary portfolio spanning marine systems, avionics, architectural "
    "technology, applied AI, biotechnology, electrical power systems, civil "
    "transportation, and industrial automation. This manual documents the sixth "
    "deliberate discipline shift in that portfolio, following the same documentation "
    "standard as every other project in the series: full logic, I/O documentation, a "
    "live HMI, functional test procedures, and an honest account of what separates a "
    "strong simulation from a certifiable production system.", lead))
story.append(P("Repository: <b>traffic-adaptive-utms</b>", body))
story.append(Spacer(1, 20))
story.append(HRFlowable(width="40%", thickness=1, color=AMBERACC))
story.append(Spacer(1, 6))
story.append(P("End of document.", caption))

doc = SimpleDocTemplate(
    OUTFILE, pagesize=A4,
    leftMargin=MARGIN_L, rightMargin=MARGIN_R,
    topMargin=MARGIN_TOP, bottomMargin=MARGIN_BOT,
    title="Adaptive Urban Traffic Management System - Technical Manual",
    author=AUTHOR,
)
doc.build(story, onFirstPage=draw_cover, onLaterPages=draw_body)
print("Built:", OUTFILE)
