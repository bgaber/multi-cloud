function jq_ui_alert(div_id, theMESSAGE) {
    var theICON = '<span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 0 0;"></span>';
    $("#" + div_id).html('<P>' + theICON + theMESSAGE + '</P>');
    $("#" + div_id).dialog({
        modal: true,
        buttons: [{
            text: "OK",
            icon: "ui-icon-check",
            click: function () {
                $(this).dialog("close");
            }
        }]
    });
}

$(document).ready(function () {
    const apigw_endpt = "https://mk4tkjgt8k.execute-api.ca-central-1.amazonaws.com/api";

    // $("#get_psurl").click(function() {
    $("#aws_upload_form").submit(function (e) {
        e.preventDefault();
        var form_data = new FormData(this); //Creates new FormData object

        // Debug alert
        //jq_ui_alert('dialog-message', "File Selected");

        var selectedFile = document.getElementById('fileInput');
        var nameOfFile = selectedFile.files.item(0).name;

        if (nameOfFile.length > 0) {
            // Output selected file name to webpage
            $("#selectedFile").html('<b>Selected File:</b> ' + nameOfFile);
            $.ajax({
                // The URL for the request
                url: apigw_endpt + "/generate_presigned_url",
                // The data to send (will be converted to a query string)
                data: {
                    file_name: nameOfFile, sid: Math.random()
                },
                // Whether this is a POST or GET request
                type: "GET",
                // The type of data we expect back
                dataType: "json",
                // Code to run if the request succeeds;
                // the response is passed to the function
                success: function (json) {
                    handleData(json, form_data);
                },
                // Code to run if the request fails; the raw request and
                // status codes are passed to the function
                error: function (xhr, status, errorThrown) {
                    jq_ui_alert('dialog-message', "AJAX problem getting the S3 PreSigned URL for " + nameOfFile + " from the generate_presigned_url Lambda function.");
                    console.log("Error: " + errorThrown);
                    console.log("Status: " + status);
                    console.dir(xhr);
                },
                // Code to run regardless of success or failure
                complete: function (xhr, status) {
                    //jq_ui_alert( 'dialog-message', "The request is complete!" );
                }
            });
        } else {
            jq_ui_alert('dialog-message', "No File Selected");
        }
    });
});