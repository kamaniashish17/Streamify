function submitArtistForm(event, index) {
    loading();
    document.getElementById(`artistForm${index}`).submit();
}

function submitGenreForm(event, index) {
    loading();
    document.getElementById(`genreForm${index}`).submit();
}

function submitSearchForm() {
    loading();
    document.getElementById('search-form').submit();
}

function loading(){    
    document.getElementById('loader').style.visibility = 'visible';
}