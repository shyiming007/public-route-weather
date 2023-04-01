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

// var jqxhr = $.getJSON($SCRIPT_ROOT + "/occupancy/" + marker.station_number,
//     function(data) {
//     data = JSON.parse(data.data);
//     console.log('data', data);

//     var node = document.createElement('div'),
//     infowindow = new google.maps.InfoWindow(),
//     chart = new google.visualization.ColumnChart(node);

//     var chart_data = new google.visualization.DataTable();
//     chart_data.addColumn('datetime', 'Time of Day');
//     chart_data.addColumn('number', '#');
//     _.forEach(data, function(row){
//     chart_data.addRow([new Date(row[0]), row[1]]);
//     })

//     chart.draw(chart_data, options);
//     infowindow.setContent(node);
//     infowindow.open(marker.getMap(), marker);
//     }).fail(function() {
//     console.log( "error" );
//     })
    