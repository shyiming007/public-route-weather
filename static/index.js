// referencing from the website https://www.youtube.com/watch?v=fc-D9eZmFFA
// referencing from the website https://www.youtube.com/watch?v=bXV8uHEANBI&t=619s
// Referencing from the website https://www.chartjs.org/docs/latest/getting-started/ 


    var btn1 = document.querySelector('.btn1');
    var btn2 = document.querySelector('.btn2');
    var realTimeDiv = document.querySelector('.search_real_time');
    var predictionDiv = document.querySelector('.search_prediction');
    var station_choose;


    // add butttons to change the page
    btn1.addEventListener('click', function() {
      realTimeDiv.classList.add('show');
      predictionDiv.classList.remove('show');
    });

    btn2.addEventListener('click', function() {
      predictionDiv.classList.add('show');
      realTimeDiv.classList.remove('show');
    });
    
    //add day of week to the title of chart
    const Day_Name = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
    const td = new Date();
    const dayWeek = td.getDay();
    const dayWeekName = Day_Name[dayWeek];
    document.getElementById("day_Week").textContent = dayWeekName;



// function for adding weather information
function addWeather(data) {
        
        var weather_html = 'Real-time Weather: ' + data[0].weather_description;
        
        var container = document.getElementById('weather-container');
        container.innerHTML = weather_html;
      
      }



// function for adding markers of stations
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
            avaiable_bike: station.avaiable_bikes,
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
            '<li>' + 'Available Bikes: ' + station.available_bikes + '</li>' +
            '<li>' + 'Available Bike Stands: ' + station.available_bike_stands + '</li>' +
            
            
            // '<li>' + dateInfo + '</li>' +
            '</ul></div>';





            var infowindow = new google.maps.InfoWindow({
                content: contentString
            
            });
            
            // get stations information based on different hours
            getHour(station.number)
            
            infowindow.open(map, marker);

            
        });
    });
}


// get data of stations
function getStations(){
    fetch("/stations")
    .then((response) => response.json())
    .then((data) => {
        console.log("fetch response", typeof data);
        addMarkers(data);
        addWeather(data);
    });
}

// get data of stations based on different hours
function getHour(n){
    fetch("/hour")
    .then((response) => response.json())
    .then((data) => {
        // console.log("fetch response", data['hour']);
        
        const today = new Date();
        const dayOfWeek = today.getDay();
        let chartDate;
        // make chartDate get different values from Sunday to Saturday
        switch (dayOfWeek) {
          case 0:
            chartDate = '2023-04-09';
            break;
          case 1:
            chartDate = '2023-04-10';
            break;
          case 2:
            chartDate = '2023-04-11';
            break;
          case 3:
            chartDate = '2023-04-12';
            break;
          case 4:
            chartDate = '2023-04-13';
            break;
          case 5:
            chartDate = '2023-04-14';
            break;
          case 6:
            chartDate = '2023-04-08';
            break;
        }
        
        displayChart(data, n, chartDate);
        displayChart2(data, n, chartDate);

    });
}

// chart part
function getChartData(data, stationNumber, day) {
    const stationData = data.filter(
      item => item.number === stationNumber && item.hour.startsWith(day)
    );
    const labels = stationData.map(item => item.hour.slice(11, 13));
    const values = stationData.map(item => item.average_bikes_hour);
    return { labels, values };
  }

let bikeChart = null;
function displayChart(data, stationNumber, day) {
    
    const chartData = getChartData(data, stationNumber, day);
    const chartOptions = {
      responsive: true,
      scales: {
        y: {
          title: {
            display: true,
            text: 'Number of average bikes'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Hour'
          }
        }
      }
    };
    const chartConfig = {
      type: 'bar',
      data: {
        labels: chartData.labels,
        datasets: [{
          label: `Average Available Bikes: Station ${stationNumber}`,
          data: chartData.values,
          backgroundColor: 'rgba(255, 255, 0, 0.7)',
          borderColor: 'rgba(255, 255, 0, 1)',
          borderWidth: 1
        }]
      },
      options: chartOptions
    };
    if (bikeChart) {
        bikeChart.destroy();
      }
    bikeChart = new Chart('bike-chart', chartConfig);
  }

  function getChartData2(data, stationNumber, day) {
    const stationData2 = data.filter(
      item => item.number === stationNumber && item.hour.startsWith(day)
    );
    const labels2 = stationData2.map(item => item.hour.slice(11, 13));
    const values2 = stationData2.map(item => item.average_bike_stands_hour);
    return { labels2, values2 };
  }

