$(function () {
  // Set today's date as default
  const today = new Date().toISOString().split("T")[0];
  $("#waste-date").val(today);

  // Tom Select for item
  const itemSelects = makeSearchable("#waste-item-select", {
    placeholder: "Search snack items...",
  });
  const itemSelect = itemSelects["waste-item-select"];

  // Submit
  $("#form-report-waste").on("submit", function (e) {
    e.preventDefault();
    const url = $(this).data("url");
    const $btn = $("#btn-submit-waste");
    hideFormError("#report-error");

    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Submitting...');

    $.ajax({
      url: url,
      method: "POST",
      data: $(this).serialize(),
      success: function (res) {
        if (res.success) {
          showToast("success", res.message);
          // Reset form
          $("#form-report-waste")[0].reset();
          itemSelect.clear();
          $("#waste-date").val(today);
        } else {
          showFormError(
            "#report-error",
            Object.values(res.errors).flat().join(" "),
          );
        }
      },
      error: function () {
        showFormError("#report-error", "Something went wrong. Try again.");
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-send me-1"></i> Submit Waste Report');
      },
    });
  });
});
