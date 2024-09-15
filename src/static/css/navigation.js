function setNavigation(value){
    document.getElementById("navigation").replaceChildren();  // Clears element

    var div_name = document.createElement("div");
    div_name.style.width = "500px";
    div_name.style.height = "50px";
    div_name.style.background = "green";
    div_name.style.color = "white";
    // div.innerHTML = "Hello";
    div_name.innerHTML = value["name"];

    document.getElementById("navigation").appendChild(div_name);

    var div_info_brief = document.createElement("div");
    div_info_brief.style.width = "500px";
    div_info_brief.style.height = "50px";
    div_info_brief.style.background = "blue";
    div_info_brief.style.color = "white";
    div_info_brief.innerHTML = value["info_brief"];

    document.getElementById("navigation").appendChild(div_info_brief);

    console.log(value["connections"]);

    value["connections"].forEach(addButton);
}

function addButton(destinationName) {
    var button = document.createElement("BUTTON");
    button.style.width = "500px";
    button.style.height = "50px";
    button.style.background = "orange";
    button.style.color = "white";
    button.innerHTML = destinationName;
    button.addEventListener('click', function(){
        getLocationInfo(destinationName);
    });

    document.getElementById("navigation").appendChild(button);
}

function getLocationInfo(name) {
    const apiUrl = 'http://localhost:5000/location/' + name.replaceAll("/", "|"); // Allows names with "/" to be processed
    console.log(apiUrl);
    fetch(apiUrl).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // return response.json();
        // console.log(response.json());
        // results = response.json();
        // results = response.json();
        // initMap();
        return response.json();
    }).then(data => {
        // Display data in an HTML element
        // results = JSON.stringify(data, null, 2);
        console.log("This is the data: ");
        console.log(data);
        setNavigation(data);
    // initMap();
    // outputElement.textContent = JSON.stringify(data, null, 2);
    }).catch(error => {
        console.error('Error:', error);
    });
}

const name = "B-30 - Mirasol/Rubí";
getLocationInfo(name);