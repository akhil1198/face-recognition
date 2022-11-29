from django.shortcuts import render
from facerecog.models import User
from facerecog.feed import responser
from facerecog.retrain import retrain
from django.http import HttpResponse, StreamingHttpResponse

# Create your views here.

def register(request):
    print(request)
    if request.method == "POST":
        form_name = request.POST['name']
        # form_id = request.POST['uuid']
        form_front = request.FILES['front']
        form_right = request.FILES['right']
        form_left = request.FILES['left']
        form_top = request.FILES['top']
        form_bottom = request.FILES['bottom']
        new_person = User.objects.create(name=form_name,
                                                    front=form_front,
                                                    right=form_right,
                                                    left=form_left,
                                                    top=form_top,
                                                    bottom=form_bottom)

        return render(request, "create_user.html", {'msg':'user Registered'})
    return render(request, "create_user.html")  
    
def rtrain(request):
	message = retrain()
	return render(request, "retrain.html", {'msg': message})

def feed(request, slug):
    url = "http://" + slug + ":8080/video"
    return StreamingHttpResponse(responser(0, url),  content_type='multipart/x-mixed-replace; boundary=frame')
    
def detect(request, slug):
    print("This is ", slug)
    url = "http://" + slug + ":8080/video"
    return StreamingHttpResponse(responser(1, url),  content_type='text/html')



    #source my-project-env/bin/activate