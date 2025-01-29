$(document).on('click', '#toggle-product', function (e) {
    var prodid = $(this).data('index');
    $.ajax({
      type: 'POST',
      url: '{% url "store:all_product" %}',
      data: {
        productid: $(this).data('index'),
        csrfmiddlewaretoken: "{{csrf_token}}",
        action: 'post'
      },
      success: function (json) {
        var item = json[0];
        var product = json[0].fields;
        var URL = 'http://127.0.0.1:8000/';
        document.getElementById("product-title").innerHTML = product.title;
        document.getElementById("product-price").innerHTML = product.price;
        document.getElementById("product-description").innerHTML = product.description;
        $('#product-image').attr('src', URL + 'media/' + product.image);
        $('#absolute-url').attr('href', URL + 'item/' + product.slug);
        $('.product-short-details .add-product').attr('data-index', item.pk);
      },
      error: function (xhr, errmsg, err) {
        console.log(err);
      }
    });
  });
  $(document).on('click', '.add-product', function (e) {
    e.preventDefault();
    var prodid = $(this).data('index');
    $.ajax({
      type: 'POST',
      url: '{% url "basket:basket_add" %}',
      data: {
        productid: prodid,
        productqty: 1,
        csrfmiddlewaretoken: "{{csrf_token}}",
        action: 'post'
      },
      success: function (json) {
        $("#success-load").load("{{ request.path }} .media-load");
        showSnackbar("Product added to Cart", "#4BCA81");
      },
      error: function (xhr, errmsg, err) {
        console.log(err)
      }
    });
  });
  $(document).on('click', '.add-wish', function (e) {
    e.preventDefault();
    var prodid = $(this).data('index');
    $.ajax({
      type: 'POST',
      url: '{% url "wishlist:add" %}',
      data: {
        product_id: prodid,
        csrfmiddlewaretoken: "{{csrf_token}}",
        action: 'post'
      },
      success: function (json) {
        console.log(json);
        showSnackbar("Product added to Wish", "#F260B5");
      },
      error: function (xhr, errmsg, err) {
        console.log(err)
      }
    });
  });