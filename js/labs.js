
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

    firebase.database().ref(`/users/test`).set({
    username: name,
    email: email
    });
}

function saveToFirebase(email) {
    var emailObject = "ethan@houston.com"

    firebase.database().ref('subscription-entries').push().set(emailObject)
        .then(function (snapshot) {
            success(); // some success method
        }, function (error) {
            console.log('error' + error);
            error(); // some error method
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