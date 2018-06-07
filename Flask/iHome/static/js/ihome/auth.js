function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


$.get('/user/auths/', function (data) {
    if (data.code == '200'){
        $('#real-name').val(data.id_name).attr('disabled', true);
        $('#id-card').val(data.id_card).attr('disabled', true);
        $('.btn-success').hide()
    }
});

$('#form-auth').submit(function (evt) {
    evt.preventDefault();
    var real_name = $('#real-name').val();
    var id_card = $('#id-card').val();
    $.ajax({
        url: '/user/auths/',
        type: 'PUT',
        dataType: 'json',
        data: {'real_name': real_name, 'id_card': id_card},
        success: function (data) {
            if(data.code == '200'){
                $('.btn-success').hide();
                $('.error-msg').hide();
                $('.popup_con').show()

            }else{
                $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>' + data.msg);
                $('.error-msg').show()
            }
        },
        error: function (data) {
            alert('请求失败')
        }
    });

    $('.popup_con').click(function() {
        $('.popup_con').hide()
    })
});


