window.onload = function () {
console.log("loaded");

    $('.basket_list').on('change',
        'input[type="number"]',
        function (event) {
            var t_href = event.target;
            $.ajax({
                url: "/basket/update/" + t_href.name + "/" + t_href.value + "/",
                success: function (data) {
                    $('.basket_list').html(data.result);
            },
        });
        event.preventDefault();
    });
};