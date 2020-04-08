from PIL import Image


def get_concat_v(image1, image2):
    btn1 = Image.open(image1)
    btn2 = Image.open(image2)
    dst = Image.new('RGB', (btn1.width, btn1.height + btn2.height))
    dst.paste(btn1, (0, 0))
    dst.paste(btn2, (0, btn1.height))
    return dst


"""
input_file = PdfFileReader(open('test1.pdf', 'rb'))
output = PdfFileWriter()
page_count = input_file.getNumPages()

for page_number in range(input_file.getNumPages()):
    page = input_file.getPage(page_number)
    page.mediaBox.lowerLeft = (page.mediaBox.getLowerLeft_x(), 20)
    output.addPage(page)

output_stream = open('output.pdf', 'wb')
output.write(output_stream)
"""
