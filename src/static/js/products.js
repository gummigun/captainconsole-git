function do_ajax(e, searchText) {
        console.log(searchText)
        $.ajax( {
            url: '/products/search/?query=' + searchText,
            type: 'GET',
            success: function(resp) {
                console.log('data', resp.data)

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

$(document).ready( function() {
    console.log( "ready!" );

    $('#search-btn').on('click', function(e) {
        console.log('Button pressed');
        e.preventDefault();
        var searchText = $('#search-box').val();

    });
    $("#video-games").click(function(e){
        console.log('Video games pressed');
        var pathname = window.location.pathname;
        if( pathname.includes('video_games')) {
            e.preventDefault();
        }
    });
    $("#consoles").click(function(e){
        console.log('Consoles pressed');
        var pathname = window.location.pathname;
        if( pathname.includes('consoles')) {
            e.preventDefault();
        }

    });
    $("#accessories").click(function(e){
        console.log('Accessories pressed');
        var pathname = window.location.pathname;
        if( pathname.includes('accessories')) {
            e.preventDefault();
        }
    });
    $("#used").click(function(e){
        console.log('Used pressed');
        var pathname = window.location.pathname;
        if( pathname.includes('used')) {
            e.preventDefault();
        }

    });
});

$(window).on('load', function () {
    console.log('loaded')
    if( window.location.pathname.includes('video_games')) {
        $('#pc-video-games').prop('checked', true);
    }
    else if( window.location.pathname.includes('consoles')) {
        $('#pc-consoles').prop('checked', true);
    }
    else if( window.location.pathname.includes('accessories')) {
        $('#pc-accessories').prop('checked', true);
    }
    else if( window.location.pathname.includes('used')) {
        $('#cond-used').prop('checked', true);
    }
});