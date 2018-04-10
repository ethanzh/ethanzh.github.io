let initMap = () => {

    let ref = database.ref(`coords`);

    let uluru = {lat: -29, lng: 131};

    const map = new google.maps.Map(document.getElementById('map'), {
            zoom: 4,
            center: uluru
        });

    ref.on(`child_added`, function (snapshot) {

        let value = snapshot.val();

        let new_html = `lat: ` + value[`lat`] + ` long: ` + value[`long`];

        // document.getElementById(`testblock`).innerHTML += (new_html + `<br />`)

        let lat = value[`lat`];
        let long = value[`long`];

        new google.maps.Marker({
            position: new google.maps.LatLng(lat, long),
            map: map,
        });


    });
};

initMap()