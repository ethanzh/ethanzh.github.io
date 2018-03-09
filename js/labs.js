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
    let name = document.getElementById('name').value;
    let email = document.getElementById('email').value;

    database.ref(`users`).child(profileID).set({
        username: name,
        email: email
    });
};


let sendMessage = () => {
    const timestamp = new Date().getTime().toString();

    let ref = database.ref(`messages`).child(timestamp);

    let message = document.getElementById(`message`).value;

    ref.set(message)
        .then(function (snapshot) {
            console.log("message sent");
        }, function (error) {
            console.log('error' + error);
            // pass
        });
};


let deleteMessages = () => {

    let ref = database.ref(`messages`);

    ref.remove();

    document.getElementById(`testblock`).innerHTML = ``;
};


let messageListener = () => {

    let ref = database.ref(`messages`);

    ref.on(`child_added`, function (snapshot) {

        console.log("Listening for messages");

        let value = snapshot.val();

        document.getElementById(`testblock`).innerHTML += (value + `<br />`);

    });
};


let messageRemovedListener = () => {

    let ref = database.ref(`messages`);

    ref.on(`child_removed`, function (snapshot) {

        console.log("Deleted messages");

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

//retrieveDatabase();

messageListener();
messageRemovedListener();
