$(function () {
  const dtConfig = (tableId, entityLabel) => ({
    responsive: true,
    pageLength: 10,
    order: [[1, "desc"]],
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
      emptyTable: `No ${entityLabel} found.`,
      zeroRecords: `No matching ${entityLabel}.`,
      search: "",
      searchPlaceholder: `Search ${entityLabel}...`,
      lengthMenu: "Rows per page _MENU_",
      info: `Showing _START_ to _END_ of _TOTAL_ ${entityLabel}`,
      infoEmpty: `Showing 0 to 0 of 0 ${entityLabel}`,
      infoFiltered: `(filtered from _MAX_ total ${entityLabel})`,
    },
  });

  $("#summary-prod-table").DataTable(dtConfig("summary-prod-table", "logs"));
  $("#summary-sales-table").DataTable(
    dtConfig("summary-sales-table", "transactions"),
  );
  $("#summary-waste-table").DataTable(
    dtConfig("summary-waste-table", "reports"),
  );
});
