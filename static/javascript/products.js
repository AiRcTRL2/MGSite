// Location of flask app
ROOT = window.location.origin;
var products_url = ROOT + '/getproducts/';
var product_url = ROOT + '/getproduct/';

product_dict = {}

function getProduct(productName) {
    var dict_id = String($(productName).attr("id"))
//    console.log(productName.childNodes[1].childNodes[9].innerHTML)
//    console.log($(productName).attr($('[id*="zoid-paypal-button"]')))
    
    $.getJSON((product_url+$(productName).attr("id")), function(data){
//        console.log(data);
    }).then(function() {
        var modal = document.getElementById("myModal");
        
        $( '.image-box' ).html(`<img src=${product_dict[dict_id]['Images'][0]}>`);
        $( '.item-price' ).html(`<span class="currency-symbol">€</span>${product_dict[dict_id]['price']}`);
        getPaypalButton(product_dict[dict_id], product_dict, true, 'large');
        modal.style.display = "block";
        
        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];

        // When the user clicks on <span> (x), close the modal
        span.onclick = function() {
          modal.style.display = "none";
          $( '#buy-now').html("");
        }

        // When the user clicks anywhere outside of the modal, close it
        window.onclick = function(event) {
          if (event.target == modal) {
            modal.style.display = "none";
            $( '#buy-now').html("");
          }
        }
        })
};

function getPaypalButton(key, data, modalBool, buttonSize) {
    if (!modalBool) {
        var string = "b" + data['ID'];
    } else {
        var string = "buy-now"
    };
    
    console.log(data['ID'])
    

    var CREATE_PAYMENT_URL  = ROOT + '/payment/';
    var EXECUTE_PAYMENT_URL = ROOT + '/execute';
    paypal.Button.render({
        env: 'sandbox', // Or 'sandbox'
        commit: true, // Show a 'Pay Now' button
        payment: function() {
            return paypal.request.post(CREATE_PAYMENT_URL+data['ID']).then(function(data) {
                return data.paymentID;
            });
        },
        onAuthorize: function(data) {
            return paypal.request.post(EXECUTE_PAYMENT_URL, {
                paymentID: data.paymentID,
                payerID:   data.payerID
            }).then(function(res) {
                console.log(res.success)
                // The payment is complete!
                // You can now show a confirmation message to the customer
            });
        }
    }, string);
};

$.getJSON(products_url, function(data) {
//    console.log(data);
    for (var i=0; i < data.data.length; i++) {
        images = data.data[i]['images'].split(",")
        images.forEach(function(element){
            element = element.trim()
        });
        
        product_dict[data.data[i]['id']] = {ID: data.data[i]['id'],
                                              Name: data.data[i]['name'],
                                              Description: data.data[i]['desc'],
                                              Images: images,
                                              link:data.data[i]['link'],
                                              price:data.data[i]['price']}
    };
}).then(function() {
    Object.keys(product_dict).forEach(function(key){
//        console.log(key, product_dict[key]);
        var html = `<div class="p-grid" id="${product_dict[key]['ID']}" onclick=getProduct(this)>
                        <div class="p-grid-in">
                            <img class="p-img" src="${product_dict[key]['Images'][0]}"/>
                            <div class="p-name">${product_dict[key]['Name']}</div>
                            <div class="p-price"><span class="currency-symbol">€</span><span class="price-text"> ${product_dict[key]['price']}</span></div>
                            <div class="p-desc">${product_dict[key]['Description']}</div>
                            <div class="button-container">
                                <div class="p-add" id="b${product_dict[key]['ID']}"></div>
                            </div>
                        </div>
                    </div>`;
        $( "#p-grid" ).append(html);
        
        getPaypalButton(key, product_dict[key], false, 'small');
    })
});




//sb-wbayu584258@personal.example.com
//$U/s$8BU
