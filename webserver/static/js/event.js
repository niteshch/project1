

// EventListData data array for filling in info box
var eventListData = [];

// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    populateTable();
    // UNI link click
    $('#eventList table tbody').on('click', 'td a.linkshowevent', showEventInfo);
    $('#eventList table tbody').on('click', 'td a.linkdeleteevent', deleteEvent);


});

// Functions =============================================================

// Fill table with data
function populateTable() {

    // Empty content string
    var tableContent = '';

    // jQuery AJAX call for JSON
    $.getJSON( '/event/geteventlist', function( data ) {
        eventListData = data;
        console.log(eventListData);

        // For each item in our JSON, add a table row and cells to the content string
        $.each(data, function(){
            tableContent += '<tr>';
            tableContent += '<td><a href="#" class="linkshowevent" rel="' + this.event_id + '">' + this.event_id + '</a></td>';
            tableContent += '<td>' + this.event_type + '</td>';
            tableContent += '<td><a href="/event/updateevent/'+this.event_id+'" class="linkeditevent" rel="' + this.event_id + '">Edit Event</a></td>';
            tableContent += '<td><a href="" class="linkdeleteevent" rel="' + this.event_id + '">Delete Event</a></td>';
            tableContent += '</tr>';
        });

        // Inject the whole content string into our existing HTML table
        $('#eventList table tbody').html(tableContent);
    });
};


// Show event Info
function showEventInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve uni from link rel attribute
    var event_id = $(this).attr('rel');

    // Get Index of object based on id value
    var arrayPosition = eventListData.map(function(arrayItem) { return arrayItem.event_id.toString(); }).indexOf(event_id);

    // Get our event Object

    var thisEventObject = eventListData[arrayPosition];

    //Populate Info Box
    $('#event_id').text(thisEventObject.event_id);
    $('#start_time').text(thisEventObject.start_time);
    $('#end_time').text(thisEventObject.end_time);
    $('#address').text(thisEventObject.address);
    $('#event_type').text(thisEventObject.event_type);
};

// Delete Event
function deleteEvent(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this event?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            url: '/event/deleteevent/' + $(this).attr('rel')
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
