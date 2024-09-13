document.addEventListener('DOMContentLoaded', function() {
    const citySelect = document.getElementById('city');
    const form = document.getElementById('demographics-form');

    form.addEventListener('submit', function(e) {
        if (citySelect.value === "") {
            e.preventDefault();
            alert('Please select a valid city from the list.');
        }
    });
});
