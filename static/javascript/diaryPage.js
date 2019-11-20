// Location of flask app
ROOT = window.location.origin;
var imgUrl = ROOT + '/diary/imgs';
var imgNames = [];
var numOfImages;
var nextImageToLoad;
var lastImageLoaded;

// Return an object containing file names
$.getJSON(imgUrl, function(data) {
    for (var i=0; i < data.length; i++) {
        imgNames.push(data[i]);
    }
    numOfImages = imgNames.length;
    // trigger function to display first set of images
    populate_imgs(imgNames);
})

// Call function to append more images as user scrolls down the page
$(window).scroll(function () {
    // -800 so we check before the end of the page to start appending new results, in case it seems to user that any gaps are the end of the gallery.
    if ($(document).height() - 800 <= $(window).scrollTop() + $(window).height()) {
        add_more();
    }
});

// function which locates backend images and appends images to our containers (first set)
function populate_imgs(img_names){
    for (var i=0; i <= 3; i++) {
        var temp_url = '../static/img/diary/' + img_names[i];
        if (i % 2 == 0) {
            $( ".photos1" ).append(`<img class=\"diaryImage\" src=\"${temp_url}\">`);
        } else {
            $( ".photos2" ).append(`<div class=\"imageContainer\"> 
                                        <img class=\"diaryImage\" src=\"${temp_url}\">
                                    </div>`);
        }
        nextImageToLoad = i + 1;
    }
}

// function to call when we need to add more results to the containers
function add_more() {
    // loading ceiling
    var plusFiveImgs = nextImageToLoad + 4;

    for (var j = nextImageToLoad; j <= plusFiveImgs; j++) {
        if (nextImageToLoad <= numOfImages-1){
            var temp_url = '../static/img/diary/' + imgNames[j];

            if (j % 2 == 0) {
                $( ".photos1" ).append(`<img class=\"diaryImage\" src=\"${temp_url}\">`);
            } else {
                $( ".photos2" ).append(`<img class=\"diaryImage\" src=\"${temp_url}\">`);
            }

            nextImageToLoad = j+1;
        }
    } 
}

