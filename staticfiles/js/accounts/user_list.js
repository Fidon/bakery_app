$(function () {
  /* ── DataTable ── */
  const table = $("#users-table").DataTable({
    responsive: true,
    pageLength: 10,
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
      emptyTable: "No users found.",
      zeroRecords: "No matching users.",
      search: "",
      searchPlaceholder: "Search...",
      lengthMenu: "_MENU_ users per page",
      info: "Showing _START_ to _END_ of _TOTAL_ users",
      infoEmpty: "Showing 0 to 0 of 0 users",
      infoFiltered: "(filtered from _MAX_ total users)",
    },
  });

  /* ── Add user ── */
  $("#form-add-user").on("submit", function (e) {
    e.preventDefault();
    const url = $(this).data("url");
    const $btn = $("#btn-save-user");
    hideFormError("#add-user-error");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Saving...');

    $.ajax({
      url: url,
      method: "POST",
      data: $(this).serialize(),
      success: function (res) {
        if (res.success) {
          bootstrap.Offcanvas.getInstance("#offcanvas-add-user").hide();
          $("#form-add-user")[0].reset();
          showToast("success", res.message);
          setTimeout(() => location.reload(), 1000);
        } else {
          const sms = Object.values(res.errors).flat().join(" ");
          showFormError("#add-user-error", sms);
        }
      },
      error: function () {
        showFormError("#add-user-error", "Something went wrong. Try again.");
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-check-lg me-1"></i> Save User');
      },
    });
  });

  /* ── Edit user — open offcanvas and populate ── */
  $(document).on("click", ".btn-action.edit", function () {
    const $btn = $(this);
    // Store URL on the form
    $("#form-edit-user").data("url", $btn.data("url"));
    $("#edit-full-name").val($btn.data("full-name"));
    $("#edit-username").val($btn.data("username"));
    $("#edit-phone").val($btn.data("phone"));
    $("#edit-role").val($btn.data("role"));
    $("#edit-user-error").hide();
    new bootstrap.Offcanvas("#offcanvas-edit-user").show();
  });

  $("#form-edit-user").on("submit", function (e) {
    e.preventDefault();
    const url = $(this).data("url");
    const $btn = $("#btn-update-user");
    $("#edit-user-error").hide();
    hideFormError("#edit-user-error");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Saving...');

    $.ajax({
      url: url,
      method: "POST",
      data: $(this).serialize(),
      success: function (res) {
        if (res.success) {
          bootstrap.Offcanvas.getInstance("#offcanvas-edit-user").hide();
          showToast("success", res.message);
          setTimeout(() => location.reload(), 1000);
        } else {
          const sms = Object.values(res.errors).flat().join(" ");
          showFormError("#edit-user-error", sms);
        }
      },
      error: function () {
        showFormError("#edit-user-error", "Something went wrong. Try again.");
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-check-lg me-1"></i> Update User');
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
      });
    },
  );

  /* ── Reset password ── */
  $(document).on("click", ".btn-action.reset-pw", function () {
    $("#reset-pw-url").val($(this).data("url"));
    $("#reset-pw-name").text($(this).data("name"));
    new bootstrap.Modal("#modal-reset-pw").show();
  });

  $("#btn-confirm-reset-pw").on("click", function () {
    const $btn = $(this);
    const url = $("#reset-pw-url").val();
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Resetting...');

    $.ajax({
      url: url,
      method: "POST",
      data: { csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val() },
      success: function (res) {
        if (res.success) {
          bootstrap.Modal.getInstance("#modal-reset-pw").hide();
          showToast("success", res.message);
        } else {
          bootstrap.Modal.getInstance("#modal-reset-pw").hide();
          showToast("error", res.error);
        }
      },
      error: function () {
        showToast("error", "Something went wrong. Try again.");
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-key me-1"></i> Reset');
      },
    });
  });

  /* ── Delete modal ── */
  $(document).on("click", ".btn-action.delete", function () {
    const $row = $(this).closest("tr");
    $("#delete-user-url").val($(this).data("url"));
    $("#delete-user-name").text($(this).data("name"));
    // Store reference to the row on the modal
    $("#modal-delete-user").data("row", $row);
    new bootstrap.Modal("#modal-delete-user").show();
  });

  $("#btn-confirm-delete").on("click", function () {
    const $btn = $(this);
    const url = $("#delete-user-url").val();
    const $row = $("#modal-delete-user").data("row");
    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Deleting...');

    $.ajax({
      url: url,
      method: "POST",
      data: { csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val() },
      success: function (res) {
        if (res.success) {
          bootstrap.Modal.getInstance("#modal-delete-user").hide();
          showToast("success", res.message);
          // Remove row from DataTable properly
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
});
