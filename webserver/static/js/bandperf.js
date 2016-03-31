

// BandperfListData data array for filling in info box
var bandperfListData = [];

// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    populateTable();
    // UNI link click
    $('#bandperfList table tbody').on('click', 'td a.linkshowbandperf', showBandperfInfo);
    $('#bandperfList table tbody').on('click', 'td a.linkdeletebandperf', deleteBandperf);


});

// Functions =============================================================

// Fill table with data
function populateTable() {

    // Empty content string
    var tableContent = '';

    // jQuery AJAX call for JSON
    $.getJSON( '/bandperf/getbandperflist', function( data ) {
        bandperfListData = data;

        // For each item in our JSON, add a table row and cells to the content string
        $.each(data, function(){
            tableContent += '<tr>';
            tableContent += '<td><a href="#" class="linkshowbandperf" rel="' + this.band_id+", "+this.event_id+ '">' + this.band_id+", "+this.event_id+ '</a></td>';
            tableContent += '<td>' + this.band_id + '</td>';
            /*tableContent += '<td><a href="/bandperf/updatebandperf/'+this.artst_user+", "+this.event_id+ '" class="linkeditbandperf" rel="' + this.artst_user+", "+this.event_id+ '">Edit Artist Performance</a></td>';*/
            tableContent += '<td><a href="" class="linkdeletebandperf" rel="' + this.band_id+", "+this.event_id+ '">Delete Artist Performance</a></td>';
            tableContent += '</tr>';
        });

        // Inject the whole content string into our existing HTML table
        $('#bandperfList table tbody').html(tableContent);
    });
};


// Show bandperf Info
function showBandperfInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve uni from link rel attribute
    var bandperf_id = $(this).attr('rel');

    // Get Index of object based on id value
    var arrayPosition = bandperfListData.map(function(arrayItem) { 
        str = arrayItem.band_id+", "+arrayItem.event_id;
        return str; }).indexOf(bandperf_id);

    // Get our bandperf Object

    var thisBandperfObject = bandperfListData[arrayPosition];

    //Populate Info Box
    $('#band_id').text(thisBandperfObject.band_id);
    $('#event_id').text(thisBandperfObject.event_id);
};

// Delete Bandperf
function deleteBandperf(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this bandperf?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            url: '/bandperf/deletebandperf/' + $(this).attr('rel')
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
