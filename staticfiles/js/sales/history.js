$(function () {
  const table = $("#sales-table").DataTable({
    responsive: true,
    pageLength: 10,
    order: [[2, "desc"]],
    columnDefs: [
      { orderable: false, targets: -1 },
      {
        targets: 4, // Total amount column
        render: function (data, type, row) {
          if (type === "display") {
            const num = parseFloat(data.replace(/,/g, ""));
            if (isNaN(num)) return data;
            return num.toLocaleString("en-US");
          }
          return data;
        },
      },
    ],
    dom:
      '<"d-flex align-items-center justify-content-between flex-wrap gap-2 mb-3"Bf>' +
      '<"table-responsive"t>' +
      '<"d-flex align-items-center justify-content-between flex-wrap gap-2 mt-3"lip>',
    buttons: [
      {
        extend: "copy",
        className: "btn btn-sm btn-outline-button1 me-1",
        text: '<i class="bi bi-clipboard"></i> Copy',
      },
      {
        extend: "excel",
        className: "btn btn-sm btn-outline-button2 me-1",
        text: '<i class="bi bi-file-earmark-excel"></i> Excel',
      },
      {
        extend: "pdf",
        className: "btn btn-sm btn-outline-button3 me-1",
        text: '<i class="bi bi-file-earmark-pdf"></i> PDF',
      },
      {
        extend: "print",
        className: "btn btn-sm btn-outline-bakery",
        text: '<i class="bi bi-printer"></i> Print',
      },
    ],
    language: {
      emptyTable: "No transactions found.",
      zeroRecords: "No matching transactions.",
      search: "",
      searchPlaceholder: "Search transactions...",
      lengthMenu: "Rows per page _MENU_",
      info: "Showing _START_ to _END_ of _TOTAL_ transactions",
      infoEmpty: "Showing 0 to 0 of 0 transactions",
      infoFiltered: "(filtered from _MAX_ total transactions)",
    },
  });

  /* ── Cancel transaction (admin only) ── */
  $(document).on("click", ".btn-action.cancel", function () {
    const $row = $(this).closest("tr");
    $("#cancel-txn-url").val($(this).data("url"));
    $("#cancel-txn-ref").text($(this).data("ref"));
    $("#modal-cancel-txn").data("row", $row);
    new bootstrap.Modal("#modal-cancel-txn").show();
  });

  $("#btn-confirm-cancel").on("click", function () {
    const $btn = $(this);
    const url = $("#cancel-txn-url").val();
    const $row = $("#modal-cancel-txn").data("row");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Cancelling...');

    $.ajax({
      url: url,
      method: "POST",
      data: { csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val() },
      success: function (res) {
        if (res.success) {
          bootstrap.Modal.getInstance("#modal-cancel-txn").hide();
          showToast("success", res.message);
          // Update status badge in the row rather than full reload
          $row
            .find(".status-badge")
            .removeClass("completed")
            .addClass("cancelled")
            .text("Cancelled");
          $row.find(".btn-action.cancel").remove();
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
          .html('<i class="bi bi-x-circle me-1"></i> Cancel Transaction');
      },
    });
  });
});
