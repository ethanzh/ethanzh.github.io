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

function writeUserData(name, email) {

    firebase.database().ref(`users`).set({
        username: name,
        email: email
    });
}

function retrieveDatabase() {

    var test = 12345;


    var ref = database.ref(`users`).child(`12345`);

    ref.on(`value`, function (snapshot) {
        var json = snapshot.val();

        console.log(json[`number`])
    });

}

function saveToFirebase() {


    var thing_to_push = {

        username: Math.random().toString().slice(3, 8),

        number: Math.random().toString().slice(3, 8)

    };

    var thing = Math.random().toString().slice(3, 8)

    firebase.database().ref(`users`).child(thing.toString())
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

function readDatabase() {

    fire

}