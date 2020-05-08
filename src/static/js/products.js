$(document).ready(function() {
    $('#search-btn').on('click', function(e) {
        console.log('Button pressed');
        e.preventDefault();
        var searchText = $('#search-box').val();
        console.log(searchText);
        $.ajax( {
            url: '/products/?search_filter=' + searchText,
            type: 'GET',
            success: function(resp) {
                console.log(resp.data)
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
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
    function do_ajax(e, searchText) {
        $.ajax( {
            url: '/products/?search_filter=' + searchText,
            type: 'GET',
            success: function(resp) {
                console.log(resp.data)
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
            error: function(xhr, status, error) {
                console.error(error);
            }
        })
    }
    $("#video-games").click(function(e){
        console.log('Video games pressed');
        e.preventDefault();
        do_ajax(e,'Video Games');
    });
    $("#consoles").click(function(e){
        console.log('Consoles pressed');
        e.preventDefault();
        do_ajax(e,'Consoles');
    });
    $("#accessories").click(function(e){
        console.log('Accessories pressed');
        e.preventDefault();
        do_ajax(e,'Accessories');
    });
    $("#used").click(function(e){
        console.log('Used pressed');
        e.preventDefault();
        do_ajax(e,'Used');
    });
});