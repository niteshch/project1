

// HiresListData data array for filling in info box
var hiresListData = [];

// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    populateTable();
    // UNI link click
    $('#hiresList table tbody').on('click', 'td a.linkshowhires', showHiresInfo);
    $('#hiresList table tbody').on('click', 'td a.linkdeletehires', deleteHires);


});

// Functions =============================================================

// Fill table with data
function populateTable() {

    // Empty content string
    var tableContent = '';

    // jQuery AJAX call for JSON
    $.getJSON( '/hires/gethireslist', function( data ) {
        hiresListData = data;

        // For each item in our JSON, add a table row and cells to the content string
        $.each(data, function(){
            tableContent += '<tr>';
            tableContent += '<td><a href="#" class="linkshowhires" rel="' + this.enth_user+", "+this.artst_user+", "+this.event_id + '">' + this.enth_user+", "+this.artst_user+", "+this.event_id + '</a></td>';
            tableContent += '<td>' + this.artst_user + '</td>';
            tableContent += '<td><a href="/hires/updatehires/'+this.enth_user+", "+this.artst_user+", "+this.event_id+'" class="linkedithires" rel="' + this.enth_user+", "+this.artst_user+", "+this.event_id + '">Edit Hires</a></td>';
            tableContent += '<td><a href="" class="linkdeletehires" rel="' + this.enth_user+", "+this.artst_user+", "+this.event_id + '">Delete Hires</a></td>';
            tableContent += '</tr>';
        });

        // Inject the whole content string into our existing HTML table
        $('#hiresList table tbody').html(tableContent);
    });
};


// Show hires Info
function showHiresInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve uni from link rel attribute
    var hires_id = $(this).attr('rel');
    console.log(hires_id)

    // Get Index of object based on id value
    var arrayPosition = hiresListData.map(function(arrayItem) { 
        str = arrayItem.enth_user+", "+arrayItem.artst_user+", "+arrayItem.event_id;
        return str; }).indexOf(hires_id);

    // Get our hires Object

    var thisHiresObject = hiresListData[arrayPosition];

    //Populate Info Box
    $('#enth_user').text(thisHiresObject.enth_user);
    $('#artst_user').text(thisHiresObject.artst_user);
    $('#event_id').text(thisHiresObject.event_id);
    $('#status').text(thisHiresObject.status);
    $('#rating').text(thisHiresObject.rating);
};

// Delete Hires
function deleteHires(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this hires?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            url: '/hires/deletehires/' + $(this).attr('rel')
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
