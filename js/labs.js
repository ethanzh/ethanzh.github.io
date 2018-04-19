// Initialize Firebase
const config = {
    apiKey: "AIzaSyDR-NpXGPfiFlm9Tr9u9_eS-0D0xt_3JDs",
    authDomain: "gps-app-c31df.firebaseapp.com",
    databaseURL: "https://gps-app-c31df.firebaseio.com",
    projectId: "gps-app-c31df",
    storageBucket: "",
    messagingSenderId: "675799163706"
};

firebase.initializeApp(config);

const database = firebase.database();


let writeUserData = () => {
    let profileID = Math.random().toString().slice(3, 8);
    let name = document.getElementById(`name`).value;
    let email = document.getElementById(`email`).value;

    database.ref(`users`).child(profileID).set({
        username: name,
        email: email
    });
};


let sendMessage = () => {
    const timestamp = new Date().getTime().toString();

    let ref = database.ref(`coords`);

    let message = document.getElementById(`message`).value;

    ref.set({

        test: message

    })

};

let deleteMessages = () => {

    let ref = database.ref(`coords`);

    ref.remove();
};

let messageRemovedListener = () => {

    let marker = new google.maps.Marker({
        position: uluru,
        map: map
    });

    let ref = database.ref(`coords`);

    ref.on(`child_removed`, function (snapshot) {

        console.log(`Messages deleted`);

        document.getElementById(`testblock`).innerHTML = ``;

    });

};


let loadXMLDoc = (url) => {
    let xhttp = new XMLHttpRequest();
    let params = JSON.stringify('{"key": "val"}');
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("demo").innerHTML =
                this.responseText;
        }
    };
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(params);
};

function hello() {
    let uluru = {lat: -29.363, lng: 131.044};
    let map = new google.maps.Map(document.getElementById('map'), {
        zoom: 4,
        center: uluru
    });
    let marker = new google.maps.Marker({
        position: uluru,
        map: map
    });
}

// initMap();
// messageRemovedListener();
