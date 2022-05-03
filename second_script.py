from PIL import Image

form = Image.open("benefit.png")
img = Image.open("106044_benefit.jpg")

# Подгонка размеров изображения.
width, height = img.size

new_width = form.size[0] - 50
new_height = int(new_width * height / width)

while new_height > form.size[1] - 225:
    new_width = new_width - 5
    new_height = int(new_width * height / width)

img = img.resize((new_width, new_height))

# Подгонка координат для вставки.
paste_width = (form.size[0] - new_width) // 2
paste_height = (form.size[1] // 2 + 50) - new_height // 2

form.paste(img, (paste_width, paste_height))

form.save('res.png')

form.close()
img.close()
