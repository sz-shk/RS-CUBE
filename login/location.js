window.onload = function() {
    askForLocation();
};

function askForLocation() {
    if (navigator.geolocation) {
        // Request the user's current position
        navigator.geolocation.getCurrentPosition(showLocation, locationError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function showLocation(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // Display the location or send it to your server
    alert("Your location: Latitude: " + latitude + ", Longitude: " + longitude);

    // Optionally, you could display this information on the page
    document.getElementById('username').innerText = ` (Location: ${latitude.toFixed(2)}, ${longitude.toFixed(2)})`;
}

function locationError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

function logout() {
    alert("You have logged out successfully!");
    // Redirect to login page or perform other logout actions.
    window.location.href = "login.html"; // Replace with your actual login page URL.
}

function startDashboard() {
    alert("Going to the Dashboard...");
    // Navigate to the dashboard or handle the action accordingly.
    window.location.href = "dashboard.html"; // Replace with actual dashboard page.
}