let bikeChart2 = null;
function displayChart2(data, stationNumber, day) {
    
    const chartData2 = getChartData2(data, stationNumber, day);
    const chartOptions2 = {
      responsive: true,
      scales: {
        y: {
          title: {
            display: true,
            text: 'Number of average bike stands'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Hour'
          }
        }
      }
    };
    const chartConfig2 = {
      type: 'bar',
      data: {
        labels: chartData2.labels2,
        datasets: [{
          label: `Average Available Stands: Station ${stationNumber}`,
          data: chartData2.values2,
          backgroundColor: 'rgba(54, 162, 235, 0.7)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: chartOptions2
    };
    if (bikeChart2) {
        bikeChart2.destroy();
      }
    bikeChart2 = new Chart('bike-chart2', chartConfig2);
  }



    
let currentPosition;
let selectedPlace;
let marker_des;
let directionsService;
let directionsRenderer;
let info_des;
let place_start;
let place_start_pre;
// Initialize and add the map
function initMap() {
    const dublin = { lat: 53.350140, lng: -6.266155 };
    // The map, centered at Dublin
    map = new google.maps.Map(document.getElementById("map"), {
    zoom: 14,
    center: dublin,
    });

    getStations();

    map.setCenter(dublin);
    map.setZoom(13);



// build a route for the real-time part
    const autocomplete_start = new google.maps.places.Autocomplete(
        document.getElementById('search_start_real'), {
            bounds: {
                east: dublin.lng + 0.001,
                west: dublin.lng - 0.001,
                south: dublin.lat - 0.001,
                north: dublin.lat + 0.001,
            },
            strictBounds: false,
        }
    );
    autocomplete_start.addListener('place_changed', function() {
        place_start = autocomplete_start.getPlace();
        
});

    const autocomplete_des = new google.maps.places.Autocomplete(
        document.getElementById('search_des_real'), {
            bounds: {
                east: dublin.lng + 0.001,
                west: dublin.lng - 0.001,
                south: dublin.lat - 0.001,
                north: dublin.lat + 0.001,
            },
            strictBounds: false,
        }
        
    );


        autocomplete_des.addListener('place_changed', function() {
            const place_des = autocomplete_des.getPlace();

            selectedPlace = {
                location: place_des.geometry.location,
                name: place_des.name,
                address: place_des.formatted_address,
                placeId: place_des.place_id,
            };

            map.setCenter(selectedPlace.location);

            if (!marker_des) {
                marker_des = new google.maps.Marker({
                    map: map,
                });
            }

            marker_des.setPosition(selectedPlace.location);

            if (!directionsService) {
                directionsService = new google.maps.DirectionsService();
            }

            if (!directionsRenderer) {
                directionsRenderer = new google.maps.DirectionsRenderer({
                    map: map,
                    polylineOptions: {
                        strokeColor: '#800080'
                    }
                });
            }

            directionsRenderer.set('directions', null)

            directionsService.route({
                    origin: new google.maps.LatLng(
                        place_start.geometry.location.lat(),
                        place_start.geometry.location.lng()
                    ),
                    destination: {
                        placeId: selectedPlace.placeId,
                    },
                    travelMode: 'BICYCLING',
                },
                function(response, status) {
                    if (status == 'OK') {
                        directionsRenderer.setDirections(response);

                        if (!info_des) {
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
                        info_des.open(map, marker_des)
                    }
                }
            );
        });
    
// });
// build a route of predicition

    map.setCenter(dublin);
    map.setZoom(13);
    const autocomplete_start_pre = new google.maps.places.Autocomplete(
        document.getElementById('search_start'), {
            bounds: {
                east: dublin.lng + 0.001,
                west: dublin.lng - 0.001,
                south: dublin.lat - 0.001,
                north: dublin.lat + 0.001,
            },
            strictBounds: false,
        }
    );
    autocomplete_start_pre.addListener('place_changed', function() {
        place_start_pre = autocomplete_start_pre.getPlace();
        
});

    const autocomplete_des_pre = new google.maps.places.Autocomplete(
        document.getElementById('search_des_pre'), {
            bounds: {
                east: dublin.lng + 0.001,
                west: dublin.lng - 0.001,
                south: dublin.lat - 0.001,
                north: dublin.lat + 0.001,
            },
            strictBounds: false,
        }
        
    );


        autocomplete_des_pre.addListener('place_changed', function() {
            const place_des_pre = autocomplete_des_pre.getPlace();

            selectedPlace = {
                location: place_des_pre.geometry.location,
                name: place_des_pre.name,
                address: place_des_pre.formatted_address,
                placeId: place_des_pre.place_id,
            };

            map.setCenter(selectedPlace.location);

            if (!marker_des) {
                marker_des = new google.maps.Marker({
                    map: map,
                });
            }

            marker_des.setPosition(selectedPlace.location);

            if (!directionsService) {
                directionsService = new google.maps.DirectionsService();
            }

            if (!directionsRenderer) {
                directionsRenderer = new google.maps.DirectionsRenderer({
                    map: map,
                    polylineOptions: {
                        strokeColor: '#800080'
                    }
                });
            }

            directionsRenderer.set('directions', null)

            directionsService.route({
                    origin: new google.maps.LatLng(
                        place_start_pre.geometry.location.lat(),
                        place_start_pre.geometry.location.lng()
                    ),
                    destination: {
                        placeId: selectedPlace.placeId,
                    },
                    travelMode: 'BICYCLING',
                },
                function(response, status) {
                    if (status == 'OK') {
                        directionsRenderer.setDirections(response);

                        if (!info_des) {
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
                        info_des.open(map, marker_des)
                    }
                }
            );
        });
    
// });



}




var map = null;
window.initMap = initMap;

