
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
        });
        google.maps.event.addListener(marker, 'click', function() {
            var contentString = '<div id="content"><h1>' + station.name + '</h1></div>' + '<div id="station_availability"></div>';
            var infowindow = new google.maps.InfoWindow({
                content: contentString
            });
            infowindow.open(map, marker);
        });
    //     // var contentString = '<div id="content"><h1>' + station.name + '</h1></div>'
    //     //                 + '<div id="station_availability"></div>';
    //                     google.maps.event.addListener(marker, 'click', function() {
    //                     drawInfoWindowChart(this);
    // });
});
}
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
    getStations();
    
}

// function drawInfoWindowChart(marker) {
//     var contentString = '<div id="content"><h1>' + station.name + '</h1></div>'
//                         + '<div id="station_availability"></div>';
//     var infowindow = new google.maps.InfoWindow({
//     content: contentString});
//     infowindow.open(map, marker);
// }



var map = null;
window.initMap = initMap;