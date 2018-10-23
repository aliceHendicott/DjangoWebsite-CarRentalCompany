function changeTimeframe() {
    current = document.getElementById("timeframe_press").innerHTML.toLowerCase()
    if (current == 'month') {
        next = 'year'
    } else if (current == 'year') {
        next = 'day'
    } else {
        next = 'month'
    }
    document.getElementById("timeframe_press").innerHTML = next.toUpperCase();
}

function exportCSV() {
    document.getElementById("hidden_start_date").value = document.getElementById("start_date").innerHTML;
    document.getElementById("hidden_end_date").value = document.getElementById("end_date").innerHTML;
    document.getElementById("formCSV").submit()
}


function LoadAnswer(answerID) {
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
