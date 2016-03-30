

// EnthusiastListData data array for filling in info box
var enthusiastListData = [];

// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    populateTable();
    // UNI link click
    $('#enthusiastList table tbody').on('click', 'td a.linkshowenthusiast', showEnthusiastInfo);
    $('#enthusiastList table tbody').on('click', 'td a.linkdeleteenthusiast', deleteEnthusiast);


});

// Functions =============================================================

// Fill table with data
function populateTable() {

    // Empty content string
    var tableContent = '';

    // jQuery AJAX call for JSON
    $.getJSON( '/enthusiast/getenthusiastlist', function( data ) {
        enthusiastListData = data;

        // For each item in our JSON, add a table row and cells to the content string
        $.each(data, function(){
            tableContent += '<tr>';
            tableContent += '<td><a href="#" class="linkshowenthusiast" rel="' + this.username + '">' + this.username + '</a></td>';
            tableContent += '<td>' + this.first_name + ' '+ this.last_name + '</td>';
            tableContent += '<td><a href="/enthusiast/updateenthusiast/'+this.username+'" class="linkeditenthusiast" rel="' + this.username + '">Edit Enthusiast</a></td>';
            tableContent += '<td><a href="" class="linkdeleteenthusiast" rel="' + this.username + '">Delete Enthusiast</a></td>';
            tableContent += '</tr>';
        });

        // Inject the whole content string into our existing HTML table
        $('#enthusiastList table tbody').html(tableContent);
    });
};


// Show Enthusiast Info
function showEnthusiastInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve uni from link rel attribute
    var username = $(this).attr('rel');

    // Get Index of object based on id value
    var arrayPosition = enthusiastListData.map(function(arrayItem) { return arrayItem.username; }).indexOf(username);

    // Get our enthusiast Object

    var thisEnthusiastObject = enthusiastListData[arrayPosition];

    //Populate Info Box
    $('#username').text(thisEnthusiastObject.username);
    $('#email').text(thisEnthusiastObject.email);
    $('#address').text(thisEnthusiastObject.address);
    $('#fname').text(thisEnthusiastObject.first_name);
    $('#mname').text(thisEnthusiastObject.middle_name);
    $('#lname').text(thisEnthusiastObject.last_name);
    $('#interests').text(thisEnthusiastObject.interests);
};

// Delete Enthusiast
function deleteEnthusiast(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this enthusiast?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            url: '/enthusiast/deleteenthusiast/' + $(this).attr('rel')
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
