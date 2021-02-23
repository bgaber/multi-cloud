function jq_ui_alert(div_id, theMESSAGE) {
    var theICON = '<span class="ui-icon ui-icon-alert" style="float:left; margin:0 7px 0 0;"></span>';
    $("#" + div_id).html('<P>' + theICON + theMESSAGE + '</P>');
    $("#" + div_id).dialog({
        modal: true,
        buttons: {
            Ok: function () {
                $(this).dialog("close");
            }
        }
    });
}

// Fill the photo with an indication that none has been
// captured.

function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/jpeg');
    photo.setAttribute('src', data);
}

$(document).ready(function() {
    document.getElementById("upload_app").innerHTML = `
<h1>Image File Upload</h1>
<div>
<input type="file" id="fileInput" />
</div>
`;
    
    // stackoverflow.com/questions/21659810/load-image-from-local-path-and-draw-it-on-canvas
    // redstapler.co/load-image-to-canvas-javascript/

    const uploadFile = file => {
        const fileInput = document.querySelector("#fileInput");
        var fName = fileInput.files.item(0).name;
        var fType = fileInput.files.item(0).type;
        $("#name_of_file").html(fName);
        
        var canvas = null;
        var photo = null;
        
        canvas = document.getElementById('canvas');
        photo = document.getElementById('photo');
        var context = canvas.getContext('2d');
        
        var URL = window.webkitURL || window.URL;
        var url = URL.createObjectURL(file);
        var img = new Image();
        img.src = url;

        img_width = img.width;
        img_height = img.height;
        var new_x = 0;
        var new_y = 0;

        if (img_width > img_height) {
            new_x = 320;
            new_y = (320*img_height)/img_width;
        } 

        else if (img_height > img_width) {
            new_x = (320*img_width)/img_height;
            new_y = 320;
        }

        else {
            new_x = 320;
            new_y = 320;
        }

        canvas.width = new_x;
        canvas.height = new_y;

        clearphoto();

        img.onload = function () {
            context.drawImage(img, 0, 0, new_x, new_y);
            var data = canvas.toDataURL(fType);
            photo.setAttribute('src', data);

            canvas.toBlob(function (blob) {
                getPreSignedURL(blob, fName, fType); // hopefully save new image to S3
            });
        }
    };

    fileInput.addEventListener("change", event => {
      const files = event.target.files;
      uploadFile(files[0]);
    });
});