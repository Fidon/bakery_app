$(function () {
  const table = $("#pending-table").DataTable({
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
      emptyTable: "No pending waste reports.",
      zeroRecords: "No matching reports.",
      search: "",
      searchPlaceholder: "Search pending...",
      lengthMenu: "Rows per page _MENU_",
      info: "Showing _START_ to _END_ of _TOTAL_ reports",
      infoEmpty: "Showing 0 to 0 of 0 reports",
      infoFiltered: "(filtered from _MAX_ total reports)",
    },
  });

  // Tooltips
  document
    .querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach(function (el) {
      new bootstrap.Tooltip(el);
    });

  const csrf = $("[name=csrfmiddlewaretoken]").val();

  /* ── Approve ── */
  $(document).on("click", ".btn-action.approve", function () {
    const $btn = $(this);
    $("#approve-url").val($btn.data("url"));
    $("#approve-row-id").val("pending-row-" + $btn.data("pk"));
    $("#approve-item").text($btn.data("item"));
    $("#approve-qty").text($btn.data("qty"));
    $("#approve-stock").text($btn.data("stock"));
    $("#approve-notes").val("");
    hideFormError("#approve-error");
    new bootstrap.Modal("#modal-approve").show();
  });

  $("#btn-confirm-approve").on("click", function () {
    const $btn = $(this);
    const url = $("#approve-url").val();
    const rowId = "#" + $("#approve-row-id").val();
    const notes = $("#approve-notes").val().trim();
    hideFormError("#approve-error");

    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Approving...');

    $.ajax({
      url: url,
      method: "POST",
      data: {
        csrfmiddlewaretoken: csrf,
        action: "approve",
        admin_notes: notes,
      },
      success: function (res) {
        if (res.success) {
          bootstrap.Modal.getInstance("#modal-approve").hide();
          showToast("success", res.message);
          // Remove the row from the DataTable
          const $row = $(rowId);
          table.row($row).remove().draw();
        } else {
          showFormError("#approve-error", res.error);
        }
      },
      error: function () {
        showFormError("#approve-error", "Something went wrong. Try again.");
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-check-lg me-1"></i> Approve');
      },
    });
  });

  /* ── Reject ── */
  $(document).on("click", ".btn-action.reject", function () {
    const $btn = $(this);
    $("#reject-url").val($btn.data("url"));
    $("#reject-row-id").val("pending-row-" + $btn.data("pk"));
    $("#reject-item").text($btn.data("item"));
    $("#reject-qty").text($btn.data("qty"));
    $("#reject-notes").val("");
    hideFormError("#reject-error");
    new bootstrap.Modal("#modal-reject").show();
  });

  $("#btn-confirm-reject").on("click", function () {
    const $btn = $(this);
    const url = $("#reject-url").val();
    const rowId = "#" + $("#reject-row-id").val();
    const notes = $("#reject-notes").val().trim();

    if (!notes) {
      showFormError("#reject-error", "Please provide a reason for rejection.");
      return;
    }
    hideFormError("#reject-error");

    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Rejecting...');

    $.ajax({
      url: url,
      method: "POST",
      data: { csrfmiddlewaretoken: csrf, action: "reject", admin_notes: notes },
      success: function (res) {
        if (res.success) {
          bootstrap.Modal.getInstance("#modal-reject").hide();
          showToast("success", res.message);
          const $row = $(rowId);
          table.row($row).remove().draw();
        } else {
          showFormError("#reject-error", res.error);
        }
      },
      error: function () {
        showFormError("#reject-error", "Something went wrong. Try again.");
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-x-lg me-1"></i> Reject');
      },
    });
  });
});
