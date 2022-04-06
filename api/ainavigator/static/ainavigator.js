// javascript function that sends form data to server
function submitRobotForm(form) {
    jform = $(form);
    $.ajax({
        type: "POST",
        url: form.action,
        data: jform.serialize(),
        success: function (data) {
            jform.trigger("reset");
            if (data['status'] != 'success')
                return;
            // redirect to the url, relative to the current page
            let oldPath = window.location.pathname+window.location.search;
            let oldHash = window.location.hash;
            window.location.assign(data['result']);
            if (oldPath == window.location.pathname+window.location.search){
                // if the page is the same but hash changed, we need to reload the page
                if (oldHash != window.location.hash){
                    window.location.reload();
                }
            }
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
