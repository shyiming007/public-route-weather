var jqxhr = $.getJSON("/stations", function(data) {
    console.log( "success", data);
})
    .done(function() {
    console.log( "second success" );
    })
    .fail(function() {
    console.log( "error" );
    })
    .always(function() {
    console.log( "complete" );
    });

