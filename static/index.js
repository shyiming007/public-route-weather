// referencing from the website https://www.youtube.com/watch?v=fc-D9eZmFFA
// referencing from the website https://www.youtube.com/watch?v=bXV8uHEANBI&t=619s


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
        var yellowIcon = {
            url: 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'
                };
        marker.setIcon(yellowIcon);
        
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


    
let currentPosition;
let selectedPlace;
let marker_des;
let directionsService;
let directionsRenderer;
let info_des;
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

    navigator.geolocation.getCurrentPosition(function(position){
        currentPosition = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
        }
        
        map.setCenter(currentPosition);
        map.setZoom(13);
        const autocomplete = new google.maps.places.Autocomplete(
            document.getElementById('search_des'),
            {
            types: ['restaurant'],
            bounds:{
                east: currentPosition.lng + 0.001,
                west: currentPosition.lng - 0.001,
                south: currentPosition.lat - 0.001,
                north: currentPosition.lat + 0.001,
            
            },
            strictBounds: false,

            }
        )
        autocomplete.addListener('place_changed', function(){
        const place = autocomplete.getPlace();

        selectedPlace = {
            location: place.geometry.location,
            name: place.name,
            address: place.formatted_address,
            placeId: place.place_id,
        };

        map.setCenter(selectedPlace.location);

        if (!marker_des){
            marker_des = new google.maps.Marker({
                map: map,
            });
        }
        // // Create a yellow icon
        // var yellowIcon = {
        //     url: 'http://maps.google.com/mapfiles/ms/icons/yellow-dot.png'
        //         };
  
        // // Set the icon to the yellow icon
        // marker_des.setIcon(yellowIcon);
        marker_des.setPosition(selectedPlace.location);
        
        console.log(selectedPlace)
        if (!directionsService){
            directionsService = new google.maps.DirectionsService();
        }

        if (!directionsRenderer){
            directionsRenderer = new google.maps.DirectionsRenderer({
            map:map,
            polylineOptions: {
                strokeColor: '#800080' 
              }
        });
        }

        directionsRenderer.set('directions',null)
    
        directionsService.route({
            origin:new google.maps.LatLng(
                currentPosition.lat,
                currentPosition.lng
            ),
            destination:{
                placeId: selectedPlace.placeId,
            },
            travelMode: 'BICYCLING',
        },
        function(response, status){
            if (status == 'OK'){
                directionsRenderer.setDirections(response);

                if(!info_des){
                    info_des = new google.maps.InfoWindow();

                }
                info_des.setContent(
                    `
                    <h3>${selectedPlace.name}</h3>
                    <div>Address: ${selectedPlace.address}</div>
                    <div>Location: ${selectedPlace.location}</div>
                    <div>Ride time: ${response.routes[0].legs[0].duration.text}</div>
                    `
                );
                info_des.open(map,marker_des)
            }
        }
        );

    });

});
}




var map = null;
window.initMap = initMap;