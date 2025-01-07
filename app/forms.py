from django import forms

class SongUploadForm(forms.Form):
    audio_file = forms.FileField(label='Audio File', required=True)
    title = forms.CharField(max_length=255, label='Title', required=True)
    artist = forms.CharField(max_length=255, label='Artist', required=True)
    album = forms.CharField(max_length=255, label='Album', required=False)
    release_date = forms.DateField(label='Release Date', required=False, widget=forms.DateInput(attrs={'type': 'date'}))