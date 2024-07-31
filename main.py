from nicegui import ui, events
from PIL import Image
from io import BytesIO
import os

class ImageHandler:
    def __init__(self):
        self.image = None
        self._dimensions = 'Image dimensions: 0x0'  # Default text
        self.istransparent = False

    def save_image(self):
        if self.image:
            output=BytesIO()
            self.image.save(output, format='PNG')
            output.seek(0)
            return output.getvalue()
        return None
        

    @property
    def dimensions(self):
        if self.image:
            width, height = self.image.size
            return f"Image dimensions: {width}x{height}"
        return self._dimensions

    def upload_image(self, e: events.UploadEventArguments):
        image_data = e.content.read()  # Read the binary data from the uploaded file
        self.image = Image.open(BytesIO(image_data))  # Open it with PIL

    def resize_image(self, size):
        if self.image:
            # self.image = self.image.resize((width, height), Image.LANCZOS)
            width, height = self.image.size
            if width > height:
                aspect_ratio = (width / height)
                new_height = size
                new_width = int(new_height * aspect_ratio)
            else:
                aspect_ratio = (height / width)
                new_width = size
                new_height = int(new_width * aspect_ratio)
            self.image = self.image.resize((new_width, new_height), Image.LANCZOS)
    
    def make_transparent(self):
        if self.image:
            img = self.image
            # Convert the image to RGBA if it isn't already
            img = img.convert("RGBA")

            # Get data of the image
            data = img.getdata()

            # List to hold new image's data
            new_data = []

            # Define the color we want to make transparent
            # In this case, it is pure white
            to_be_transparent = (255, 255, 255, 255)

            # Tolerance for color comparison
            tolerance = 10

            # Iterate through each pixel
            for item in data:
                # Change all white (also shades of whites)
                # pixels to transparent (white here, you can change as per the background color of your image)
                if all(i > 255 - tolerance for i in item[:3]):
                    new_data.append((255, 255, 255, 0))  # Making white pixels fully transparent
                else:
                    new_data.append(item)  # Other pixels remain unchanged

            # Update image data
            print('Making transparent')
            img.putdata(new_data)
            self.image = img
            self.istransparent = True
            print('Done making transparent', self.istransparent)

with ui.dialog() as error_dialog, ui.card():
            ui.label('Please enter a filename before downloading').classes('text-red-500')
            ui.button('Close', on_click=error_dialog.close).tailwind('bg-red-500 text-white')

def download_image():
    if filename_text.value:
        print('Downloading image')
        ui.download(handler.save_image(), filename=f'{filename_text.value}.png', media_type='image/png')
    else:
        print('Please enter a filename before downloading')
        error_dialog.open()

# Setup UI
handler = ImageHandler()  # Instantiate the image handler
with ui.column().classes('mx-auto w-full max-w-5xl p-4 bg-white shadow-md rounded-md'):
    ui.label('Image Editor') \
        .classes('text-2xl font-bold my-6 text-center w-full')

    with ui.column().classes('w-full'):
        ui.label('Upload an image to get started').classes('text-lg text-center w-full text-gray-600')
        ui.upload(on_upload=handler.upload_image).tailwind.width('w-1/3 mx-auto')

    ui.separator()

    with ui.row().classes('w-full mx-auto space-x-3 align-content-center flex justify-center'):
        ui.label('Image Operations').classes('text-lg font-bold text-center w-full')
        with ui.card():
            ui.button('Make Transparent', on_click=handler.make_transparent)
            ui.label('is now transparent!').bind_visibility_from(handler, 'istransparent') \
                .classes('text-green-500')  # Emphasize success state


        with ui.card().classes('mx-auto'): 
            ui.button('Resize', on_click=lambda: handler.resize_image(int(long_edge.value)))
            long_edge = ui.number(value=300, label='Long edge size')
    
    ui.separator()

    with ui.column().classes('w-full flex justify-center align-items-center'):
        ui.label('Image dimensions: 0x0').bind_text(handler, 'dimensions').classes('text-gray-600 text-center w-full')  # Softer text for secondary info
        viewer = ui.image().classes('w-96 mx-auto mt-4 border border-gray-300')  
        viewer.bind_source(handler, 'image')
        filename_text= ui.input(label='Enter filename').classes('mx-auto')
        ui.button('Download as PNG', on_click=download_image).tailwind.width('w-1/3 mx-auto')

port = int(os.getenv('PORT', 8080))

ui.run(port=port)
