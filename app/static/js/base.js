$('#formButton').click(function() {
    var values = $(myForm).serialize();
    $.ajax({
      url: "/login",
      method: "POST",
      data: values,
      success: function(){
        window.location.reload();
      },
      error: function(){
        $("#loginMessage").html('Incorrect username or password');
        $("#loginMessage").removeClass("d-none");
      },
    }).done(function() {
      $('#loginModal').modal('hide');
    });
});

$('#addForm').submit(function(event) {
  event.preventDefault();
  let myform = document.getElementById("addForm");
  let fd = new FormData(myform);
  fd.append('add-image', $('#add-image')[0].files[0]);
  $.ajax({
    url: '/add_wish',
    type: 'POST',
    cache: false,
    processData: false,
    contentType: false,
    dataType: 'json',
    data: fd,
    success: function() {
      window.location.reload();
    }
  }).done(function() {
    $('#addModal').modal('hide');
  });
});

$('#logoutButton').click(function() {
    $.ajax({
        url: "/logout",
        method: "GET",
        success: function(){
          window.location.href('/');
        },
      });
})