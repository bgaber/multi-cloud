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

function getPreSignedURL(imBlob) {
    const apigw_endpt = "https://mk4tkjgt8k.execute-api.ca-central-1.amazonaws.com/api";

    var nameOfFile = `${parseInt(Math.random() * 10000000)}.png`;

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
                handleData(json, imBlob);
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