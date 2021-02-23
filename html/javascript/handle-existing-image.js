function getPreSignedURL(imBlob, nameOfFile, typeOfFile) {
    const apigw_endpt = "https://mk4tkjgt8k.execute-api.ca-central-1.amazonaws.com/api";

    if (nameOfFile.length > 0) {
        // Output computed file name to webpage
        $("#name_of_file").html('<center><b>Name of New Image File:</b> ' + nameOfFile + '</center>');
        $.ajax({
            // The URL for the request
            url: apigw_endpt + "/generate_presigned_url",
            // The data to send (will be converted to a query string)
            data: {
                file_name: nameOfFile, sid: Math.random()
            },
            type: "GET",
            // The type of data expected back
            dataType: "json",
            // Code to run if the request succeeds;
            // the response is passed to the function
            success: function (json) {
                handleData(json, imBlob, typeOfFile);
            },
            // Code to run if the request fails; the raw request and
            // status codes are passed to the function
            error: function (xhr, status, errorThrown) {
                jq_ui_alert('dialog-message', "There was an AJAX problem with the getPreSignedURL function.");
                console.log("Error: " + errorThrown);
                console.log("Status: " + status);
                console.dir(xhr);
            }
        });
    } else {
        jq_ui_alert('dialog-message', "Invalid name for the new image file.");
    }
}

function handleData(json, imBlob, typeOfFile) {
    // Output S3 Pre-Signed URL to webpage
    //$("#psurl_result").html('<b>PreSigned URL:</b> ' + json.fields);
    console.log("Status Return: " + json.status);
    //console.log("PreSign Return: " + json.fields);
    $.ajax({
        headers: { 'x-amz-acl': 'public-read' },
        url: json.fields,
        type: 'PUT',
        contentType: typeOfFile,
        data: imBlob,
        processData: false,
        xhr: function () {
            var xhr = $.ajaxSettings.xhr();
            if (xhr.upload) {
                var progressbar = $("<div>", { style: "background:#607D8B;height:10px;margin:10px 0;" }).appendTo("#results"); //create progressbar
                xhr.upload.addEventListener('progress', function (event) {
                    var percent = 0;
                    var position = event.loaded || event.position;
                    var total = event.total;
                    if (event.lengthComputable) {
                        percent = Math.ceil(position / total * 100);
                        progressbar.css("width", + percent + "%");
                    }
                }, true);
            }
            return xhr;
        }
    }).done(function (response) {
        document.getElementById("analysis_button").style.visibility = "visible";
        var url = $(response).find("Location").text(); //get file location
        var the_file_name = $(response).find("Key").text(); //get uploaded file name
        jq_ui_alert('dialog-message', "Successful upload to S3 using pre-signed url.");
        //$("#results").html("<span>File has been uploaded, Here's your file <a href=" + url + ">" + the_file_name + "</a></span>"); //response
        $("#upload_result").html('<b>Upload Result:</b> Success');
        console.log("Upload Result: Success");
    });
}