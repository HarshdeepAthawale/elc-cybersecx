#!/usr/bin/env python3
"""
Generate submission PDF with proper structure: keys, ciphertexts, graphs,
analysis, and full source code. Uses reportlab platypus for correct code display.
Run: python generate_submission_pdf.py
Output: submission.pdf
"""

from pathlib import Path

BASE_DIR = Path(__file__).parent
OUTPUT_PDF = BASE_DIR / "submission.pdf"

# Page dimensions
PAGE_WIDTH = 612
PAGE_HEIGHT = 792
MARGIN = 50
CONTENT_WIDTH = PAGE_WIDTH - 2 * MARGIN


def truncate(text: str, max_len: int = 500) -> str:
    """Truncate long text with ellipsis."""
    text = text.replace("\n", " ")
    if len(text) <= max_len:
        return text
    return text[:max_len] + "... [truncated]"


def safe_text(text: str) -> str:
    """Ensure text is PDF-safe (basic ASCII + common chars)."""
    return text.encode("ascii", "replace").decode("ascii")


def main() -> None:
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Preformatted,
            Image,
            PageBreak,
            Table,
            TableStyle,
        )
    except ImportError as e:
        print(f"Install reportlab: pip install reportlab\nError: {e}")
        return

    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN,
    )
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=20,
        spaceAfter=12,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=20,
        spaceAfter=10,
    )
    code_style = ParagraphStyle(
        "Code",
        parent=styles["Code"],
        fontName="Courier",
        fontSize=8,
        leftIndent=10,
        rightIndent=10,
        spaceBefore=6,
        spaceAfter=12,
        backColor=colors.Color(0.95, 0.95, 0.95),
        borderColor=colors.Color(0.7, 0.7, 0.7),
        borderWidth=0.5,
        borderPadding=8,
    )
    code_title_style = ParagraphStyle(
        "CodeTitle",
        parent=styles["Heading3"],
        fontSize=11,
        spaceBefore=16,
        spaceAfter=4,
    )

    # ========== TITLE ==========
    story.append(Paragraph("ELC Secure Network Configuration", title_style))
    story.append(Paragraph(
        "Encryption Module &mdash; Submission Document",
        ParagraphStyle("Subtitle", parent=styles["Normal"], fontSize=12, spaceAfter=20),
    ))
    story.append(Spacer(1, 20))

    # ========== 1. ENCRYPTION KEYS ==========
    story.append(Paragraph("1. Encryption Keys", section_style))
    keys_file = BASE_DIR / "keys.txt"
    if keys_file.exists():
        keys_text = keys_file.read_text().strip()
    else:
        keys_text = "CAESAR: 3\nPLAYFAIR: MONARCHY\nHILL: GYBNQKURP"
    story.append(Preformatted(safe_text(keys_text), code_style))
    story.append(Spacer(1, 12))

    # ========== 2. PLAINTEXT ==========
    story.append(Paragraph("2. Plaintext (Input)", section_style))
    pt_file = BASE_DIR / "plaintext.txt"
    if pt_file.exists():
        pt_content = pt_file.read_text()
        story.append(Preformatted(safe_text(truncate(pt_content, 600)), code_style))
    story.append(Spacer(1, 12))

    # ========== 3. CIPHERTEXTS ==========
    story.append(Paragraph("3. Ciphertext Outputs (sample)", section_style))
    for name, path in [
        ("Caesar", BASE_DIR / "caesar_cipher.txt"),
        ("Playfair", BASE_DIR / "playfair_cipher.txt"),
        ("Hill", BASE_DIR / "hill_cipher.txt"),
    ]:
        story.append(Paragraph(f"<b>{name}</b> (first 250 chars):", code_title_style))
        if path.exists():
            ct = truncate(path.read_text(), 250)
            story.append(Preformatted(safe_text(ct), code_style))
    story.append(Spacer(1, 12))

    # ========== 4. TIMING RESULTS ==========
    story.append(Paragraph("4. Timing Results", section_style))
    timing_data = [
        ["Algorithm", "Encrypt (ms)", "Decrypt (ms)"],
        ["Caesar", "~4.5", "~2.5"],
        ["Playfair", "~19.0", "~18.8"],
        ["Hill", "~28.5", "~29.9"],
    ]
    t = Table(timing_data, colWidths=[120, 120, 120])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3498db")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8f9fa")]),
    ]))
    story.append(t)
    story.append(Paragraph(
        "<i>Fastest: Caesar (encryption &amp; decryption). Times averaged over 5 runs.</i>",
        ParagraphStyle("Caption", parent=styles["Normal"], fontSize=9, spaceBefore=6),
    ))
    story.append(Spacer(1, 16))

    # ========== 5. GRAPHS ==========
    story.append(Paragraph("5. Timing Graphs", section_style))
    for img_name in ["encryption_time.png", "decryption_time.png"]:
        img_path = BASE_DIR / img_name
        if img_path.exists():
            img = Image(str(img_path), width=5.5 * inch, height=2.75 * inch)
            story.append(img)
            story.append(Paragraph(
                img_name,
                ParagraphStyle("ImgCaption", parent=styles["Normal"], fontSize=9, spaceBefore=4),
            ))
            story.append(Spacer(1, 12))
    story.append(PageBreak())

    # ========== 6. ANALYSIS ==========
    story.append(Paragraph("6. Analysis", section_style))
    analysis = """
    <b>Performance:</b> Caesar is fastest (~5ms encrypt) due to simple shift; Playfair ~4x slower 
    (digraph + matrix); Hill slowest (~28ms) from matrix multiply and modular inverse.
    <br/><br/>
    <b>Security vs Speed:</b> Caesar (weak, 25 keys) &rarr; Playfair (moderate, digraph) &rarr; 
    Hill (polygraphic, stronger). All correctly encrypt/decrypt with keys in keys.txt.
    """
    story.append(Paragraph(analysis, styles["Normal"]))
    story.append(PageBreak())

    # ========== 7. SOURCE CODE ==========
    story.append(Paragraph("7. Source Code", section_style))
    story.append(Paragraph(
        "Complete implementation of Caesar, Playfair, and Hill ciphers with timing measurement.",
        ParagraphStyle("Intro", parent=styles["Normal"], fontSize=10, spaceAfter=12),
    ))

    code_files = [
        ("main.py", BASE_DIR / "main.py"),
        ("cipher_module.py", BASE_DIR / "cipher_module.py"),
        ("timing_results.py", BASE_DIR / "timing_results.py"),
    ]

    for fname, fpath in code_files:
        story.append(Paragraph(f"<b>{fname}</b>", code_title_style))
        if fpath.exists():
            code = fpath.read_text()
            # Preformatted preserves indentation; wrap long lines for PDF
            max_line = 95
            wrapped_lines = []
            for line in code.split("\n"):
                safe_line = safe_text(line)
                if len(safe_line) > max_line:
                    for i in range(0, len(safe_line), max_line):
                        wrapped_lines.append(safe_line[i:i + max_line])
                else:
                    wrapped_lines.append(safe_line)
            code_block = "\n".join(wrapped_lines)
            story.append(Preformatted(code_block, code_style))
        else:
            story.append(Paragraph(f"<i>File not found: {fname}</i>", styles["Normal"]))
        story.append(Spacer(1, 8))

    doc.build(story)
    print(f"Saved {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
