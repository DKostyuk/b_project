$(document).ready(function(){
    // console.log(1);

    $('.hidden-info').removeClass('hidden').hide();
    $('.btn-see-info').click(function() {
        $(this).find('span').each(function() { $(this).toggle(); });
    });

    $('.slider-for').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        asNavFor: '.slider-nav',
        autoplay: true
    });
    $('.slider-nav').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        asNavFor: '.slider-for',
        dots: false,
        centerMode: true,
        focusOnSelect: true
    });

    $("#category_name").change(function(){//подписываемся на событие
        var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
        var category_name = $("#category_name").val();
        var data = {};
        data["csrfmiddlewaretoken"] = csrf_token;
        data.category_name = category_name;
        console.log(data.category_name);
        console.log(data);
        console.log(77777777777);
        // console.log(url);
        console.log(category_name);
        $.ajax({
            url: '/test_ajax/',
            type: 'POST',
            data: data,
            cache: true,
            success: function(data) {
                console.log("OK");
                // console.log(data);
                // var xxx = data.category_name;
                console.log(data);
                console.log(Object.keys(data).length);
                console.log(4444444444444);
                $('#test_test').text("УСПЕХ");


                $('#subcategory_names').html("");
                for(var i=1;i < Object.keys(data).length+1;i++){
                    console.log(data[i]);
                    $('#subcategory_names').append('<input name="subcategory_name" type="radio" ' +
                        'required="required" value="' + data[i] +'">' + data[i]);
                }
            },
            error: function(){
               console.log("ERROR");
            }
        });
    });

    $(".navbar-home12").css("background-color","yellow");

    $('.navbar-nav a').each(function () {      // проходим по нужным нам ссылками
        var location = window.location.href; // переменная с адресом страницы
        var link = this.href;                // переменная с url ссылки
        var result = location.match(link);  // результат возвращает объект если совпадение найдено и null при обратном

        if(result != null) {                // если НЕ равно null
            // console.log(0000000);
            // console.log(location);
            // console.log(3333333);
            // console.log(link);
            // console.log(this);
            $(this).addClass('current');    // добавляем класс
            }
    });

   function basketUpdating(product_id, nmb, is_delete) {
       // ajax()
       var data ={};
       data.product_id = product_id;
       data.nmb = nmb;
       // data.price = price;
       var csrf_token = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();
       data["csrfmiddlewaretoken"] = csrf_token;

       if (is_delete){
            data["is_delete"] = true;
        }

       var url = form.attr("action");
       console.log("DATA_DATA_DATA");
       console.log(data);

       $.ajax({
           url: url,
           type: 'POST',
           data: data,
           cache: true,
           success: function (data) {
               console.log("OK");
               console.log(url);
               console.log(data);
               console.log(987);
               console.log(data.products_total_nmb);
               console.log(789);

               if (data.products_total_nmb || data.products_total_nmb == 0){
                   $('#basket_total_nmb').text("("+data.products_total_nmb+")");
                    console.log(data.products);
                   $('.basket-items ul').html("");
                   $.each(data.products, function(k, v){
                       $('.basket-items ul').append('<li>'+ v.name +', '+ v.nmb +' штук по ' + v.price_per_item + ' грн.          ' +
                            '<a class="delete-item" href="" data-product_id="'+v.id+'">X</a>'+
                            '</li>');
                       // $('.basket-items ul').append('<li>'+ v.name +', '+ v.nmb +' штук по '+ v.price_per_item +' грн.          ' +
                       //      '<a class="delete-item" href="" data-product_id="'+v.id+'">X</a>'+
                       //      '</li>');
                   })
               }
           },
           error: function(error){
               console.log("ERROR");
               console.log(JSON.stringify(error));
           }
       })
   }

   var form = $('#form_buying_product');

   form.on('submit', function (e) {
       e.preventDefault();
       console.log('258');
       var nmb = $('#number').val();
       var submit_btn = $('#submit_btn');
       var product_id = submit_btn.data("product_id");
       var product_name = submit_btn.data("name");

       basketUpdating(product_id, nmb, is_delete=false)

   });

    function showingBasket(){
       $('.basket-items').removeClass('hidden');
    }

    $('.basket-container').on('mouseover', function(e){
        e.preventDefault();
        showingBasket();
    });

    $('.basket-container').on('mouseout', function(e){
        e.preventDefault();
        $('.basket-items').addClass('hidden');
    });

    $(document).on('click','.delete-item', function(e){
        e.preventDefault();
        product_id = $(this).data("product_id");
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete=true)
    });

    function calculatingBasketAmount(){
        //console.log(123);
        var total_order_amount = 0;
        // проходим по каждому элементу с таким class (ИД может быть только у одного элемента на странице !!!!)
        $('.total-product-in-basket-amount').each(function(){
            // прибавляем с переменной то что взяли при проходе элемента
            total_order_amount +=parseFloat($(this).text()); //преобразовывает текст в число parseFloat
        });
        //console.log(total_order_amount);
        $('#total_order_amount').text(total_order_amount.toFixed(2)); // вписываем значение текстом на ИД
    };
    calculatingBasketAmount();

    $(document).on('change','.product-in-basket-nmb', function () { //отслеживаем изменения на классе
        var current_nmb = $(this).val(); // считыаем текущее кол-во и получаем значение в переменную
        var current_tr = $(this).closest('tr');//находим строку-ячейку где произошли изменения - ближайшая tr
        // console.log('current_tr   ', current_tr);
        var current_price = parseFloat(current_tr.find('.product-price').text()); // из этого ряда находим span
                                                                                  // с нужным классом.
                                                // из него берем текст и переводим с помощью ParseFloat в число
        var total_amount = parseFloat(current_nmb*current_price).toFixed(2); // получаем новую сумму, новое кол-во на сущ.цену
        current_tr.find('.total-product-in-basket-amount').text(total_amount); //находим в текущей строке span с нужным
                                        // классом и записываем туда текстом переменную - общую новую сумму по строке
        calculatingBasketAmount();
    });

    calculatingBasketAmount();

    // $("#show-hide").hide("drop", 9000);
    setTimeout(function() { $("#show-hide").hide("bounce", 'slow'); }, 1000);


    $('.service-slider').slick({
        infinite: true,
        slidesToShow: 3,
        slidesToScroll: 1
    });

});

