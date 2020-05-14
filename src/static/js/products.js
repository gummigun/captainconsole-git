var products = {'data': []};
var products_filtered = {'data': []};


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
    $.ajax( {
        url: '/products/?query=' + searchText,
        type: 'GET',
        success: function(resp) {
            console.log('data', resp.data)
            products_filtered['data'] = resp.data
            map_data()
        },
        error: function(xhr, status, error) {
            console.error(error);
            return {}
        }
    });
}

function filter_data(items, filter_type) {
    let items_str = Array.from(items).join('$')
    console.log(items_str)
    $.ajax( {
        url: '/products/?filter=' + items_str + '&filterby=' + filter_type,
        type: 'GET',
        success: function(resp) {
            console.log('data', resp.data)
            products_filtered['data'] = resp.data
            map_data()
        },
        error: function(xhr, status, error) {
            console.error(error);
            return {}
        }
    });
}

$(document).ready( function() {
    console.log( "ready!" );

    $('#search-btn').on('click', function(e) {
        console.log('Button pressed');
        e.preventDefault();
        var searchText = $('#search-box').val();
        get_data( searchText)
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
    // get_data('')
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

let filtered = new Set()

$('#byConsole').on('click', function() {
    $("input:checkbox").each(function(){
        console.log('Checkbox pressed');

        let $this = $(this);

        if($this.is(":checked")) {
            filtered.add($this.attr("id"));
        } else {
            filtered.delete($this.attr("id"))
        }

    });
    filter_data(filtered, 'console')
});

$('#byCategory').on('click', function() {
    $("input:checkbox").each(function(){
        console.log('Checkbox pressed');

        let $this = $(this);

        if($this.is(":checked")) {
            filtered.add($this.attr("id"));
        } else {
            filtered.delete($this.attr("id"))
        }

    });
    filter_data(filtered, 'category')
});

$('#byCondition').on('click', function() {
    $("input:checkbox").each(function(){
        console.log('Checkbox pressed');

        let $this = $(this);

        if($this.is(":checked")) {
            filtered.add($this.attr("id"));
        } else {
            filtered.delete($this.attr("id"))
        }

    });
    filter_data(filtered, 'condition')
});