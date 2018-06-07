function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var fileM = document.querySelector('#img-file');
$(document).ready(function() {
    $('#form-avatar').submit(function(evt) {
        evt.preventDefault();
        var fileObj = fileM.files[0];
        var formdata = new FormData();
        formdata.append("avatar", fileObj);
        $.ajax({
            url: '/user/user/',
            type: 'PUT',
            datatype: 'json',
            data: formdata,
            async: false,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                $('#user-avatar').attr('src', data.url);
            },
            error: function () {
                alert('上传失败')
            }
        })
    });

    $('#form-name').submit(function(evt) {
        evt.preventDefault();
        var name = $('#user-name').val();
        $.ajax({
            url: '/user/user/',
            type: 'PUT',
            datatype: 'json',
            data: {'name': name},
            success: function (data) {
                if (data.code == '200'){
                    $('.popup_con').show()
                    $('.error-msg').hide()
                }else if(data.code == '1007'){
                    $('.error-msg').show()
                    $('.popup_con').hide()
                    // $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>' + data.msg)
                }
            },
            error: function () {
                alert('保存失败')
            }
        })
    });

    $('.popup_con').click(function() {
        $('.popup_con').hide()
    })
});


// 上传头像另一种写法
// $('#form-avatar').submit(function () {
//
//     $(this).ajaxSubmit({
//         url: '/user/user/',
//         type: 'PUT',
//         dataType: 'json',
//         success: function (data) {
//             if(data.code == '200'){
//                 $('#user-avatar').attr('src', data.url)
//             }
//         },
//         error: function (data) {
//             alert('上传头像失败');
//         }
//     });
//
//     return false
// });