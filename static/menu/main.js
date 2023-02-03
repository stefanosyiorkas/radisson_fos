let ORDERING = false;

$(document).ready(function() {
    //check if local storage value of "cart retrived " is True
    if (ORDERING) {
        retrieve_saved_cart()
    }
    var cart = !!localStorage.getItem("cart") ? JSON.parse(localStorage.getItem("cart")) : null;
    if (cart !== null)
        if (cart.length == 0){
            document.getElementById('cart-count').innerText = ''
        }else{
            try {
                document.getElementById('cart-count').innerText = parseFloat(cart.length).toLocaleString('en-US')
            } catch (e) {
                console.log(e)
            }
        }

    if (window.location.href.indexOf("cart") > -1) {
        //dynamically generate the cart on the page
        if (document.getElementById('table_number').innerHTML == ''){
            document.getElementById("checkout_button").disabled = true;
        }
        load_cart()
    }

    if (window.location.href.indexOf("view-orders") > -1) {
        order_list_functionality()
    }
    $('#order-tbl').find('th, td').addClass('px-2 py-1 align-middle')
    $('#order-tbl').find('th:nth-child(1), td:nth-child(1)').addClass('text-center')
    $('#order-tbl').find('th:nth-last-child(1), td:nth-last-child(1)').addClass('text-right')
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });

    document.querySelector('.nav-subcategories').addEventListener('click', function(e){

        if (e.target.classList.contains('subcategory-link')){
            const yOffSet = 350;
            var current = document.querySelector('.active')
            if (current)
                current.classList.remove('active')
            e.target.classList.add('active')
            const id = e.target.getAttribute('href');
            document.querySelector(id)?.scrollIntoView()
        }
    })
});

const sections = document.querySelectorAll("section");
//const links = document.querySelectorAll("nav .subcategory-link");
//try{
//    links[0].classList.add("active")
//} catch(e){
//    console.log(e)
//}
//
//window.addEventListener("scroll", () => {
//    var current = "";
//
//    sections.forEach((section) => {
//        const sectionTop = section.offsetTop;
//        if (scrollY >= sectionTop - 900 ) {
//            current = section.getAttribute("id");
//        }
//    });
//
//    links.forEach((li) => {
//        li.classList.remove("active");
//        if (li.title === current) {
//            li.classList.add("active");
//            li.scrollIntoView()
//        }
//    });
//});

function order_list_functionality() {
//    document.getElementById('pending-orders').innerText = document.getElementsByClassName("table-danger").length
    onRowClick("orders_table", function(row) {
        var id = row.getElementsByTagName("td")[0].innerHTML;
        var csrftoken = getCookie('csrftoken');
        //send get request to see if user has superuser permissions
        var user_is_super = check_user_super();
        var user_is_staff = check_user_staff();
        if (user_is_super || user_is_staff) {
            if (row.classList.length == 1 && row.classList.contains("table-danger")){
                row.classList.add("pending");
            } else if (row.classList.length == 1 && row.classList.contains("table-success")){
                row.classList.add("completed");
            }
            if (row.classList.contains("pending")){
                var r = confirm("Would you like to mark order " + id + " as delivered?");
                if (r == true) {
                    $.ajax({
                        url: "/mark_order_as_delivered", // the endpoint
                        type: "POST", // http method
                        data: { id: id, csrfmiddlewaretoken: csrftoken }, // data sent with the post request

                        // handle a successful response
                        success: function(json) {
                            //make the row green
                            row.classList.remove("table-danger");
                            row.classList.add("table-success");
                            row.classList.add("completed");
                            row.classList.remove("pending")
                            row.classList.remove("mark-as-complete")
                            order_list_functionality()
                        },

                        // handle a non-successful response
                        error: function(xhr, errmsg, err) {
                            //have this as another toast
                            //have this as another toast
                            console.log("the server said no lol")
                        }
                    }); //make ajax post request
                }
            }else if (row.classList.contains("completed")){
                var r = confirm("Would you like to mark order " + id + " as pending?");
                if (r == true) {
                    $.ajax({
                        url: "/mark_order_as_pending", // the endpoint
                        type: "POST", // http method
                        data: { id: id, csrfmiddlewaretoken: csrftoken }, // data sent with the post request

                        // handle a successful response
                        success: function(json) {
                            //make the row red
                            row.classList.remove("table-success");
                            row.classList.add("table-danger");
                            row.classList.add("pending");
                            row.classList.remove("completed")
                            order_list_functionality()
                        },

                        // handle a non-successful response
                        error: function(xhr, errmsg, err) {
                            //have this as another toast
                            console.log("the server said no lol")
                        }
                    }); //make ajax post request
                }
            }

        }

    });
}

function check_user_super() {
    var return_value;
    $.ajax({
        url: "/check_superuser",
        type: 'GET',
        success: function(res) {
            console.log("we got back from the server the value ---> " + res)
            if (res == "True") {
                console.log("assigned true")
                return_value = true;
            } else {
                return_value = false;
            }
        },
        async: false
    });
    return return_value
}

