from flask import Flask, render_template, request, send_file
from rembg import remove
from io import BytesIO
import base64

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if file is uploaded
        if 'image' not in request.files:
            return render_template('index.html', error='No image uploaded')
            
        file = request.files['image']
        
        # Validate file
        if file.filename == '':
            return render_template('index.html', error='No selected file')
            
        if not allowed_file(file.filename):
            return render_template('index.html', error='Invalid file type')

        try:
            # Process image
            input_image = file.read()
            output_image = remove(input_image)
            
            # Convert to base64 for displaying in HTML
            processed_image = base64.b64encode(output_image).decode('utf-8')
            
            return render_template('index.html', 
                                 processed_image=processed_image,
                                 original_name=file.filename)
            
        except Exception as e:
            return render_template('index.html', error=str(e))
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
