function drawHeatmap(me) {
    console.log('toggle heatmap');
    console.log('clicked checkbox-1', me, me.prop('checked'));
    checked = me.prop('checked');
    if(checked) {
    if(heatmap == null) {
    var jqxhr = $.getJSON($SCRIPT_ROOT + "/heatmap",
    function(data) {
    console.log('data', data);
    var heatmapData = [];
    data.data.forEach((row) => {
    heatmapData.push(
    {location: new google.maps.LatLng(row.position_lat, row.position_lng),
    weight: row.available_bikes});
    });
    heatmap = new google.maps.visualization.HeatmapLayer({
    data: heatmapData,
    map: map
    });
    console.log(heatmap);
    heatmap.setMap(map);
    heatmap.set('radius', 40);
    // heatmap.setMap(heatmap.getMap() ? null : map);
    }).fail(function() {
    console.log('failed');
    });
    } else {
    heatmap.setMap(map);
    }
    } else {
    heatmap.setMap(null);
    }
    }


    // function addMarkers(real_times) {
    //     real_times.forEach(real_time => {
            
    //         var marker = new google.maps.Marker({
    //             position:{
    //                 lat: real_time.position_lat,
    //                 lng: real_time.position_lng,
    //             },
    //             map: map,
    //             title: real_time.name,
    //             real_time_number: real_time.number,
    //             total_bike_stands: real_time.bike_stands,
    //             real_time_status: real_time.status,
    //             avaiable_bike: real_time.avaiable_bikes,
    //             avaiable_bike_stand: real_time.avaiable_bike_stands,
                
    //         });
    //         if (real_time.status==0){
    //             var real_time_sta = 'OPEN'
    //         }
    //         else{
    //             real_time_sta = 'CLOSE'
    //         }
    //         var yellowIcon = {
    //             url: 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'
    //                 };
    //         marker.setIcon(yellowIcon);
            
    //         google.maps.event.addListener(marker, 'click', function() {
    //             var contentString = '<div id="content"><h1>' + real_time.name + '</h1></div>' + '<div id="real_time_availability"><ul>' +
    //             '<li>' + 'real_time Number: ' + real_time.number + '</li>' +
    //             '<li>' + 'Total Bike Stands: ' + real_time.bike_stands + '</li>' +
    //             '<li>' + 'real_time Status: ' + real_time_sta + '</li>' +
    //             '<li>' + 'Avaiable Bikes: ' + real_time.avaiable_bikes + '</li>' +
    //             '<li>' + 'Avaiable Bike Stands: ' + real_time.avaiable_bike_stands + '</li>' +
                
                
    //             // '<li>' + dateInfo + '</li>' +
    //             '</ul></div>';
