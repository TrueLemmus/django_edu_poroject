window.onload = function () {
    $('.basket_list').on('click', 'input[type="number"]', function () {
        var target = event.target
        
        $.ajax({
            url: '/baskets/edit/' + target.name + '/' + target.value + '/',
            success: function (data) {
                $('.basket_list').html(data.result);
            },
        });
    });
}