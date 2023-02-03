function menuSearch() {
    var input, filter, menu, cards, a, i, y, txtValue;
    var categories = new Set();
    input = document.getElementById('searchBar');
    filter = input.value.toUpperCase();
    menu = document.getElementById("menu-card");
    cats = document.getElementsByClassName("section");
    cards = menu.getElementsByClassName('card');

    for (i = 0; i < cards.length; i++) {
        h = cards[i].getElementsByTagName("h5")[0];
        txtValue = h.textContent || h.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          categories.add(cards[i].parentElement.id);
          cards[i].style.display = "";
        } else {
          cards[i].style.display = "none";
        }
    }
    console.log(categories);
    for (y = 0; y < cats.length; y++) {
        if (categories.has(cats[y].id)) {
            cats[y].style.display = '';
        } else {
            cats[y].style.display = "none";
        }
    }
}

function imageModal(name) {
    // Get the modal
    var modal = document.getElementById('dish-img-modal');

    // Get the image and insert it inside the modal - use its "alt" text as a caption
    var img = document.getElementById('dish-img-' + name);
    var modalImg = document.getElementById("modalImg");
    var captionText = document.getElementById("caption");
    try {
        img.onclick = function(){
            document.body.style.overflow = "hidden";
            modal.style.display = "block";
            modalImg.src = this.src;
            modalImg.alt = this.alt;
            captionText.innerHTML = this.alt;
        }
        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];

        // When the user clicks on <span> (x), close the modal
            span.onclick = function() {
                modal.style.display = "none";
                document.body.style.overflow = "auto";
            }
            modalImg.onclick = function() {
                modal.style.display = "none";
                document.body.style.overflow = "auto";
            }
            captionText.onclick = function() {
                modal.style.display = "none";
                document.body.style.overflow = "auto";
            }
            modal.onclick = function() {
                modal.style.display = "none";
                document.body.style.overflow = "auto";
            }

    }
    catch(err) {
        console.log(err)
}

}
