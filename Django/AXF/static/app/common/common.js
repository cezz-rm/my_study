
function addShop(good_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url:'/axf/addgoods/',
        type: 'POST',
        data: {'good_id': good_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            $('#num_' + good_id ).html(msg.c_num)
        },
        error: function (msg) {
            alert('请求错误')
        }
    })
}

function subShop(good_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url:'/axf/subgoods/',
        type: 'POST',
        data:{'good_id': good_id},
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        success: function (msg) {
            $('#num_' + good_id).html(msg.c_num)
        },
        error: function (msg) {
           alert('减少失败')
        }
    })
}

function cartchangeselect(cart_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
        $.ajax({
            url:'/axf/changeCartSelect/',
            type:'POST',
            data:{'cart_id': cart_id},
            dataType: 'json',
            headers:{'X-CSRFToken': csrf},
            success:function (msg) {
                if(msg.is_select){
                    s = '<span onclick="cartchangeselect(' + cart_id + ')">√</span>'
                }else {
                    s = '<span onclick="cartchangeselect(' + cart_id + ')" style="width: 40px; height: 40px; background-color: white"></span>'
                }
                $('#changeselect_' + cart_id).html(s)
            },
            error:function (msg) {
                alert('更改失败..')
            }
        })
}


function allselect(status) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/axf/allSelect/',
        type: 'POST',
        dataType: 'json',
        headers: {'X-CSRFToken': csrf},
        data: {'status': status},
        success: function (msg) {
            if(msg.is_select){
                s = '<span onclick="allselect(' + 1 + ')">√</span>';
            }else{
                s = '<span onclick="allselect(' + 0 + ')" style="width: 40px; height: 40px; background-color: white"></span>';
            }
                $('#allselect').html(s);
                changeAll(msg.is_select);
        },
        error: function () {
            alert('全选失败')
        }
    })

}


function changeAll(msg) {
    if (msg){
        $('.is_choose > span').html('√').css("background-color","yellow");;
        // $('#allselect > span').text('√');
    }else{
        $('.is_choose > span').html('&nbsp;').css("background-color","white");
        // $('#allselect > span').html(ni);
    }
}









