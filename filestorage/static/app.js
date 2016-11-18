$(document).ready(function() {
    // Hide upload result block
    $("#upload-results-block").hide();
    // Add eventhandler to upload file when form is submitted
    $("#upload-submit-button").on("click", function() {
        var file_data = $("#input-file").prop("files")[0];
        var form_data = new FormData();
        form_data.append('file', file_data);                           
        $.ajax({
            url: "/files",
            dataType: 'script',
            cache: false,
            contentType: false,
            processData: false,
            data: form_data,                         
            type: 'PUT',
            success: function(response_text){
                response = $.parseJSON(response_text);
                displayAttributes = ['uuid', 'key', 'name', 'size', 'create_utc', 'md5', 'sha1', 'sha256'];
                listHtml = "<dl>";
                for(i=0; i<displayAttributes.length; i++) {
                    key = displayAttributes[i];
                    listHtml += "<dt>" + key + "</dt><dd>" + response[key] + "</dd>";
                }
                listHtml += "</dl>";
                $("#result-uuid").html(response["uuid"]);
                $("#result-key").html(response["key"]);
                $("#upload-results-block #attributes").html(listHtml);
                $("#upload-raw-response").html(response_text);
                $("#upload-form-block").hide();
                document.getElementById("input-file").value = '';
                $("#upload-results-block").show();
            }
        });
        // End of $.ajax()
    });
    // Add eventhandler to display upload form after uploading a file
    $("#button-new-upload").on("click", function() {
        $("#upload-results-block").hide();
        $("#upload-form-block").show();
    });
    // That's it!
});