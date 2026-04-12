$(function () {
  function showToast(type, msg) {
    const icons = { success: "check-circle-fill", error: "x-circle-fill" };
    const $t = $(`
      <div class="toast-item ${type}" data-autohide="true">
        <span class="toast-icon"><i class="bi bi-${icons[type]}"></i></span>
        <div class="toast-body">${msg}</div>
        <button class="toast-close" onclick="$(this).parent().remove()"><i class="bi bi-x"></i></button>
      </div>`);
    if (!$("#toast-container").length)
      $("body").append('<div id="toast-container"></div>');
    $("#toast-container").append($t);
    setTimeout(() => $t.fadeTo(400, 0, () => $t.remove()), 4500);
  }

  /* ── Edit profile ── */
  $("#form-edit-profile").on("submit", function (e) {
    e.preventDefault();
    const $btn = $("#btn-save-profile");
    hideFormError("#edit-profile-error");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Saving...');

    $.ajax({
      url: $("#form-edit-profile").data("url"),
      method: "POST",
      data: $(this).serialize(),
      success: function (res) {
        if (res.success) {
          bootstrap.Offcanvas.getInstance("#offcanvas-edit-profile").hide();
          showToast("success", res.message);
          if ($("#edit-full-name").not(":disabled").length) {
            $("#display-full-name").text($("#edit-full-name").val());
          }
          $("#display-username").text($("#edit-username").val());
          $("#display-phone").text($("#edit-phone").val() || "—");
        } else {
          const sms = Object.values(res.errors).flat().join(" ");
          showFormError("#edit-profile-error", sms);
        }
      },
      error: function () {
        showFormError(
          "#edit-profile-error",
          "Something went wrong. Try again.",
        );
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-check-lg me-1"></i> Save Changes');
      },
    });
  });

  /* ── Change password ── */
  $("#form-change-password").on("submit", function (e) {
    e.preventDefault();
    const $btn = $("#btn-change-pw");
    hideFormError("#change-pw-error");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Updating...');

    $.ajax({
      url: $("#form-change-password").data("url"),
      method: "POST",
      data: $(this).serialize(),
      success: function (res) {
        if (res.success) {
          bootstrap.Offcanvas.getInstance("#offcanvas-change-password").hide();
          showToast("success", res.message);
          $("#form-change-password")[0].reset();
        } else {
          const sms = Object.values(res.errors).flat().join(" ");
          showFormError("#change-pw-error", sms);
        }
      },
      error: function () {
        showFormError("#change-pw-error", "Something went wrong. Try again.");
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-check-lg me-1"></i> Update Password');
      },
    });
  });
});
