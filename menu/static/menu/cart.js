function CheckoutButtonClicked() {
   document.getElementById("clear-cart-btn").disabled = true;
   document.getElementById("checkout_button").style.display = "none"; // to undisplay
   document.getElementById("loading-order").style.display = ""; // to display
   return true;
}
var FirstLoading = true;
function RestoreSubmitButton()
{
   if( FirstLoading )
   {
      FirstLoading = false;
      return;
   }
   document.getElementById("checkout_button").style.display = ""; // to display
   document.getElementById("loading-order").style.display = "none"; // to undisplay
}
// To disable restoring submit button, disable or delete next line.
document.onfocus = RestoreSubmitButton;