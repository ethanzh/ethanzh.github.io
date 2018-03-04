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

const database = firebase.database();

document.cookie = "username=John Doe; expires=Thu, 18 Dec 2020 12:00:00 UTC";

function writeUserData() {

    let profileID = Math.random().toString().slice(3, 8);
    let name = document.getElementById('name').value;
    let email = document.getElementById('email').value;

    firebase.database().ref(`users`).child(profileID).set({
        username: name,
        email: email
    });
}

function retrieveDatabase() {

    let test = 12345;


    let ref = database.ref(`users`).child(`12345`);

    ref.on(`value`, function (snapshot) {
        let json = snapshot.val();


        document.getElementById(`testblock`).innerHTML += (json[`username`] + `<br />`);


    });

}

function sendMessage() {

    const timestamp = new Date().getTime().toString();

    let ref = database.ref(`messages`).child(timestamp);

    let message = document.getElementById(`message`).value;

    ref.set(message)
        .then(function (snapshot) {
            // pass
        }, function (error) {
            console.log('error' + error);
            // pass
        });
}

function messageFirstRun() {


    let ref = database.ref(`messages`);

    ref.once(`value`, function (snapshot) {

        let add_html = "";

        try {

            for (const [key, value] of Object.entries(snapshot.val())) {

                add_html += (value + `<br />`);
            }

        }
        catch(err) {

        }

        document.getElementById(`testblock`).innerHTML += add_html;

    })
}


function deleteMessages(){

    let ref = database.ref(`messages`);

    ref.remove();

    document.getElementById(`testblock`).innerHTML = ``;

}

function messageListnener() {

    let ref = database.ref(`messages`);

    ref.on(`child_added`, function (snapshot) {

        let value = snapshot.val();

        document.getElementById(`testblock`).innerHTML += (value + `<br />`);

    });

}

function messageRemovedListener() {

    let ref = database.ref(`messages`);

    ref.on(`child_removed`, function (snapshot) {

        document.getElementById(`testblock`).innerHTML = ``;

    });
}

function saveToFirebase() {


    let thing_to_push = {

        username: Math.random().toString().slice(3, 8),

        number: Math.random().toString().slice(3, 8)

    };

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

}

//retrieveDatabase();

messageFirstRun();
messageListnener();
messageRemovedListener();
