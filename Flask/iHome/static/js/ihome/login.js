function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        // e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        // if (!mobile) {
        //     $("#mobile-err span").html("请填写正确的手机号！");
        //     $("#mobile-err").show();
        //     return;
        // }
        // if (!passwd) {
        //     $("#password-err span").html("请填写密码!");
        //     $("#password-err").show();
        //     return;
        // }
        var path = location.search;
        var house_id = path.split('=')[1];
        $.ajax({
            url:'/user/login/',
            type: 'POST',
            dataType: 'json',
            data: {'mobile': mobile, 'password': passwd, 'house_id': house_id},
            success: function (data) {
                if (data.code == '200'){
                    if (data.house_id){
                        location.href = '/house/detail/?id=' + data.house_id
                    }else {
                        location.href='/user/my/'
                    }

                }
            },
            error:function (data) {
                alert(data.msg)
            }
        });


    });
})