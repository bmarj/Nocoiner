// javascript function that sends form data to server
function submitRobotForm(form) {
    jform = $(form);
    $.ajax({
        type: "POST",
        url: form.action,
        data: jform.serialize(),
        success: function (data) {
            jform.trigger("reset");
            // redirect to the url, relative to the current page
            window.location.href = data['result'];
        },
        error: function (data) {
            console.log('Error:', data);
        }
    });
}

document.forms['robotForm'].addEventListener('submit', (event) => {
    event.preventDefault();
    submitRobotForm(event.target);
});
