try{
    document.getElementsByClassName('cancel-link')[0].className = 'btn btn-dark cancel-link form-control';
}catch(e){}

if (window.location.href.includes('/change/')){
    document.getElementsByClassName('col-sm-7 field-image')[0].querySelectorAll('input[type="checkbox"]')[0].style.display = 'none';
    document.getElementsByClassName('col-sm-7 field-image')[0].getElementsByTagName('label')[0].style.display = 'none';
}

function getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }

function removeImageAdmin(restaurant, category) {
        var r = confirm("Remove image for this item?");
        if (r == true) {
            var item_id = window.location.pathname.split("/")[4];
            var csrftoken = getCookie('csrftoken');
            $.ajax({
                url: "/"+restaurant+"_menu/set_default_image/"+category,
                type: "POST",
                data: { id: item_id, csrfmiddlewaretoken: csrftoken },

                success: function(json) {
                    location.reload();
                },
                error: function(xhr, errmsg, err) {
                    console.log("Unable to remove image due to error: " + xhr.responseText);
                }
            });
        }

    }