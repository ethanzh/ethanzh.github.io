// Initialize Firebase
const config = {
    apiKey: "AIzaSyBjy9RhH3obaqdhsq9_GW78swKM3rSLVtI",
    authDomain: "personalsite-backend.firebaseapp.com",
    databaseURL: "https://personalsite-backend.firebaseio.com",
    projectId: "personalsite-backend",
    storageBucket: "",
    messagingSenderId: "379247301983"
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

    document.getElementById(`testblock`).innerHTML = ``;
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

function test() {
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
