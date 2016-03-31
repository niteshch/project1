

// ArtistperfListData data array for filling in info box
var artistperfListData = [];

// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    populateTable();
    // UNI link click
    $('#artistperfList table tbody').on('click', 'td a.linkshowartistperf', showArtistperfInfo);
    $('#artistperfList table tbody').on('click', 'td a.linkdeleteartistperf', deleteArtistperf);


});

// Functions =============================================================

// Fill table with data
function populateTable() {

    // Empty content string
    var tableContent = '';

    // jQuery AJAX call for JSON
    $.getJSON( '/artistperf/getartistperflist', function( data ) {
        artistperfListData = data;

        // For each item in our JSON, add a table row and cells to the content string
        $.each(data, function(){
            tableContent += '<tr>';
            tableContent += '<td><a href="#" class="linkshowartistperf" rel="' + this.artst_user+", "+this.event_id+ '">' + this.artst_user+", "+this.event_id+ '</a></td>';
            tableContent += '<td>' + this.artst_user + '</td>';
            /*tableContent += '<td><a href="/artistperf/updateartistperf/'+this.artst_user+", "+this.event_id+ '" class="linkeditartistperf" rel="' + this.artst_user+", "+this.event_id+ '">Edit Artist Performance</a></td>';*/
            tableContent += '<td><a href="" class="linkdeleteartistperf" rel="' + this.artst_user+", "+this.event_id+ '">Delete Artist Performance</a></td>';
            tableContent += '</tr>';
        });

        // Inject the whole content string into our existing HTML table
        $('#artistperfList table tbody').html(tableContent);
    });
};


// Show artistperf Info
function showArtistperfInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve uni from link rel attribute
    var artistperf_id = $(this).attr('rel');

    // Get Index of object based on id value
    var arrayPosition = artistperfListData.map(function(arrayItem) { 
        str = arrayItem.artst_user+", "+arrayItem.event_id;
        return str; }).indexOf(artistperf_id);

    // Get our artistperf Object

    var thisArtistperfObject = artistperfListData[arrayPosition];

    //Populate Info Box
    $('#artst_user').text(thisArtistperfObject.artst_user);
    $('#event_id').text(thisArtistperfObject.event_id);
};

// Delete Artistperf
function deleteArtistperf(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this artistperf?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            url: '/artistperf/deleteartistperf/' + $(this).attr('rel')
        }).done(function( response ) {

            // Update the table
            populateTable();

        });

    }
    else {

        // If they said no to the confirm, do nothing
        return false;

    }

};
