var products = {
    'data': []
};
var products_filtered = {
    'data': []
};


function map_data() {
    var newHtml = products_filtered.data.map(d => {
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
}

function get_data(searchText) {
    $.ajax({
        url: '/products/?query=' + searchText,
        type: 'GET',
        success: function (resp) {
            products_filtered['data'] = resp.data
            map_data()
        },
        error: function (xhr, status, error) {
            console.error(error);
            return {}
        }
    });
}

function filter_data(items, filter_type) {
    $.ajax({
        url: '/products/all/?filter=' + items + '&filterby=' + filter_type,
        type: 'GET',
        success: function (resp) {
            products_filtered['data'] = resp.data
            map_data()
        },
        error: function (xhr, status, error) {
            console.error(error);
            return {}
        }
    });
}

function order_data(items) {
    $.ajax({
        url: '/products/all/?order=' + items,
        type: 'GET',
        success: function (resp) {
            products_filtered['data'] = resp.data
            map_data()
        },
        error: function (xhr, status, error) {
            console.error(error);
            return {}
        }
    });
}

$(document).ready(function () {
    $('#search-btn').on('click', function (e) {
        var pathname = window.location.pathname;
        var searchText = $('#search-box').val();

        e.preventDefault();

        if (pathname.includes('products')) {
            get_data(searchText)

        } else {
            window.location.href = '/products/all/?search=' + searchText;
        }
    });
    $("#video-games").click(function (e) {
        var pathname = window.location.pathname;
        if (pathname.includes('video_games')) {
            e.preventDefault();
        }
    });
    $("#consoles").click(function (e) {
        var pathname = window.location.pathname;
        if (pathname.includes('consoles')) {
            e.preventDefault();
        }

    });
    $("#accessories").click(function (e) {
        var pathname = window.location.pathname;
        if (pathname.includes('accessories')) {
            e.preventDefault();
        }
    });
    $("#used").click(function (e) {
        var pathname = window.location.pathname;
        if (pathname.includes('used')) {
            e.preventDefault();
        }

    });
    $('.Orderby_button').click(function () {
        let val = $(this).attr("value");
        var pathname = window.location.pathname;
        if (pathname.includes('products')) {
            order_data(val)
        }
    });
});

$(window).on('load', function () {
    // get_data('')
    if (window.location.pathname.includes('video_games')) {
        $('#pc-video-games').prop('checked', true);
    } else if (window.location.pathname.includes('consoles')) {
        $('#pc-consoles').prop('checked', true);
    } else if (window.location.pathname.includes('accessories')) {
        $('#pc-accessories').prop('checked', true);
    } else if (window.location.pathname.includes('used')) {
        $('#cond-used').prop('checked', true);
    }
});

$('#byConsole').on('click', function () {
    $("#byConsole").children('input').each(function () {
        let $this = $(this);
        if ($this.is(":checked")) {
            filter_data($this.attr("value"), 'console')
        }
    });
});

$('#byCategory').on('click', function () {
    $("#byCategory").children('input').each(function () {
        let $this = $(this);
        if ($this.is(":checked")) {
            filter_data($this.attr("value"), 'category')
        }
    });
});

$('#byCondition').on('click', function () {
    $("#byCondition").children('input').each(function () {
        let $this = $(this);
        if ($this.is(":checked")) {
            filter_data($this.attr("value"), 'condition')
        }
    });
});