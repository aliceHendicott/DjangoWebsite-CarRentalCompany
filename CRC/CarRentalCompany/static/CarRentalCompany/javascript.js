function LoadAnswer(answerID){
    var answerDiv = document.getElementById(answerID);
    if(answerDiv.style.display == "block"){
        answerDiv.style.display = "none";
    } else{
        answerDiv.style.display = "block";
    }
}

function handleLogin() {

    var username = $('#id_username').val();
    var password = $('#id_password').val();
    var csrfmiddlewaretoken = $('input[name="csrfmiddlewaretoken"]').val();

    if (username.length == 0 || password.length == 0) {
        alert("Please enter a username and password");
        return;
    }

    var data = {
        username: username,
        password: password,
        csrfmiddlewaretoken: csrfmiddlewaretoken
    };

    sendForm('/loginjs/', data,
        function(rc, data) {
            location.reload();
        },
        function(xhr) {
            alert('invalid credentials');
        })

}

function sendForm(address, formData, successCallback, errorCallback) {
    $.post(address, formData, function (data) {
        var rc = data.response;
        successCallback(rc, data);
    }).fail(function (xhr, status, error) {
        errorCallback(xhr);
    });
}

function sortStores() {
    $('#sort-div-stores').load(document.location + ' #sort-div-stores');
}

function getGeoLocation(callback) {

        // User isn't using chrome
        // Proceed with geolocation
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function (currentPosition) {
                var response = {latitude: currentPosition.coords.latitude, longitude: currentPosition.coords.longitude};
                if (callback !== undefined) {
                    callback(response);
                }
            });

        } else {
            throw "Geolocation is not currently enabled.";
        }
}
//Calling geolocation
// try {
//     getGeoLocation(function(data) {
//         console.log(data);
//     });
// } catch {
//     console.log("geolocation not enabled");
// }

function dynamicSort(property) {
    var sortOrder = 1;
    if(property[0] === "-") {
        sortOrder = -1;
        property = property.substr(1);
    }
    return function (a,b) {
        var result = (a[property] < b[property]) ? -1 : (a[property] > b[property]) ? 1 : 0;
        return result * sortOrder;
    }
}

function sortCarsList(element) {
    var sortBy = $(element).val;
    if (sortBy == "make"){
        cars_json.sort(dynamicSort("car_makename"))
    }
    if (sortBy == "body"){
        cars_json.sort(dynamicSort("car_bodytype"))
    }
    if (sortBy == "price"){
        cars_json.sort(dynamicSort("car_price_new"))
    }
    var data = {"new_car_list": cars_json}

}