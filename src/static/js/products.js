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
                    return `<div class="single-product">
                                <a href="/products/$(d.id)">
                                    <img class="product-img" src="${d.firstImage}" alt=""/>
                                    <h4>Product: ${ d.name }</h4>
                                    <p>Category: ${ d.category }</p>
                                    <p>Price: ${ d.price }</p>
                                    <p>Description: ${ d.description }</p>
                                </a>
                            </div>`
                });
                $('.products').html(newHtml.join(''));
                $('#search-box').val('');
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        })
    });
});