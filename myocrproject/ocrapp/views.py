import os, json, glob, io, cv2
import numpy as np
from PIL import Image
from .forms import ImageUploadForm, UserRegisterForm
from .models import uploadedFile,ProcessedImage
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from ocrmodel.pipeline import process
from django.conf import settings
import easyocr
from easyocrmodel.pipeline import easy_process

# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
            return redirect('login_request')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            messages.error(request, "User doesn't exist.")
            return redirect('register')
  
        if user.check_password(password):
            login(request, user)
            return redirect('image_upload')
        else:
            return render(request, "login.html", {"form": form, "invalid_creds": True}) 
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


@login_required
def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_content = file.read()
            file_exists = uploadedFile.objects.filter(image_data=file_content).first()
            
            if not file_exists:
                file_name = default_storage.save(file.name, ContentFile(file_content))
                uploaded_file = uploadedFile.objects.create(
                    file_name=file_name,
                    image_data=file_content,
                    file_path=os.path.join(settings.MEDIA_ROOT, 'uploads',file_name),
                    uploaded_at=default_storage.url(file_name)
                )
            language = form.cleaned_data.get('language')

            return redirect('model_process', image_name=file, language=language)
    form = ImageUploadForm()
    return render(request, "image_upload.html", {"form": form, "logged_in": True})

def model_process(request, image_name, language):
    context = {"logged_in": True, 'show_prompt': True}
    base_dir = settings.MEDIA_ROOT
    output_dir = os.path.join(base_dir , f"/result/{request.user.username}")
    os.makedirs(output_dir, exist_ok=True)


    input_file = uploadedFile.objects.get(file_name=image_name)

    processed_data = ProcessedImage.objects.filter(image=input_file).first()

    if processed_data:
        context['image_url'] = processed_data.image_data
        context['processed_text'] = json.loads(processed_data.processed_text)
        return render(request, 'display_processed_text.html', context)

    input_file_path = os.path.join(base_dir, image_name)
    if language == 'en':
        process(input_file_path, output_dir)

        context['image_url'] = f"{settings.MEDIA_URL}/result/{request.user.username}/{image_name}"
        image_name = image_name.rsplit(".",1)
        json_file_name = f"{image_name[0]}_text.json"
        json_file_path = os.path.join(f"{output_dir}/json/{json_file_name}")

        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)
                context['processed_text'] = data
                processed_image = ProcessedImage.objects.create(
                    user=request.user,
                    image = image_name[0] + ".jpg",
                    image_data= context['image_url'],
                    processed_text=json.dumps(data)
                )
    else:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)

        processed_image_path, extracted_texts = easy_process(input_file_path, language, output_dir)

        base_filename = os.path.splitext(image_name)[0]
        processed_filename = f"{base_filename}.jpg"
        image_path = os.path.join(output_dir, processed_filename)

        context['image_url'] = f"{settings.MEDIA_URL}/result/{request.user.username}/{processed_filename}"
        image_name = image_name.rsplit(".",1)

        json_file_name = f"{image_name[0]}_text.json"
        json_dir = os.path.join(output_dir, "json")
        os.makedirs(json_dir, exist_ok=True)
        json_file_path = os.path.join(json_dir, json_file_name)

        extracted_data = {'texts': extracted_texts}

        with open(json_file_path, 'w') as json_file:
            json.dump(extracted_data, json_file)

        print(f"Data written to {json_file_path}")

        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)
            context['processed_text'] = data
            processed_image = ProcessedImage.objects.create(
                user=request.user,
                image = image_name[0] + ".jpg",
                image_data= context['image_url'],
                processed_text=json.dumps(data)
            )    


    return render(request, 'display_processed_text.html', context)

@login_required
def history(request):
    context = {'logged_in': True}
    base_dir = os.path.join(settings.MEDIA_ROOT, f"result/{request.user.username}")
    
    image_file_paths = [f for extension in ['*.jpg', '*.jpeg', '*.png', '*.pdf'] for f in glob.glob(os.path.join(base_dir, extension))]
    text_file_paths = {os.path.basename(f).replace('_text.json', ''): f for f in glob.glob(os.path.join(f"{base_dir}/json", '*_text.json'))}

    image_data = []
    for image_file_path in image_file_paths:
        image_file_name = os.path.basename(image_file_path)
        image_url = os.path.join(settings.MEDIA_URL, "result", request.user.username, image_file_name).replace("\\", "/")
        
        base_name = os.path.splitext(image_file_name)[0]
        text_file_path = text_file_paths.get(base_name)
        if text_file_path:
            text_url = os.path.join(settings.MEDIA_URL, "result", request.user.username, "json", os.path.basename(text_file_path)).replace("\\", "/")
        else:
            text_url = None
        
        image_data.append({
            'image_url': image_url,
            'text_url': text_url, 
        })
    
    context['image_data'] = image_data

    return render(request, 'history.html', context)

def contact_form(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        email_body = f"Message from {name}, Email: {email}\n\n{message}"

        send_mail(
            subject,
            email_body,
            'daslaliya4750@conestogac.on.ca',
            ['Parminderkaur5610@conestogac.on.ca', 'Jthind4958@conestogac.on.ca'], 
            fail_silently=False,
        )

        messages.success(request, 'Your message has been sent. Thank you!')
        return redirect('/#contact')

    return redirect('/#contact')

    
def logout(request):
    return redirect('index')

def policy(request):
    return render(request, 'policy.html')
