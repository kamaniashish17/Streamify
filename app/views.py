from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import io
from .forms import SongUploadForm
from .utils import upload_audio_file, get_search_results
import re

results = []
indexed_results = []
new_audio_data = None

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'user/home.html')
    else:
        global new_audio_data
        if request.method == "POST":
            upload_audio_file(request)
            new_audio_data = request.FILES["audioData"].read()
            return render(request, 'app/home.html', {'message' : 'Song uploaded successfully!'})
        return render(request, 'app/home.html')

def upload_song(request):
    print(request.POST)
    form = SongUploadForm()
    return render(request, 'app/upload.html', {'form' : form})


def search_results(request):
    global results
    global indexed_results

    if request.method == "POST":
        if "search_text" in request.POST:
            search_text = request.POST["search_text"]
            results = get_search_results(search_text)
            indexed_results = []
            for index, result in enumerate(results):
                indexed_results.append({
                    "index" : index,
                    "trackName" : result["trackName"],
                    "artistName" : result["artistName"],
                    "genreName" : result["genreName"],
                    "coverImage" : result["coverImage"],
                    "isCoverImageURL" : isinstance(result["coverImage"], str)
                })
            return render(request, 'app/search_results.html', {'search_text': search_text, 'indexed_results': indexed_results})
        elif "index" in request.POST:
            index = int(request.POST["index"])
            return render(request, 'app/search_results.html', {'track_name' : results[index]["trackName"], 'indexed_results': indexed_results, 'index' : index})

    return render(request, 'app/home.html')


def serve_image(request, index):
    global results
    image_data = results[index]["coverImage"]
    if image_data:
        response = HttpResponse(image_data, content_type="image/png")
        return response
    return JsonResponse({"error": "Cover image not found"}, status=404)


def serve_audio(request, index):
    global results
    audio_data = results[index]["audioData"]
    if audio_data:
        response = HttpResponse(io.BytesIO(audio_data), content_type="audio/mpeg")
        response['Content-Disposition'] = f'inline; filename="{results[index]["trackName"]}.mp3"'
        return response
    return JsonResponse({"error": "Track not found"}, status=404)

def serve_new_uploaded_audio(request):
    global new_audio_data
    if new_audio_data:
        response = HttpResponse(io.BytesIO(new_audio_data), content_type="audio/mpeg")
        response['Content-Disposition'] = f'inline; filename="new_song.mp3"'
        return response
    return JsonResponse({"error": "Track not found"}, status=404)



