

// TutorsListData data array for filling in info box
var tutorsListData = [];

// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    populateTable();
    // UNI link click
    $('#tutorsList table tbody').on('click', 'td a.linkshowtutors', showTutorsInfo);
    $('#tutorsList table tbody').on('click', 'td a.linkdeletetutors', deleteTutors);


});

// Functions =============================================================

// Fill table with data
function populateTable() {

    // Empty content string
    var tableContent = '';

    // jQuery AJAX call for JSON
    $.getJSON( '/tutors/gettutorslist', function( data ) {
        tutorsListData = data;

        // For each item in our JSON, add a table row and cells to the content string
        $.each(data, function(){
            tableContent += '<tr>';
            tableContent += '<td><a href="#" class="linkshowtutors" rel="' + this.enth_user+", "+this.artst_user+ '">' + this.enth_user+", "+this.artst_user + '</a></td>';
            tableContent += '<td>' + this.artst_user + '</td>';
            tableContent += '<td><a href="/tutors/updatetutors/'+this.enth_user+", "+this.artst_user+'" class="linkedittutors" rel="' + this.enth_user+", "+this.artst_user+'">Edit Tutors</a></td>';
            tableContent += '<td><a href="" class="linkdeletetutors" rel="' + this.enth_user+", "+this.artst_user+'">Delete Tutors</a></td>';
            tableContent += '</tr>';
        });

        // Inject the whole content string into our existing HTML table
        $('#tutorsList table tbody').html(tableContent);
    });
};


// Show tutors Info
function showTutorsInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve uni from link rel attribute
    var tutors_id = $(this).attr('rel');
    console.log(tutors_id)

    // Get Index of object based on id value
    var arrayPosition = tutorsListData.map(function(arrayItem) { 
        str = arrayItem.enth_user+", "+arrayItem.artst_user;
        return str; }).indexOf(tutors_id);

    // Get our tutors Object

    var thisTutorsObject = tutorsListData[arrayPosition];

    //Populate Info Box
    $('#enth_user').text(thisTutorsObject.enth_user);
    $('#artst_user').text(thisTutorsObject.artst_user);
    $('#salary').text(thisTutorsObject.salary);
    $('#status').text(thisTutorsObject.status);
    $('#rating').text(thisTutorsObject.rating);
};

// Delete Tutors
function deleteTutors(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this tutors?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            url: '/tutors/deletetutors/' + $(this).attr('rel')
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
