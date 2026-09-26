import re

from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# Register Unicode font
pdfmetrics.registerFont(
    TTFont("DejaVuSans", "DejaVuSans.ttf")
)


def clean_text(text):

    text = text.replace("**", "")

    text = re.sub(
        r"<br\s*/?>",
        " - ",
        text
    )

    text = text.replace("|", " ")

    text = text.replace("•", "-")

    text = text.replace("–", "-")

    text = text.replace("—", "-")

    text = text.replace("&", "&amp;")

    text = re.sub(
        r"^\s*\*[-|:]+\s*\*$",
        "",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def create_pdf(
    current_location,
    destination,
    days,
    budget,
    interests,
    travel_plan
):

    filename = f"{destination}_travel_plan.pdf"

    document = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Use Unicode font for all PDF styles
    styles["Normal"].fontName = "DejaVuSans"
    styles["Heading2"].fontName = "DejaVuSans"
    styles["Heading3"].fontName = "DejaVuSans"
    styles["Title"].fontName = "DejaVuSans"

    title_style = styles["Title"]

    title_style.alignment = TA_CENTER

    content = []

    # TITLE
    content.append(
        Paragraph(
            "TRAVEL PLAN",
            title_style
        )
    )

    content.append(
        Spacer(1, 15)
    )

    # TRIP DETAILS
    content.append(
        Paragraph(
            "Trip Details",
            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 8)
    )

    details = [
        f"<b>Starting Location:</b> {current_location}",
        f"<b>Destination:</b> {destination}",
        f"<b>Number of Days:</b> {days}",
        f"<b>Budget:</b> {budget}",
        f"<b>Interests:</b> {interests}"
    ]

    for detail in details:

        content.append(
            Paragraph(
                detail,
                styles["Normal"]
            )
        )

        content.append(
            Spacer(1, 5)
        )

    content.append(
        Spacer(1, 15)
    )

    # TRAVEL PLAN
    content.append(
        Paragraph(
            "Detailed Travel Plan",
            styles["Heading2"]
        )
    )

    content.append(
        Spacer(1, 10)
    )

    lines = travel_plan.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Skip markdown table separator lines
        if re.match(
            r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?$",
            line
        ):
            continue

        # Detect headings before cleaning
        if line.startswith("###"):

            line = line.replace(
                "###",
                ""
            ).strip()

            line = clean_text(line)

            if line:

                content.append(
                    Paragraph(
                        line,
                        styles["Heading3"]
                    )
                )

        elif line.startswith("##"):

            line = line.replace(
                "##",
                ""
            ).strip()

            line = clean_text(line)

            if line:

                content.append(
                    Paragraph(
                        line,
                        styles["Heading2"]
                    )
                )

        else:

            line = clean_text(line)

            if line:

                content.append(
                    Paragraph(
                        line,
                        styles["Normal"]
                    )
                )

        content.append(
            Spacer(1, 5)
        )

    # BUILD PDF
    document.build(content)

    return filename

