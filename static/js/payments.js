var stripe = Stripe('pk_test_51JQ0vKAMyq8PpY7xNS3m6EhB29HUGSx7OmmONegcvVV33bjPYcWLyfTiVhsHZKOQ2oFmtpDoSPqhFMqUOP85ANRG00x84FF9MS')
var elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
    base: {
        color: "#000",
        lineHeight: '6.4',
        fontSize: '16px'
    }
};

var card = elements.create("card", {
    style: style
});
card.mount("#card-element");
card.on('change', function (event) {
    var displayError = document.getElementById('card-errors')
    if (event.error) {
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert alert-info');
    } else {
        displayError.textContent = '';
        $('#card-errors').removeClass('alert alert-info');
    }
});

var form = document.getElementById('payment-form');
form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var custName = document.getElementById("custName").value;
    var custAdd = document.getElementById("custAdd").value;
    var custAdd2 = document.getElementById("custAdd2").value;
    var postCode = document.getElementById("postCode").value;

    var URL = 'https://pratamailham.pythonanywhere.com/order/add/'

    $.ajax({
        type: "POST",
        url: URL,
        data: {
            order_key: clientsecret,
            csrfmiddlewaretoken: CSRF_TOKEN,
            action: "post",
        },
        success: function (json) {
            console.log(json.success)

            stripe.confirmCardPayment(clientsecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        address: {
                            line1: custAdd,
                            line2: custAdd2
                        },
                        name: custName
                    },
                }
            }).then(function (result) {
                if (result.error) {
                    console.log('payment error')
                    console.log(result.error.message);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        console.log('payment processed')
                        // There's a risk of the customer closing the window before callback
                        // execution. Set up a webhook or plugin to listen for the
                        // payment_intent.succeeded event that handles any business critical
                        // post-payment actions.
                        window.location.replace("https://pratamailham.pythonanywhere.com/payment/orderplaced/");
                    }
                }
            });

        },
        error: function (xhr, errmsg, err) {},
    });

});