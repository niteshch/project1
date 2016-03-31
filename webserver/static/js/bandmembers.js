

// BandmembersListData data array for filling in info box
var bandmembersListData = [];

// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    populateTable();
    // UNI link click
    $('#bandmembersList table tbody').on('click', 'td a.linkshowbandmembers', showBandmembersInfo);
    $('#bandmembersList table tbody').on('click', 'td a.linkdeletebandmembers', deleteBandmembers);


});

// Functions =============================================================

// Fill table with data
function populateTable() {

    // Empty content string
    var tableContent = '';

    // jQuery AJAX call for JSON
    $.getJSON( '/bandmembers/getbandmemberslist', function( data ) {
        bandmembersListData = data;

        // For each item in our JSON, add a table row and cells to the content string
        $.each(data, function(){
            tableContent += '<tr>';
            tableContent += '<td><a href="#" class="linkshowbandmembers" rel="' + this.artst_user+", "+this.band_id+ '">' + this.artst_user+", "+this.band_id+ '</a></td>';
            tableContent += '<td>' + this.artst_user + '</td>';
            tableContent += '<td><a href="/bandmembers/updatebandmembers/'+this.artst_user+", "+this.band_id+ '" class="linkeditbandmembers" rel="' + this.artst_user+", "+this.band_id+ '">Edit Band Members</a></td>';
            tableContent += '<td><a href="" class="linkdeletebandmembers" rel="' + this.artst_user+", "+this.band_id+ '">Delete Band Members</a></td>';
            tableContent += '</tr>';
        });

        // Inject the whole content string into our existing HTML table
        $('#bandmembersList table tbody').html(tableContent);
    });
};


// Show bandmembers Info
function showBandmembersInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve uni from link rel attribute
    var bandmembers_id = $(this).attr('rel');

    // Get Index of object based on id value
    var arrayPosition = bandmembersListData.map(function(arrayItem) { 
        str = arrayItem.artst_user+", "+arrayItem.band_id;
        return str; }).indexOf(bandmembers_id);

    // Get our bandmembers Object

    var thisBandmembersObject = bandmembersListData[arrayPosition];

    //Populate Info Box
    $('#artst_user').text(thisBandmembersObject.artst_user);
    $('#band_id').text(thisBandmembersObject.band_id);
    $('#status').text(thisBandmembersObject.status);
};

// Delete Bandmembers
function deleteBandmembers(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this bandmembers?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            url: '/bandmembers/deletebandmembers/' + $(this).attr('rel')
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
