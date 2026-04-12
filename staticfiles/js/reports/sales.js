$(function () {
  $("#sales-report-table").DataTable({
    responsive: true,
    pageLength: 10,
    order: [[1, "desc"]],
    columnDefs: [
      {
        targets: 4, // Total amount column
        render: function (data, type) {
          if (type === "display") {
            const num = parseFloat(String(data).replace(/,/g, ""));
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
      emptyTable: "No sales transactions found.",
      zeroRecords: "No matching transactions.",
      search: "",
      searchPlaceholder: "Search transactions...",
      lengthMenu: "Rows per page _MENU_",
      info: "Showing _START_ to _END_ of _TOTAL_ transactions",
      infoEmpty: "Showing 0 to 0 of 0 transactions",
      infoFiltered: "(filtered from _MAX_ total transactions)",
    },
  });
});
