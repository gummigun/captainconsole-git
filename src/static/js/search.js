$(document).ready(function () {
  $('#search-btn').on('click', function (e) {
    e.preventDefault();
    var searchText = $('#search-box').val();
    $.ajax({
      url: '/products/search/?query=' + searchText,
      type: 'GET',
      success: function (resp) {
        var newHtml = resp.data.map(d => {
          return `<a href="/products/${ d.id }" class="SingleProduct">
                                <img class="SingleProduct__image"
                                  src="${ d.firstImage }" alt="">
                                <div class="SingleProduct__generalDesrciption">
                                  <div class="SingleProduct__namePriceWrapper">
                                    <span class="SingleProduct__name">${ d.name }</span>
                                    <span class="SingleProduct__price">${ d.price }</span>
                                  </div>
                                  <span class="SingleProduct__type">${ d.category }</span>
                                </div>
                            </a>`
        });
        $('.Products').html(newHtml.join(''));
        $('#search-box').val('');
      },
      error: function (xhr, status, error) {
        console.error(error);
      }
    });
  });

  function do_ajax(e, searchText) {
    $.ajax({
      url: '/products/search/?query=' + searchText,
      type: 'GET',
      success: function (resp) {

        var newHtml = resp.data.map(d => {
          return `<a href="/products/${ d.id }" class="SingleProduct">
                                <img class="SingleProduct__image"
                                  src="${ d.firstImage }" alt="">
                                <div class="SingleProduct__generalDesrciption">
                                  <div class="SingleProduct__namePriceWrapper">
                                    <span class="SingleProduct__name">${ d.name }</span>
                                    <span class="SingleProduct__price">${ d.price }</span>
                                  </div>
                                  <span class="SingleProduct__type">${ d.category }</span>
                                </div>
                            </a>`
        });
        $('.Products').html(newHtml.join(''));
        $('#search-box').val('');
      },
      error: function (xhr, status, error) {
        console.error(error);
      }
    })
  }
});