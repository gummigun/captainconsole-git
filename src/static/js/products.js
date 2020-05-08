$(document).ready(function() {
    $('#search-btn').on('click', function(e) {
        console.log('Button pressed');
        e.preventDefault();
        var searchText = $('#search-box').val();
        console.log(searchText);
        $.ajax( {
            url: '/products?search_filter=' + searchText,
            type: 'GET',
            success: function(resp) {
                var newHtml = resp.data.map(d => {
                    return `<a href="/products/{{ product.id }}" class="SingleProduct">
                                <img class="SingleProduct__image"
                                  src="{{ product.productimage_set.first.images }}" alt="">
                                <div class="SingleProduct__generalDesrciption">
                                  <div class="SingleProduct__namePriceWrapper">
                                    <span class="SingleProduct__name">{{ product.name }}</span>
                                    <span class="SingleProduct__price">{{ product.price }}</span>
                                  </div>
                                  <span class="SingleProduct__type">{{ product.category }}</span>
                                </div>
                            </a>`
                });
                $('.Products').html(newHtml.join(''));
                $('#search-box').val('');
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        })
    });
});