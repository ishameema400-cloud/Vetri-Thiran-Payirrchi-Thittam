import os
from datetime import datetime
from fpdf import FPDF

EXPORT_FOLDER = "static/exports"

def save_pdf(layout: list) -> str:
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Helvetica', '', 12)

    for panel in layout:
        image_path = panel['image_path']
        story_text = panel['text']

        pdf.add_page()

        # Panel Title
        pdf.set_font('Helvetica', 'B', 14)
        pdf.cell(0, 10, f"Panel {panel['panel']}: {panel['title']}", ln=True, align="C")
        pdf.set_font('Helvetica', '', 11)

        # Image Placement
        y_image = 30
        image_height = 100
        spacing_after_image = 15

        if os.path.exists(image_path):
            pdf.image(image_path, x=35, y=y_image, w=140, h=image_height)
        else:
            pdf.set_y(y_image)
            pdf.multi_cell(0, 10, f"Image missing: {image_path}")

        # Text Placement
        pdf.set_y(y_image + image_height + spacing_after_image)

        if panel.get('scene_description'):
            pdf.set_font('Helvetica', 'I', 10)
            pdf.multi_cell(0, 6, f"Scene: {panel['scene_description']}")
            pdf.ln(3)

        pdf.set_font('Helvetica', '', 11)
        story_lines = story_text.strip().splitlines()
        cleaned_text = "\n".join(story_lines).strip()
        safe_text = cleaned_text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 6, safe_text)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"comic_{timestamp}.pdf"
    pdf_path = os.path.join(EXPORT_FOLDER, filename)
    pdf.output(pdf_path)

    return pdf_path