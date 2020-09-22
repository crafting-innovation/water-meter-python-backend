from fpdf import FPDF
import os
os.chdir(r'C:\Users\user\Desktop\update_table')
def add_image(image_path,imagepath1):
    pdf = FPDF()
    pdf.add_page()
    pdf.image(imagepath1, x=-3, y=0, w=220,h=28)
    pdf.image(image_path, x=57, y=0, w=95)
    pdf.set_font("Arial", size=8)
    pdf.ln(30)
    txt = "Diamond District Office Building, HAL Old, Airport Rd, ISRO Colony, Kodihalli, Bengaluru, Karnataka 560017"
    pdf.cell(0, 10, txt=txt, ln=1, align="C")
    pdf.set_font("Arial", size=14,style='B')
    pdf.ln(1)
    pdf.cell(180, 10, txt="Crafting Innovation Water Service Statement", ln=1, align="R")
    pdf.set_line_width(1)
    pdf.set_draw_color(26, 214, 32)
    pdf.line(70, 70, 200, 70)
    pdf.set_font("Arial", size=12,style='B')
    pdf.cell(180, 10, txt="Statement Summary",  align="R")
    pdf.ln(8)
    pdf.set_font("Arial", size=7,style='B')
    pdf.cell(180, 10, txt="Billing Address : {}".format('Salarpuria sattava Outer ring road Marathalli sector 2 Bengaluru - 560098'),  align="R")
    pdf.ln(5)
    pdf.set_font("Arial", size=10,style='B')
    pdf.cell(180, 10, txt="Statement Date : {}".format('26-5-2020'),  align="R")
    pdf.ln(5)
    pdf.cell(180, 10, txt="Statement Number : {}".format('Salarpuria-4-2020'),  align="R")
    pdf.ln(5)
    pdf.cell(180, 10, txt="Total Bill amount : Rs. {}".format('2823822'),  align="R")
    pdf.ln(5)
    pdf.cell(180, 10, txt="Billing Duration : {}".format('1-4-2020 to 30-4-2020'),  align="R")
    pdf.ln(13)
    pdf.set_font("Arial", size=8,style='B')
    pdf.cell(80, 10, txt="Greetings from Crafting Innovation Private Ltd. We are writing to provide you with an summary of water usage for all residents of your apartment." ,  align="L")
    pdf.ln(3)
    pdf.cell(80, 10, txt="In case of any queries feel free to contact us to help us serve you better" ,  align="L")
    pdf.ln(15)
    header = [['Flat', 'Consumption', 'Usage charges', 'Tax','Total','Invoice No.']]
    pdf.set_line_width(0.5)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_font("Arial", size=9,style='B')
    pdf. set_text_color(26, 214, 32)
    col_width = pdf.w / 8.3
    invoice_col_width = pdf.w/3
    row_height = pdf.font_size+2
    for row in header:
        count=0
        for item in row:
            count = count+1
            if count==6:
                pdf.cell(invoice_col_width, row_height*1,
                     txt=item, border=1)
            else:
                pdf.cell(col_width, row_height*1,
                     txt=item, border=1)      
        pdf.ln(row_height*1)
    pdf.ln(3)
    data = [['First Name', 'Last Name', 'email', 'zip','abcde','salarpuriaW1101-4-2020'],
            ['Mike', 'Driscoll', 'mike@somewhere.com', '55555','abcde','salarpuriaW1101-4-2020']          
            ]
    pdf.set_line_width(0.5)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_font("Arial", size=8)
    pdf. set_text_color(0, 0, 0)
    col_width = pdf.w / 8.3
    invoice_col_width = pdf.w/3
    row_height = pdf.font_size+5
    for row in data:
        count=0
        for item in row:
            count = count+1
            if count==6:
                pdf.cell(invoice_col_width, row_height*1,
                     txt=item, border=1)
            else:
                pdf.cell(col_width, row_height*1,
                     txt=item, border=1)      
        pdf.ln(row_height*1)
    pdf.output("add_image.pdf")
    
if __name__ == '__main__':
    add_image('Crafting Innovation _logo (1).jpg','footer.jpg')
