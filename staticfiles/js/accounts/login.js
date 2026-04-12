$(function () {
  $("#login-form").on("submit", function (e) {
    e.preventDefault();

    const $btn = $("#login-btn");
    const $error = $("#login-error");
    const $errorMsg = $("#login-error-msg");

    // Reset error
    $error.hide();
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Signing in...');

    $.ajax({
      url: $(this).data("url"),
      method: "POST",
      data: {
        username: $("#username").val().trim(),
        password: $("#password").val(),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        next: $("input[name=next]").val(),
      },
      success: function (res) {
        if (res.success) {
          window.location.href = res.redirect;
        } else {
          $errorMsg.text(res.error);
          $error.show();
          $btn
            .prop("disabled", false)
            .html('<i class="bi bi-box-arrow-in-right me-1"></i> Sign In');
        }
      },
      error: function () {
        $errorMsg.text("Something went wrong. Please try again.");
        $error.show();
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-box-arrow-in-right me-1"></i> Sign In');
      },
    });
  });
});