$(document).ready(function(){
    // console.log(4055151);
    CKEDITOR.replace( 'id_description', {
        toolbar: [
            { name: 'document', groups: [ 'mode' ], items: [ 'Preview' ] },
            { name: 'clipboard', groups: [ 'undo' ], items: [ '-', 'Undo', 'Redo' ] },
            { name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ], items: [ 'Bold', 'Italic', 'Underline', 'Subscript', 'Superscript', '-' ] },
            { name: 'paragraph', groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ], items: [ 'NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-'] },
            { name: 'tools', items: [ 'Maximize'] }
            ]
    });
});


// Function for Google Map - Start
function initMapMy() {
    // console.log(2741913);
    var geo;
    var geoElement = document.getElementById('geoMap');
    var geoOptions = {
        zoom: 17
        // center: {lat: 52.280973, lng: 20.967678}
    };

    // console.log(geoElement);

    geo  = new google.maps.Geocoder();

    var geoMap  = new google.maps.Map(geoElement, geoOptions);


    var  open_map_btn = $('#open_map_btn');
    var cosmetolog_address = open_map_btn.data("cosmetolog_address");
    // console.log(cosmetolog_address);

    geo.geocode({'address': cosmetolog_address}, function (results, status){
        if(status == google.maps.GeocoderStatus.OK) {
            geoMap.setCenter(results[0].geometry.location);
            // var qwerty = results[0].geometry.location.lat();
            // console.log('qwerty', qwerty);
            var marker = new google.maps.Marker({
                map: geoMap,
                position: results[0].geometry.location
            });
        }
        else {
            alert('Адресс не найден');
        }
    });
}
// Function for Google Map - End

//autoComplete - Start
function Search() {
    $.fn.selectpicker.Constructor.BootstrapVersion = '4';
    $("#tags").autocomplete({
        minlength: 3,
        source: "/search_ajax/",
        select: function (event, ui) {
            var hiddenInput = document.getElementById("tags_48");
            hiddenInput.value = ui.item.id;
            // log( "Selected: " + ui.item.value + " aka " + ui.item.id );
        }
    });

    $("#tags_1").autocomplete({
        minlength: 3,
        source: "/search_ajax_service/",
        select: function (event, ui) {
            var hiddenInput = document.getElementById("tags_148");
            hiddenInput.value = ui.item.id;
        }
    });

    $("#tags_city").autocomplete({
        autoFocus: true,
        minlength: 3,
        source: "/search_ajax_city/",
        select: function (event, ui) {
            var hiddenInput = document.getElementById("tags_city_48");
            hiddenInput.value = ui.item.id;
            var city_id = ui.item.id;
            console.log('Popepostr');
            console.log(city_id);
            var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
            console.log(123456789);
            var data = {};
            data["csrfmiddlewaretoken"] = csrf_token;
            data.city_id = city_id;
            console.log(1);
            console.log(data.city_id);
            console.log(2);
            console.log(data);
            $.ajax({
                url: '/search_ajax_street/',
                type: 'POST',
                data: data,
                cache: true,
                success: function (data) {
                    console.log("OK");
                    console.log(data);
                    $("#tags_street").autocomplete({
                        minlength: 3,
                        source: data,
                        select: function (event, ui) {
                            var hiddenInput = document.getElementById("tags_street_48");
                            hiddenInput.value = ui.item.id;
                        }
                    });
                },
                error: function () {
                    console.log("ERROR");
                }
            });
        }
    });
}
Search();



// form.on('submit', function (e) {
   //     e.preventDefault();
   //     var address123 = $('#tags').val();
   //     console.log(address123);
   //
   // });

//autoComplete - End