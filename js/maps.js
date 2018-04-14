
const ref = database.ref(`coords`);

const orgLat = 37.427148;
const orgLong = -122.10964;

let initMap = () => {

    let uluru = {lat: orgLat, lng: orgLong};

    const map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
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


let addRandomPoints = () => {

    const NorthSouth = Math.random();

    let ns;

    switch (true) {

        case NorthSouth < 0.5:
            ns = 1; // North
            break;
        case NorthSouth >= 0.5 && NorthSouth < 1:
            ns = -1; // South
            break;

    }

    const EastWest = Math.random();

    let ew;

    switch (true) {

        case EastWest < 0.5:
            ew = 1; // East
            break;
        case EastWest >= 0.5 && EastWest < 1:
            ew = -1; // West
            break;
    }

    for (let i = 0; i < 50; i++){

        let scaled = i / 500;

        let newLat = orgLat + (scaled * ew);
        let newLong = orgLong + (scaled * ns);

        console.log(ew);

        console.log("hi 1");

        let newPoint = {
            lat: newLat,
            long: newLong
        };

        ref.push(newPoint);
    }

};


initMap();