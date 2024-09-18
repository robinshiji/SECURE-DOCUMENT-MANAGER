from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from .models import Document,ImageUpload
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import mimetypes
from .forms import DocumentForm,ImageUploadForm,EditProfileForm,UploadTextFileForm
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

#user registration 

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('loginview')

    return render(request, 'register.html')
          
#user login 
def loginview(request):
	
	if request.method == "POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		if not User.objects.filter(username=username).exists():
			messages.error(request, 'Invalid Username')
			return redirect('loginview')
		
		
		user = authenticate(username=username, password=password)
		
		if user is None:
			messages.error(request, "Invalid Password")
			return redirect('loginview')
		else:
			auth_login(request, user)
			return redirect('document')
	return render(request, 'login.html')

# for profile updation
@login_required(login_url='loginview')
def profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        
            return redirect('document')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

#upload file and store database and image folder[dynamic image handling]
@login_required(login_url='loginview')
def document(request):
    if request.method == 'POST':
        form= DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('viewdoc')  # or wherever you want to redirect
    else:
        form = DocumentForm()
    return render(request, 'document.html')

#viewing uploaded documents
@login_required(login_url='loginview')
def view_doc(request):
    documents = Document.objects.all()  # Retrieve all uploaded documents
    return render(request, 'document.html', {'documents': documents})

#downloading documents
@login_required(login_url='loginview')
def download(request, document_id):
    # Get the document from the database
    document = get_object_or_404(Document, id=document_id)

    # Get the file path and open the file
    file_path = document.file.path
    file_name = document.file.name

    # Guess the content type
    mime_type, _ = mimetypes.guess_type(file_path)

    # Open the file and send it as a response
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response

#deleting documents
@login_required(login_url='loginview')
def delete(request, document_id):
    # Fetch the document by its ID or return a 404 if not found
    document = get_object_or_404(Document, id=document_id)
    
    if request.method == 'POST':
        document.delete()
        return redirect('viewdoc')  
    return render(request, 'document_confirm_delete.html', {'document': document})


#upload image
@login_required(login_url='loginview')
def upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('viewimg')  # Redirect to a success page
    else:
        form = ImageUploadForm()
    return render(request, 'images.html')


#view images
@login_required(login_url='loginview')
def viewimg(request):
     img=ImageUpload.objects.all()
     return render(request,'images.html',{'img':img})

#delete images 
@login_required(login_url='loginview')
def delete_image(request, imgid):
    img = get_object_or_404(ImageUpload, id=imgid)
    
    if request.method == 'POST':
        img.delete()
        return redirect('viewimg')  
    return render(request, 'image_confirm_delete.html', {'img': img})


#text to pdf convertion
@login_required(login_url='loginview')
def upload_and_convert_view(request):
    if request.method == 'POST':
        form = UploadTextFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            if uploaded_file.content_type == 'text/plain':
                # Read the text file content
                text_content = uploaded_file.read().decode('utf-8')

                # Create the PDF response
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="converted_text.pdf"'

                # Generate the PDF
                p = canvas.Canvas(response, pagesize=letter)
                width, height = letter

                # Set initial position and line height
                x = 100
                y = height - 50
                line_height = 20

                # Split content into lines and add them to the PDF
                lines = text_content.splitlines()

                for line in lines:
                    # Split long lines to fit within the PDF page width
                    if len(line) > 90:  # Approximate limit per line
                        words = line.split(" ")
                        temp_line = ""
                        for word in words:
                            if len(temp_line + word) < 90:
                                temp_line += word + " "
                            else:
                                p.drawString(x, y, temp_line.strip())
                                y -= line_height
                                temp_line = word + " "
                        if temp_line:
                            p.drawString(x, y, temp_line.strip())
                            y -= line_height
                    else:
                        p.drawString(x, y, line)
                        y -= line_height

                    # Start a new page if we run out of space
                    if y <= 50:
                        p.showPage()
                        y = height - 50

                # Finalize the PDF
                p.showPage()
                p.save()

                return response
            else:
                return HttpResponse("Please upload a valid text file (.txt)")
    else:
        form = UploadTextFileForm()

    return render(request, 'upload_and_convert.html', {'form': form})


#logout page code
@login_required(login_url='loginview')
def logout(request):
    auth_logout(request)
    return redirect('loginview')



# Create your views here.
