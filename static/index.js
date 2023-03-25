// Initialize and add the map
function initMap() {
    const dublin = { lat: 53.350140, lng: -6.266155 };
    // The map, centered at Dublin
    map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: dublin,
    });
    // The marker, positioned at Dublin
    const marker = new google.maps.Marker({
    position: dublin,
    map: map,
    });
}
    var map;
    window.initMap = initMap;