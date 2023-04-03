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
