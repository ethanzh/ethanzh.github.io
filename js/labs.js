// Initialize Firebase
var config = {
    apiKey: "AIzaSyBjy9RhH3obaqdhsq9_GW78swKM3rSLVtI",
    authDomain: "personalsite-backend.firebaseapp.com",
    databaseURL: "https://personalsite-backend.firebaseio.com",
    projectId: "personalsite-backend",
    storageBucket: "",
    messagingSenderId: "379247301983"
};
firebase.initializeApp(config);

var database = firebase.database();

document.cookie = "username=John Doe; expires=Thu, 18 Dec 2020 12:00:00 UTC";

function writeUserData() {

    var profileID = Math.random().toString().slice(3,8);

    var name = document.getElementById('name').value;
    var email = document.getElementById('email').value;

    firebase.database().ref(`users`).child(profileID).set({
        username: name,
        email: email
    });

    console.log(document.cookie)
}

function getIP() {

    var url = 'https://api.ipify.org?format=json';

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText)
        }
    };
    xhttp.open("GET", url, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send();

}

getIP();

function retrieveDatabase() {

    var test = 12345;


    var ref = database.ref(`users`).child(`12345`);

    ref.on(`value`, function (snapshot) {
        var json = snapshot.val();

        console.log(json[`username`])
    });

}

retrieveDatabase();

function saveToFirebase() {


    var thing_to_push = {

        username: Math.random().toString().slice(3, 8),

        number: Math.random().toString().slice(3, 8)

    };

    var thing = Math.random().toString().slice(3, 8)

    firebase.database().ref(`users`).child((12345).toString())
        .set(thing_to_push)
        .then(function (snapshot) {
            // pass
        }, function (error) {
            console.log('error' + error);
            // pass
        });
}

function loadXMLDoc(url) {

    var xhttp = new XMLHttpRequest();
    var params = JSON.stringify('{"key": "val"}');
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("demo").innerHTML =
                this.responseText;
        }
    };
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhttp.send(params);

}

