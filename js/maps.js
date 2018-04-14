
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

    for (let i = 0; i < 50; i++){

        let firstRandom = Math.random() * 100;
        let secondRandom = Math.random() * 100;

        let posOrNegOne = Math.random();
        if (posOrNegOne >= 0.5){
            posOrNegOne = 1;
        } else {
            posOrNegOne = -1;
        }

        let posOrNegTwo = Math.random();
        if (posOrNegTwo >= 0.5){
            posOrNegTwo = 1;
        } else {
            posOrNegTwo = -1;
        }

        let newLat = ((firstRandom / 5000) * posOrNegOne) + orgLat;
        let newLong = ((secondRandom / 1000) * posOrNegTwo) + orgLong;

        let newPoint = {
            lat: newLat,
            long: newLong
        };

        ref.push(newPoint);
    }

};


initMap();