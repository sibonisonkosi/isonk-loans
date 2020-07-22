$(document).ready(function(){


    //This part was never used
    $('.show-form').click(function () {
        $.ajax({
            url: '/dashboard/create-loan',
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#modal-loan').modal('show')
            },
            // success:function (data) {
            //     $('#modal-loan .modal-content').html(data.html_form);
            // }
        });
    });
    
    $('#modal-loan').on('submit','.create-form', function () {
        var form = $(this);
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',
            success: function (data) {
                if(data.form_is_valid){
                    console.log('data is saved');
                }
                else {
                    $('#modal-loan .modal-content').html(data.html_form)
                }
            }
        });
        return false
        
    })
    //End her



});