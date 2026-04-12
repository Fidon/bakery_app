$(function () {
  /* ── DataTable ── */
  const table = $("#items-table").DataTable({
    responsive: true,
    pageLength: 10,
    columnDefs: [
      { orderable: false, targets: -1 },
      {
        targets: 3,
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
      emptyTable: "No snack items found.",
      zeroRecords: "No matching items.",
      search: "",
      searchPlaceholder: "Search items...",
      lengthMenu: "Rows per page _MENU_",
      info: "Showing _START_ to _END_ of _TOTAL_ items",
      infoEmpty: "Showing 0 to 0 of 0 items",
      infoFiltered: "(filtered from _MAX_ total items)",
    },
  });

  /* ── Add item ── */
  $("#form-add-item").on("submit", function (e) {
    e.preventDefault();
    const url = $(this).data("url");
    const $btn = $("#btn-save-item");
    hideFormError("#add-item-error");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Saving...');

    $.ajax({
      url: url,
      method: "POST",
      data: $(this).serialize(),
      success: function (res) {
        if (res.success) {
          bootstrap.Offcanvas.getInstance("#offcanvas-add-item").hide();
          $("#form-add-item")[0].reset();
          showToast("success", res.message);
          setTimeout(() => location.reload(), 1000);
        } else {
          showFormError(
            "#add-item-error",
            Object.values(res.errors).flat().join(" "),
          );
        }
      },
      error: function () {
        showFormError("#add-item-error", "Something went wrong. Try again.");
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-check-lg me-1"></i> Save Item');
      },
    });
  });

  /* ── Edit item — populate offcanvas ── */
  $(document).on("click", ".btn-action.edit", function () {
    const $btn = $(this);
    $("#form-edit-item").data("url", $btn.data("url"));
    $("#edit-name").val($btn.data("name"));
    $("#edit-unit").val($btn.data("unit"));
    $("#edit-price").val($btn.data("price"));
    $("#edit-description").val($btn.data("description"));
    hideFormError("#edit-item-error");
    new bootstrap.Offcanvas("#offcanvas-edit-item").show();
  });

  $("#form-edit-item").on("submit", function (e) {
    e.preventDefault();
    const url = $(this).data("url");
    const $btn = $("#btn-update-item");
    hideFormError("#edit-item-error");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Saving...');

    $.ajax({
      url: url,
      method: "POST",
      data: $(this).serialize(),
      success: function (res) {
        if (res.success) {
          bootstrap.Offcanvas.getInstance("#offcanvas-edit-item").hide();
          showToast("success", res.message);
          setTimeout(() => location.reload(), 1000);
        } else {
          showFormError(
            "#edit-item-error",
            Object.values(res.errors).flat().join(" "),
          );
        }
      },
      error: function () {
        showFormError("#edit-item-error", "Something went wrong. Try again.");
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-check-lg me-1"></i> Update Item');
      },
    });
  });

  /* ── Toggle active/inactive ── */
  $(document).on(
    "click",
    ".btn-action.block, .btn-action.unblock",
    function () {
      const url = $(this).data("url");
      $.ajax({
        url: url,
        method: "POST",
        data: { csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val() },
        success: function (res) {
          if (res.success) {
            showToast("success", res.message);
            setTimeout(() => location.reload(), 900);
          } else {
            showToast("error", res.error);
          }
        },
        error: function () {
          showToast("error", "Something went wrong. Try again.");
        },
      });
    },
  );

  /* ── Delete ── */
  $(document).on("click", ".btn-action.delete", function () {
    const $row = $(this).closest("tr");
    $("#delete-item-url").val($(this).data("url"));
    $("#delete-item-name").text($(this).data("name"));
    $("#modal-delete-item").data("row", $row);
    new bootstrap.Modal("#modal-delete-item").show();
  });

  $("#btn-confirm-delete").on("click", function () {
    const $btn = $(this);
    const url = $("#delete-item-url").val();
    const $row = $("#modal-delete-item").data("row");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Deleting...');

    $.ajax({
      url: url,
      method: "POST",
      data: { csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val() },
      success: function (res) {
        if (res.success) {
          bootstrap.Modal.getInstance("#modal-delete-item").hide();
          showToast("success", res.message);
          table.row($row).remove().draw();
        } else {
          bootstrap.Modal.getInstance("#modal-delete-item").hide();
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
});
