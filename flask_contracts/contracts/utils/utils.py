from io import BytesIO
from flask_sqlalchemy.model import camel_to_snake_case
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Table
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from barcode import EAN13
from barcode.writer import ImageWriter, SIZE

def get_my_pdf():
    buffer = BytesIO()
    canvas = Canvas(buffer, pagesize=A4)
    WIDTH, HEIGHT = A4
    MARIGIN = 1.5 * cm
    canvas.translate(MARIGIN, HEIGHT-MARIGIN)

    # header
    canvas.drawString(200, 0, "Reservation confirmation")
    canvas.setFont("Times-Roman", size=10)
    canvas.drawString(455, -0.9*cm, "Flask-Contracts")
    canvas.setStrokeGray(0)
    canvas.line(0, -1*cm, WIDTH - 2*MARIGIN, -1*cm)

    # footer
    canvas.drawString(0, -26.5*cm, "\u00A9 2021 S. Kwiatkowski")
    canvas.drawString(455, -26.9*cm, "Flask-Contracts")
    canvas.line(0, -27*cm, WIDTH - 2*MARIGIN, -27*cm)


    # barcode
    number = '123456789123'
    my_code = EAN13(number, writer=ImageWriter())
    image = my_code.render()
    im = ImageReader(image)
    canvas.drawImage(im, x=0, y=-4*cm, width=120, height=75)

    # paragraphs
    txt_obj = canvas.beginText(14, -6.5* cm)
    txt_obj.setFont("Times-Roman", 12)
    txt_lst = ["Booking information", "Booking no.:", "Contractor:", "Truck plate no.:",
                "Warehouse:","Date and time of booking:", " ", "Drivers are asked for:", 
                "1. Providing the booking number or presenting the booking report for the entrance guardhouse.",
                "2. Providing the guard with the telephone number, name and surname and registration number of",
                "    the vehicle in the case where these data have not been completed before the transport arrives at", 
                "    the warehouse.",
                "3.Reporting to the office 30 minutes before the booked time slot.", " ",
                "In the event of a delayed arrival and or failure to comply with any of the above provisions,",
                " it will be effective the reservation of the time slot is forfeited."]
    for line in txt_lst:
        txt_obj.textOut(line)
        txt_obj.moveCursor(0 ,16)
    canvas.drawText(txt_obj)

    # summary table
    canvas.setFont("Times-Roman", size=14)
    canvas.drawString(0, -20*cm, "SUMMARY:")
    table_data = [['Booking no.', 'Contractor', 'Contractor no.', 'Pallets pos.', 'Pallets'],
                ['1', 'Test', '2', '3', '4']]
    t = Table(table_data)
    style = [('BACKGROUND',(0,0),(-1,-2),colors.lightblue),
            ('ALIGN',(0,-1),(-1,-1),'CENTER'),
            ('BOX', (0,0), (-1,-1), 0.25, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),]
    t.setStyle(tblstyle=style)
    t.wrapOn(canvas, 10, 10)
    t.drawOn(canvas=canvas, x=20, y=-22*cm)

    canvas.showPage()
    canvas.save()
    return buffer

