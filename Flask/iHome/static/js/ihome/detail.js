function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}



$(document).ready(function () {
    var path = location.search;
    var id = path.split('=')[1] ;
    $.get('/house/detail/' + id + '/', function (data) {
        if (data.code == '200'){
            var detail_hosue = template('house_detail_list', {ohouse: data.house, facilitys: data.facility_list, booking: data.booking});
            $('.container').append(detail_hosue);

            var mySwiper = new Swiper ('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationType: 'fraction'
            });

            $(".book-house").show();

        }
    });
});


// $('#login_now').click(function () {
//   alert('1');
// });

function login_now() {
    var house_id = location.search.split('=')[1];
    location.href = '/user/login/?house_id=' + house_id;
}