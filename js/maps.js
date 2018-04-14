let initMap = () => {

    let ref = database.ref(`coords`);

    let uluru = {lat: -29, lng: 131};

    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: uluru
    });

    let markers = [];

    ref.on(`child_added`, function (snapshot) {

        let value = snapshot.val();

        let lat = value[`lat`];
        let long = value[`long`];

        addMarker(lat, long);

    });

    // Adds a marker to the map and push to the array.
    let addMarker = (lat, long) => {
        let marker = new google.maps.Marker({
            position: new google.maps.LatLng(lat, long),
            map: map
        });
        markers.push(marker);
    };

    let setMapOnAll = (map) => {

        for (let i = 0; i < markers.length; i++) {

            markers[i].setMap(map);
        }
    };

    // Removes the markers from the map, but keeps them in the array.
    function clearMarkers() {
        setMapOnAll(null);
    }

    ref.on(`child_removed`, function (snapshot) {

        clearMarkers();

    });

};


initMap();