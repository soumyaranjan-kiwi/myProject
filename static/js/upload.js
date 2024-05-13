function uploadFile() {
    var form = document.getElementById("uploadForm");
    var formData = new FormData(form);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "{% url 'fileupload' %}", true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                console.log(xhr.responseText);
                // Handle success response here
            } else {
                console.error("Error:", xhr.status, xhr.statusText);
                // Handle error response here
            }
        }
    };

    xhr.send(formData);
}
