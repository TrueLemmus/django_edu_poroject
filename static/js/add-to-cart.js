$('#catalog').on('click', function () {
  var target = event.target;;
  
  $.ajax({
      url: '/baskets/add/' + target.dataset.product_id + '/',
      success: function (data) {
          $("#notification").fadeIn("slow").text(data.result);
          $("#notification").delay(2000).fadeOut("slow");
      },
  });
});