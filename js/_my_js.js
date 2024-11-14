// Function to get the current year and set it to an element with a specific ID
function setCurrentYear(elementId) {
    const currentYear = new Date().getFullYear();
    document.getElementById(elementId).textContent = currentYear;
}


document.addEventListener("DOMContentLoaded", function () {
    // Fetch the footer.html file
    fetch('footer.html')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            // Inject the footer content into the placeholder
            document.getElementById('footer-placeholder').innerHTML = data;

            // Optional: Update the year dynamically
            const currentYear = new Date().getFullYear();
            document.getElementById('currentYear').textContent = currentYear;
        })
        .catch(error => {
            console.error('Error loading footer:', error);
        });
});
