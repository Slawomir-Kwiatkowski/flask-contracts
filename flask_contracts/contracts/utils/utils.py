from base64 import decode
from io import BytesIO
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table
from reportlab.pdfgen.canvas import Canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from barcode import EAN13
from barcode.writer import ImageWriter


def create_pdf(booking_no,
                contractor,
                contractor_no,
                truck_plate,
                warehouse,
                date,
                time,
                pallets_pos,
                pallets,
                app_path):
    buffer = BytesIO()
    canvas = Canvas(buffer, pagesize=A4)
    WIDTH, HEIGHT = A4
    MARIGIN = 1.5 * cm
    canvas.translate(MARIGIN, HEIGHT-MARIGIN)
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
    pdfmetrics.registerFont(TTFont('Verabd', 'Verabd.ttf'))
    

    # header
    canvas.setFont("Verabd", size=14)
    canvas.drawString(160, 0, "Reservation confirmation")
    canvas.setFont("Vera", size=10)
    canvas.drawString(430, -0.9*cm, "Flask-Contracts")
    canvas.setStrokeGray(0)
    canvas.line(0, -1*cm, WIDTH - 2*MARIGIN, -1*cm)

    # footer
    canvas.drawString(0, -26.2*cm, "\u00A9 2021 S. Kwiatkowski")
    canvas.drawString(430, -26.5*cm, "Flask-Contracts")
    canvas.line(0, -26.6*cm, WIDTH - 2*MARIGIN, -26.6*cm)


    # barcode
    my_code = EAN13(str(booking_no).zfill(12), writer=ImageWriter())
    image = my_code.render()
    im = ImageReader(image)
    canvas.drawImage(im, x=0, y=-5*cm, width=150, height=100)

    # paragraphs
    txt_obj = canvas.beginText(14, -6.5* cm)
    txt_obj.setFont("Vera", 12)
    txt_obj.setWordSpace(3)
    txt_lst = ["Booking information", 
                "Booking no.: " + str(booking_no),
                "Contractor: " + contractor,
                "Truck plate no.: " + truck_plate,
                "Warehouse: " + warehouse,
                f"Date and time of booking: {date} {time}",
                 " ", 
                "Drivers are asked for:", 
                "1. Providing the booking number or presenting the booking report for ",
                "   the entrance guardhouse.",
                "2. Providing the guard with the telephone number, name and surname", 
                "   and registration number of the vehicle in the case where these data",
                "   have not been completed before the transport arrives at the warehouse.", 
                "3. Reporting to the office 30 minutes before the booked time slot.", " ",
                "   In the event of a delayed arrival and or failure to comply with any of ",
                "the above provisions, it will be effective the reservation of the time slot ",
                "is forfeited."]
    for line in txt_lst:
        txt_obj.textOut(line)
        txt_obj.moveCursor(0, 16)
    canvas.drawText(txt_obj)

    # summary table
    canvas.setFont("Verabd", size=14)
    canvas.drawString(0, -19.5*cm, "SUMMARY:")
    table_data = [['Booking no.', 'Contractor', 'Contractor no.', 'Pallets pos.', 'Pallets'],
                [booking_no, contractor, contractor_no, pallets_pos, pallets]]
    t = Table(table_data, colWidths=[60, 230, 70, 60, 50], rowHeights=30)
    style = [('BACKGROUND',(0,0),(-1,-2),colors.lightblue),
            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]
    t.setStyle(tblstyle=style)
    t.wrapOn(canvas, 10, 10)
    t.drawOn(canvas=canvas, x=20, y=-22*cm)

    canvas.showPage()
    canvas.save()
    return buffer

