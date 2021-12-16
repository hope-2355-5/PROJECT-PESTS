$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (res) {
                // if (data == "Tidak Menggunakan Masker !") {
                //     // Get and display the result
                //$('.loader').hide();
                //$('#result').fadeIn(600);
                //$('#result').html(`<h3 style="color: #dc3545;">${preds}</h3>`);
                //console.log('Success!');
                // } else if (data == "Masker Terdeteksi") {
                    // Get and display the result     
                    //#28a745
                console.log(res)
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').html(`<h3 style="color: #FF4500;">${res}</h3>`);
                //$('#result').html(`<h3 style="color: #FF4500;">${res}</h3>`);
                console.log('Success!');
                // }
                
            },
        });
    });

});
