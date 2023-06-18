from PIL import Image, ImageDraw, ImageFont
import time
import textwrap

'''
A method to generate the title for img based on time.
'''
def title():
    localtime = time.localtime(time.time())
    name = '%d-%d-%d-%d-%d-%d' % (
        localtime[0], localtime[1], localtime[2], localtime[3], localtime[4], localtime[5])

    return name

'''
Convert a sentence to img.
White background, centered, wrap automatically.
Based on https://code-maven.com/create-images-with-python-pil-pillow
'''
def convert_text(sentence, max_font_size, name):
    image_width = 1280
    image_height = 800

    img = Image.new('RGB', (image_width, image_height), color='white')
    draw = ImageDraw.Draw(img)

    font_size = max_font_size
    font = ImageFont.truetype("Roboto-Black.ttf", font_size)

    while True:
        wrapped_text = textwrap.wrap(sentence, width=int(image_width / font_size))

        total_text_height = len(wrapped_text) * font.getsize('hg')[1]
        if total_text_height <= image_height:
            break

        font_size -= 1
        font = ImageFont.truetype("Roboto-Black.ttf", font_size)

    y = (image_height - total_text_height) // 2

    for line in wrapped_text:
        text_width, text_height = draw.textsize(line, font)
        x = (image_width - text_width) // 2
        draw.text((x, y), line, font=font, fill='black')
        y += text_height

    img.save('img/' + name + '.png')


