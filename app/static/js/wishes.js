function removeWish(id) {
    $.ajax({
        url: `/api/v1/wish/${id}`,
        method: "DELETE",
        success: function(){
            window.location.reload();
        },
    });
}

$(document).ready(function(){
    $('#inp').change(function(e){
        var image = new FormData();
        image.append("file", e.target.files[0]);
        $.ajax({
          url: "/download_file",
          method: "POST",
          processData: false,
          contentType: false,
          data: image,
          success: function(){
            window.location.reload();
          },
        });
    });
});

$(document).on("click",".editWishButton", function () {
    let wish_id = $(this).data("id");
    $.ajax({
        url: `/api/v1/wish/${wish_id}`,
        method: "GET",
        success: function(data){
          let res = $(data)[0];
          let form = $("#editForm");
          form.find('input[name="edit-title"]').val(res["title"]);
          form.find('input[name="edit-description"]').val(res["description"]);
          form.find('input[name="edit-link"]').val(res["link"]);
          form.find('input[name="edit-id"]').val(wish_id);
          $("#editModal").modal("show")
        },
      });
 });