function check_user_staff() {
    var return_value;
    $.ajax({
        url: "/check_staff_user",
        type: 'GET',
        success: function(res) {
            console.log("we got back from the server the value ---> " + res)
            if (res == "True") {
                console.log("assigned true")
                return_value = true;
            } else {
                return_value = false;
            }
        },
        async: false
    });
    return return_value
}

function add_to_cart(info) {
    //info will be the stuff displayed in the reciept
    // item description as well as teh price
    if (info == null) {
        display_notif("please login");
    }
    else{
        info['comments'] = document.getElementById(info['item_description']+'-additional-comments').value
        document.getElementById(info['item_description']+'-additional-comments').value=''
        display_notif("add to cart", info);
        var cart_retrieved = !!localStorage.getItem("cart") ? localStorage.getItem("cart") : null
        if (cart_retrieved === null) {
            //make a new cart
            var cart = [info];
            localStorage.setItem('cart', JSON.stringify(cart));
            document.getElementById('cart-count').innerText = parseFloat(cart.length).toLocaleString('en-US')

        } else {
            var cart = JSON.parse(cart_retrieved);
            cart.push(info)
            localStorage.setItem('cart', JSON.stringify(cart));
            if (cart.length != 0){
                document.getElementById('cart-count').innerText = parseFloat(cart.length).toLocaleString('en-US')
            }
        }
    }

}

// Get the button:
let mybutton = document.getElementById("goToTop");

// When the user scrolls down 500px from the top of the document, show the button
window.onscroll = function() {myscrollFunction()};

