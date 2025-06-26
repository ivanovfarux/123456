document.addEventListener('DOMContentLoaded', function() {
    var checkbox = document.getElementById('statusCheckbox');

    checkbox.addEventListener('change', function() {
        var isChecked = this.checked; // true if checked, false if unchecked
        
        // Simulate sending the status to the backend using AJAX
        // Replace this with your actual AJAX call to send the status to the server
        if (isChecked) {
            // Send value "1" to the backend
            sendStatusToBackend("1");
        } else {
            // Send value "0" to the backend
            sendStatusToBackend("0");
        }
    });
    
    function sendStatusToBackend(statusValue) {
        // Here you would implement your AJAX call to send the status to the server
        // Example using fetch API
        fetch('/update-status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ status: statusValue })
        })
        .then(response => {
            // Handle response if needed
            console.log('Status sent successfully');
        })
        .catch(error => {
            console.error('Error sending status:', error);
        });
    }
});
console.log("ishladi.");