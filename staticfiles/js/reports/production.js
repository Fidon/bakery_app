$(function () {
  const table = $("#production-report-table").DataTable({
    responsive: true,
    pageLength: 10,
    order: [[1, "desc"]],
    columnDefs: [
      { orderable: false, targets: [] },
      {
        targets: 4, // Quantity column
        render: function (data, type) {
          if (type === "display") {
            const num = parseFloat(data.replace(/,/g, ""));
            return isNaN(num) ? data : num.toLocaleString("en-US");
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
      emptyTable: "No production logs found.",
      zeroRecords: "No matching logs.",
      search: "",
      searchPlaceholder: "Search logs...",
      lengthMenu: "Rows per page _MENU_",
      info: "Showing _START_ to _END_ of _TOTAL_ logs",
      infoEmpty: "Showing 0 to 0 of 0 logs",
      infoFiltered: "(filtered from _MAX_ total logs)",
    },
    footerCallback: function () {
      const api = this.api();
      // Sum only visible (filtered) rows
      const total = api
        .column(4, { search: "applied" })
        .data()
        .reduce(function (acc, val) {
          return acc + (parseFloat(String(val).replace(/,/g, "")) || 0);
        }, 0);
      $("#tfoot-qty").text(total.toLocaleString("en-US"));
      $("#total-qty-stat").text(total.toLocaleString("en-US"));
    },
  });

  // Tooltips
  document
    .querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach((el) => new bootstrap.Tooltip(el));
});