function myscrollFunction() {
  try {
      if (document.body.scrollTop > 500 || document.documentElement.scrollTop > 500) {
        mybutton.style.opacity = 1;
      } else {
        mybutton.style.opacity = 0;
      }
  } catch (e) {
    console.log(e)
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

function scrollToElement(id){
console.log("scrollToElement")
console.log(id)
 var element = document.getElementById(id);
 element.scrollIntoView();
}

function onRowClick(tableId, callback) {
    var table = document.getElementById(tableId),
        rows = table.getElementsByTagName("tr"),
        i;

    for (i = 0; i < rows.length; i++) {
        table.rows[i].onclick = function(row) { return function() { callback(row); }; }(table.rows[i]);
    }
}

function display_notif(type, info = "No info provided", timeout="3000") {
    //the different types of toasts are success, warning ... info and error
    toastr.options = {
        "closeButton": true,
        "debug": false,
        "newestOnTop": false,
        "progressBar": true,
        "positionClass": "toast-bottom-right",
        "preventDuplicates": false,
        "onclick": null,
        "showDuration": "70",
        "hideDuration": "1000",
        "timeOut": timeout,
        "extendedTimeOut": "500",
        "showEasing": "swing",
        "hideEasing": "linear",
        "showMethod": "fadeIn",
        "hideMethod": "fadeOut"
    }
    switch (type) {
        case "add to cart":
            toastr.success(info.item_description + ': € ' + info.price, 'Added to Cart');
            break;
        case "remove from cart":
            toastr.info("Successfully removed " + info + " from cart");
            break;
        case "new order":
            toastr.success("New Order Received");
            break;
        case "table none":
            toastr.error("Please select a table");
            break;
        case "please login":
            toastr.error("Please login first");
            break;
        case "clear cart":
            toastr.success("Successfully cleared the cart");
            break;
    }

}

function load_cart() {
    document.getElementById("card-tbl").style.display = "";
    var table = document.getElementById('cart_body');
    table.innerHTML = ""; //clear the table
    try {
        var cart = JSON.parse(localStorage.getItem("cart"));
    }
    catch(err) {
        console.log(err)
      var cart = null
    }

    var total = 0;
    if (cart !== null && cart.length > 0) {
        document.getElementById("empty-cart").style.display = "none";
        document.getElementById("cart-content").style.display = "";
        for (var i = 0; i < cart.length; i++) {

            var row = table.insertRow(-1);
            var item_number = row.insertCell(0);
            var item_description = row.insertCell(1);
            var item_price = row.insertCell(2);
            var item_remove = row.insertCell(3);
            item_number.innerHTML = String(i + 1);
            if (cart[i].comments.length > 0)
                item_description.innerHTML = '<b>' + cart[i].item_description + '</b>' + '<pre>' + cart[i].comments + '</pre>';
            else
                item_description.innerHTML = '<b>' + cart[i].item_description + '</b>'
            item_price.innerHTML = "€" + parseFloat(cart[i].price).toLocaleString('en-US', { style: 'decimal', maximumFractionDigits: 2, minimumFractionDigits: 2 });
            item_remove.innerHTML = '<button class="btn btn-light btn-sm" onclick="remove_from_cart(' + i + ')">X</button>';
            total += parseFloat(cart[i].price)
        }
        total = Math.round(total * 100) / 100
        localStorage.setItem('total_price', total);
        document.getElementById('total').innerHTML = "€ " + parseFloat(localStorage.getItem("total_price")).toLocaleString('en-US', { style: 'decimal', maximumFractionDigits: 2, minimumFractionDigits: 2 })


        onRowClick("cart_body", function(row) {
            var value = row.getElementsByTagName("td")[0].innerHTML;
            var description = row.getElementsByTagName("td")[1].innerHTML.split("<pre>")[0].replace(/(<([^>]+)>)/ig, "");
            var r = confirm("Proceed to delete '" + description + "' from cart?");
            if (r == true) {
                document.getElementById("cart_body").deleteRow(value - 1);
                try {
                    document.getElementById('cart-count').innerText = parseFloat(cart.length - 1).toLocaleString('en-US')
                } catch (err) {
                    console.log(err)
                }
                //edit the cart
                cart.splice(value - 1, 1) //this is how you remove elements from a list in javascript
                localStorage.setItem('cart', JSON.stringify(cart)); //change the elements in the cart in local storage
                display_notif("remove from cart", description)
                load_cart() //refresh the page
            }
        });
    } else {
        display_empty_cart()
    }
    $('#card-tbl').find('th').addClass('px-2 py-1 align-middle')
    $('#card-tbl').find('td').addClass('px-2 py-3 align-middle')
    $('#card-tbl').find('td:nth-child(3)').addClass('text-center')
    $('#card-tbl').find('th:nth-child(1), td:nth-child(1)').addClass('text-center')
    $('#card-tbl').find('th:nth-last-child(1), td:nth-last-child(1)').addClass('text-center')

}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} //this function is to get the CSRF token

function display_empty_cart() {
    document.getElementById("empty-cart").style.display = "";
    document.getElementById("cart-content").style.display = "none";
    var table = document.getElementById('cart_body');
    table.innerHTML = ""; //clear the table
    document.getElementById('total').innerHTML = "€ 0"
    document.getElementById("checkout_button").disabled = true;
    document.getElementById('cart-count').innerText = '';
}

function clear_cart_btn(){
    if (confirm("Proceed to clear the cart?")) {
        clear_cart()
    }
}

function clear_cart() {
    localStorage.removeItem("cart"); //Clear the cart
    localStorage.removeItem("total_price"); //clear the price
    localStorage.removeItem("table_number"); //Clear the table number
    //remove the elements from the page
    display_empty_cart();
    display_notif("clear cart");
}

function clear_cart_silent() {
    localStorage.removeItem("cart"); //Clear the cart
    localStorage.removeItem("total_price"); //clear the price
    localStorage.removeItem("table_number"); //Clear the table number
}

function checkout() {
    //this is the function that will be run when the user wants to checkout
    CheckoutButtonClicked();
    var cart = localStorage.getItem("cart")
    var price_of_cart = localStorage.getItem("total_price")
    var table_number = document.getElementById('table_number').innerHTML
    var csrftoken = getCookie('csrftoken');

    console.log("Table " + table_number)
    if (table_number=="none" || table_number==null || table_number==''){
        display_notif("table none")
    } else {
        console.log("Checkout was clicked so we now send it to the server!") // sanity check
        $.ajax({
        url: "/checkout", // the endpoint
        type: "POST", // http method
        data: { cart: cart, price_of_cart: price_of_cart, table_number: table_number, csrfmiddlewaretoken: csrftoken }, // data sent with the post request

        // handle a successful response
        success: function(json) {
//            display_notif("new order")
            clear_cart_silent()
            window.location.replace('/order_success');
        },

        // handle a non-successful response
        error: function(xhr, errmsg, err) {
            //have this as another toast
            console.log("the server said no lol")

        }
    });
    }

}

function logout() {
    if (ORDERING) {
        var current_cart = localStorage.getItem("cart")
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: "save_cart", // the endpoint
            type: "POST", // http method
            data: { cart: current_cart, csrfmiddlewaretoken: csrftoken }, // data sent with the post request

            // handle a successful response
            success: function(json) {
                //clear the local storage
                localStorage.removeItem("cart"); //Clear the cart
                localStorage.setItem('cart_retrieved', false);
                window.location.href = "logout";
            },

            // handle a non-successful response
            error: function(xhr, errmsg, err) {
                //have this as another toast
                console.log("the server said no lol")

            }
        });
    } else {
        window.location.href = "/logout";
    }
}

function retrieve_saved_cart() {
    if (localStorage.getItem("cart_retrieved") !== "true") {
        $.ajax({
            url: "retrieve_saved_cart",
            type: 'GET',
            success: function(res) {
                localStorage.setItem('cart_retrieved', true);
                localStorage.setItem("cart", res)
            }
        });
        //
    }
}