$(function () {
  /* ── DataTable ── */
  const table = $("#history-table").DataTable({
    responsive: true,
    pageLength: 10,
    order: [[1, "desc"]],
    columnDefs: [{ orderable: false, targets: -1 }],
    dom:
      '<"d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3"Bf>' +
      '<"table-responsive"t>' +
      '<"d-flex align-items-center justify-content-between flex-wrap gap-2 mt-3"lip>',
    buttons: [
      {
        extend: "copy",
        className: "btn btn-sm btn-outline-button1",
        text: '<i class="bi bi-clipboard"></i> Copy',
      },
      {
        extend: "excel",
        className: "btn btn-sm btn-outline-button2 mx-1",
        text: '<i class="bi bi-file-earmark-excel"></i> Excel',
      },
      {
        extend: "pdf",
        className: "btn btn-sm btn-outline-button3 mx-1",
        text: '<i class="bi bi-file-earmark-pdf"></i> PDF',
      },
      {
        extend: "print",
        className: "btn btn-sm btn-outline-bakery",
        text: '<i class="bi bi-printer"></i> Print',
      },
    ],
    language: {
      emptyTable: "No production logs found.",
      zeroRecords: "No matching logs.",
      search: "",
      searchPlaceholder: "Search logs...",
      lengthMenu: "Rows per page _MENU_",
      info: "Showing _START_ to _END_ of _TOTAL_ logs",
      infoEmpty: "Showing 0 to 0 of 0 logs",
      infoFiltered: "(filtered from _MAX_ total logs)",
    },
  });

  /* ── Delete log entry (admin only) ── */
  $(document).on("click", ".btn-action.delete", function () {
    const $row = $(this).closest("tr");
    $("#delete-log-url").val($(this).data("url"));
    $("#delete-log-item").text($(this).data("item"));
    $("#delete-log-qty").text($(this).data("qty"));
    $("#delete-log-date").text($(this).data("date"));
    $("#modal-delete-log").data("row", $row);
    new bootstrap.Modal("#modal-delete-log").show();
  });

  $("#btn-confirm-delete-log").on("click", function () {
    const $btn = $(this);
    const url = $("#delete-log-url").val();
    const $row = $("#modal-delete-log").data("row");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Deleting...');

    $.ajax({
      url: url,
      method: "POST",
      data: { csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val() },
      success: function (res) {
        if (res.success) {
          bootstrap.Modal.getInstance("#modal-delete-log").hide();
          showToast("success", res.message);
          table.row($row).remove().draw();
        } else {
          showToast("error", res.error);
        }
      },
      error: function () {
        showToast("error", "Something went wrong. Try again.");
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-trash me-1"></i> Delete');
      },
    });
  });

  /* ── Tooltips ── */
  document
    .querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach(function (el) {
      new bootstrap.Tooltip(el);
    });
});
