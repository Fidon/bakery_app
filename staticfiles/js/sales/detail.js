$(function () {
  /* ── Cancel transaction from detail page (admin only) ── */
  $("#btn-cancel-txn").on("click", function () {
    new bootstrap.Modal("#modal-cancel-txn").show();
  });

  $("#btn-confirm-cancel").on("click", function () {
    const $btn = $(this);
    const url = $("#btn-cancel-txn").data("url");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Cancelling...');

    $.ajax({
      url: url,
      method: "POST",
      data: { csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val() },
      success: function (res) {
        if (res.success) {
          showToast("success", res.message);
          // Redirect to history after a moment
          setTimeout(() => {
            window.location.href = "/sales/";
          }, 1200);
        } else {
          bootstrap.Modal.getInstance("#modal-cancel-txn").hide();
          showToast("error", res.error);
          $btn
            .prop("disabled", false)
            .html('<i class="bi bi-x-circle me-1"></i> Cancel Transaction');
        }
      },
      error: function () {
        showToast("error", "Something went wrong. Try again.");
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-x-circle me-1"></i> Cancel Transaction');
      },
    });
  });
});
