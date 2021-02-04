function handleData(json, imBlob) {
    // Output S3 Pre-Signed URL to webpage
    //$("#psurl_result").html('<b>PreSigned URL:</b> ' + json.fields);
    console.log("Status Return: " + json.status);
    console.log("PreSign Return: " + json.fields);
    $.ajax({
        headers: { 'x-amz-acl': 'public-read' },
        url: json.fields,
        type: 'PUT',
        contentType: 'image/png',
        data: imBlob,
        processData: false,
        success: function (data) {
            jq_ui_alert('dialog-message', "Successful upload to S3 using pre-signed url.");
            // Output success message to webpage
            $("#upload_result").html('<b>Upload Result:</b> Success');
            console.log("Upload Result: Success");
        },
        error: function (xhr, status, errorThrown) {
            jq_ui_alert('dialog-message', "Unsuccessful upload to S3 using pre-signed url.");
            // Output failure message to webpage
            $("#upload_result").html('<b>Upload Result:</b> Failed');
            console.log("Upload Result: Failed");
            console.log("Error: " + errorThrown);
            console.log("Status: " + status);
            console.dir(xhr);
        }
    });
}