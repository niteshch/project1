

// InstrumentListData data array for filling in info box
var instrumentListData = [];

// DOM Ready =============================================================
$(document).ready(function() {

    // Populate the user table on initial page load
    populateTable();
    // UNI link click
    $('#instrumentList table tbody').on('click', 'td a.linkshowinstrument', showInstrumentInfo);
    $('#instrumentList table tbody').on('click', 'td a.linkdeleteinstrument', deleteInstrument);


});

// Functions =============================================================

// Fill table with data
function populateTable() {

    // Empty content string
    var tableContent = '';

    // jQuery AJAX call for JSON
    $.getJSON( '/instrument/getinstrumentlist', function( data ) {
        instrumentListData = data;

        // For each item in our JSON, add a table row and cells to the content string
        $.each(data, function(){
            tableContent += '<tr>';
            tableContent += '<td><a href="#" class="linkshowinstrument" rel="' + this.instr_id + '">' + this.instr_id + '</a></td>';
            tableContent += '<td>' + this.instr_type + '</td>';
            tableContent += '<td><a href="/instrument/updateinstrument/'+this.instr_id+'" class="linkeditinstrument" rel="' + this.instr_id + '">Edit Instrument</a></td>';
            tableContent += '<td><a href="" class="linkdeleteinstrument" rel="' + this.instr_id + '">Delete Instrument</a></td>';
            tableContent += '</tr>';
        });

        // Inject the whole content string into our existing HTML table
        $('#instrumentList table tbody').html(tableContent);
    });
};


// Show instrument Info
function showInstrumentInfo(event) {

    // Prevent Link from Firing
    event.preventDefault();

    // Retrieve uni from link rel attribute
    var instr_id = $(this).attr('rel');

    // Get Index of object based on id value
    var arrayPosition = instrumentListData.map(function(arrayItem) { return arrayItem.instr_id.toString(); }).indexOf(instr_id);

    // Get our instrument Object

    var thisInstrumentObject = instrumentListData[arrayPosition];

    //Populate Info Box
    $('#instr_id').text(thisInstrumentObject.instr_id);
    $('#condition').text(thisInstrumentObject.condition);
    $('#instr_type').text(thisInstrumentObject.instr_type);
    $('#buyer_name').text(thisInstrumentObject.buyer_name);
    $('#seller_name').text(thisInstrumentObject.seller_name);
    $('#cost').text(thisInstrumentObject.cost);
    $('#status').text(thisInstrumentObject.status);
};

// Delete Instrument
function deleteInstrument(event) {

    event.preventDefault();

    // Pop up a confirmation dialog
    var confirmation = confirm('Are you sure you want to delete this instrument?');

    // Check and make sure the user confirmed
    if (confirmation === true) {

        // If they did, do our delete
        $.ajax({
            url: '/instrument/deleteinstrument/' + $(this).attr('rel')
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
