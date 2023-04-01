
// $.ajax({
//     url: "/occupancy/" + station_number,
//     success: function(response){
//       var data = JSON.parse(response.data);
      
//     }
//   });
// fetch('/occupancy/12')
//         .then(response => response.json())
//         .then(data => {
//         const firstValue = data.data[0][1];
//         console.log(`The first value of res is: ${firstValue}`);
//         });
// function getOccupancy(stationId, callback) {
//     fetch(`/occupancy/${stationId}`)
//     .then((response) => response.json())
//     .then((data) => {
//         console.log("fetch response", typeof data);
//         static occupancy = JSON.parse(data.data)[2][3];
//         callback(occupancy);
//     });
// }
function addMarkers(stations) {
    stations.forEach(station => {
        
        var marker = new google.maps.Marker({
            position:{
                lat: station.position_lat,
                lng: station.position_lng,
            },
            map: map,
            title: station.name,
            station_number: station.number,
            total_bike_stands: station.bike_stands,
            station_status: station.status,
            firstValue: station.avaiable_bikes,
            avaiable_bike_stand: station.avaiable_bike_stands,
            
        });
        if (station.status==0){
            var station_sta = 'OPEN'
        }
        else{
            station_sta = 'CLOSE'
        }
        
        google.maps.event.addListener(marker, 'click', function() {
            var contentString = '<div id="content"><h1>' + station.name + '</h1></div>' + '<div id="station_availability"><ul>' +
            '<li>' + 'Station Number: ' + station.number + '</li>' +
            '<li>' + 'Total Bike Stands: ' + station.bike_stands + '</li>' +
            '<li>' + 'Station Status: ' + station_sta + '</li>' +
            '<li>' + 'Avaiable Bikes: ' + station.avaiable_bikes + '</li>' +
            '<li>' + 'Avaiable Bike Stands: ' + station.avaiable_bike_stands + '</li>' +
            
            
            // '<li>' + dateInfo + '</li>' +
            '</ul></div>';
            // // var jqxhr = $.getJSON($SCRIPT_ROOT + "/occupancy/" + marker.station_number, function(data) {
            //     data = JSON.parse(data.data);
            //     console.log('data', data);
            
            //     var node = document.createElement('div'),
            //     // infowindow = new google.maps.InfoWindow(),
            //     chart = new google.visualization.ColumnChart(node);
            
            //     var chart_data = new google.visualization.DataTable();
            //     chart_data.addColumn('datetime', 'Time of Day');
            //     chart_data.addColumn('number', '#');
            //     _.forEach(data, function(row){
            //     chart_data.addRow([new Date(row[0]), row[1]]);
            //     })
            
            //     chart.draw(chart_data, options);
                // infowindow.setContent(node);
                // infowindow.open(marker.getMap(), marker);
                // }).fail(function() {
                // console.log( "error" );
                // })
            
            var infowindow = new google.maps.InfoWindow({
                content: contentString
            
            });
            
            infowindow.open(map, marker);
        });
    });
}


    
//     var infowindow = new google.maps.InfoWindow({
//         content: contentString
    
//     });
    
//     infowindow.open(map, occupancy);
// });
    
// });
// }
// function addMarkers(stations) {
//     _.forEach(stations, function(station) {
//       var marker = new google.maps.Marker({
//         position: {
//           lat: station.position_lat,
//           lng: station.position_lng
//         },
//         map: map,
//         title: station.name,
//         station_number: station.number,
//       });
//       var contentString =
//         '<div id="content"><h1>' +
//         station.name +
//         '</h1></div>' +
//         '<div id="station_availability"></div>';
//       google.maps.event.addListener(marker, 'click', function() {
//         drawInfoWindowChart(this);
//       });
//     });
//   }

function getStations(){
    fetch("/stations")
    .then((response) => response.json())
    .then((data) => {
        console.log("fetch response", typeof data);
        addMarkers(data);
    
    });
}

// function getOccupancy(){
//     fetch("/occupancy/{station_id}")
//     .then((response) => response.json())
//     .then((data) => {
//         console.log("fetch response", typeof data);
//         addOccupancy(data);
    
//     });
// }

// function drawHeatmap(me) {
//     // console.log('toggle heatmap');
//     console.log('clicked checkbox-1', me, me.prop('checked'));
//     checked = me.prop('checked');
//     if(checked) {
//     if(heatmap == null) {
//     var jqxhr = $.getJSON($SCRIPT_ROOT + "/heatmap",
//     function(data) {
//     console.log('data', data);
//     var heatmapData = [];
//     data.data.forEach((row) => {
//     heatmapData.push(
//     {location: new google.maps.LatLng(row.position_lat, row.position_lng),
//     weight: row.available_bikes});
//     });
//     heatmap = new google.maps.visualization.HeatmapLayer({
//     data: heatmapData,
//     map: map
//     });
//     console.log(heatmap);
//     heatmap.setMap(map);
//     heatmap.set('radius', 40);
//     // heatmap.setMap(heatmap.getMap() ? null : map);
//     }).fail(function() {
//     console.log('failed');
//     });
//     } else {
//     heatmap.setMap(map);
//     }
//     } else {
//     heatmap.setMap(null);
//     }
//     }
    

// Initialize and add the map
function initMap() {
    const dublin = { lat: 53.350140, lng: -6.266155 };
    // The map, centered at Dublin
    map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: dublin,
    });
    // The marker, positioned at Dublin
    // const marker = new google.maps.Marker({
    // position: dublin,
    // map: map,
    // });
    // getOccupancy();
    getStations();
    
}




var map = null;
window.initMap = initMap;