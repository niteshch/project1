

// ArtistListData data array for filling in info box
var artistListData = [];

// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    populateTable();
    // UNI link click
    $('#artistList table tbody').on('click', 'td a.linkshowartist', showArtistInfo);
    $('#artistList table tbody').on('click', 'td a.linkdeleteartist', deleteArtist);


});

// Functions =============================================================

// Fill table with data
function populateTable() {

    // Empty content string
    var tableContent = '';

    // jQuery AJAX call for JSON
    $.getJSON( '/artist/getartistlist', function( data ) {
        artistListData = data;

        // For each item in our JSON, add a table row and cells to the content string
        $.each(data, function(){
            tableContent += '<tr>';
            tableContent += '<td><a href="#" class="linkshowartist" rel="' + this.username + '">' + this.username + '</a></td>';
            tableContent += '<td>' + this.first_name + ' '+ this.last_name + '</td>';
            tableContent += '<td><a href="/artist/updateartist/'+this.username+'" class="linkeditartist" rel="' + this.username + '">Edit Artist</a></td>';
            tableContent += '<td><a href="" class="linkdeleteartist" rel="' + this.username + '">Delete Artist</a></td>';
            tableContent += '</tr>';
        });

        // Inject the whole content string into our existing HTML table
        $('#artistList table tbody').html(tableContent);
    });
};


// Show Artist Info
function showArtistInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve uni from link rel attribute
    var username = $(this).attr('rel');

    // Get Index of object based on id value
    var arrayPosition = artistListData.map(function(arrayItem) { return arrayItem.username; }).indexOf(username);

    // Get our artist Object

    var thisArtistObject = artistListData[arrayPosition];

    //Populate Info Box
    $('#username').text(thisArtistObject.username);
    $('#email').text(thisArtistObject.email);
    $('#address').text(thisArtistObject.address);
    $('#fname').text(thisArtistObject.first_name);
    $('#mname').text(thisArtistObject.middle_name);
    $('#lname').text(thisArtistObject.last_name);
    $('#experience').text(thisArtistObject.experience);
    $('#specialization').text(thisArtistObject.specialization);
};

// Delete Artist
function deleteArtist(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this artist?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            url: '/artist/deleteartist/' + $(this).attr('rel')
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
