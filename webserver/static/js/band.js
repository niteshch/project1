

// BandListData data array for filling in info box
var bandListData = [];

// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    populateTable();
    // UNI link click
    $('#bandList table tbody').on('click', 'td a.linkshowband', showBandInfo);
    $('#bandList table tbody').on('click', 'td a.linkdeleteband', deleteBand);


});

// Functions =============================================================

// Fill table with data
function populateTable() {

    // Empty content string
    var tableContent = '';

    // jQuery AJAX call for JSON
    $.getJSON( '/band/getbandlist', function( data ) {
        bandListData = data;

        // For each item in our JSON, add a table row and cells to the content string
        $.each(data, function(){
            tableContent += '<tr>';
            tableContent += '<td><a href="#" class="linkshowband" rel="' + this.band_id + '">' + this.band_id + '</a></td>';
            tableContent += '<td>' + this.band_name + '</td>';
            tableContent += '<td><a href="/band/updateband/'+this.band_id+'" class="linkeditband" rel="' + this.band_id + '">Edit Band</a></td>';
            tableContent += '<td><a href="" class="linkdeleteband" rel="' + this.band_id + '">Delete Band</a></td>';
            tableContent += '</tr>';
        });

        // Inject the whole content string into our existing HTML table
        $('#bandList table tbody').html(tableContent);
    });
};


// Show band Info
function showBandInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve uni from link rel attribute
    var band_id = $(this).attr('rel');

    // Get Index of object based on id value
    var arrayPosition = bandListData.map(function(arrayItem) { return arrayItem.band_id; }).indexOf(band_id);

    // Get our band Object

    var thisBandObject = bandListData[arrayPosition];

    //Populate Info Box
    $('#band_id').text(thisBandObject.band_id);
    $('#band_name').text(thisBandObject.band_name);
    $('#since').text(thisBandObject.since);
    $('#specialization').text(thisBandObject.specialization);
};

// Delete Band
function deleteBand(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this band?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            url: '/band/deleteband/' + $(this).attr('rel')
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
