$(function () {
  const searchableSelects = makeSearchable("#item-select", {
    placeholder: "Search snack items...",
  });
  const itemSelect = searchableSelects["item-select"];
  const batch = []; // { id, name, unit, quantity, notes }

  const $emptyState = $("#batch-empty");
  const $rowsList = $("#batch-rows");
  const $submitArea = $("#submit-area");
  const $batchCount = $("#batch-count");
  const $batchSummary = $("#batch-summary");

  /* ── Update unit label when item changes ── */
  $("#item-select").on("change", function () {
    const $opt = $(this).find(":selected");
    const unit = $opt.data("unit") || "units";
    $("#unit-display").text(unit);
    $("#item-quantity").focus();
  });

  /* ── Add row to batch ── */
  $("#btn-add-row").on("click", function () {
    const $select = $("#item-select");
    const $qty = $("#item-quantity");
    const $notes = $("#item-notes");
    const itemId = $select.val();
    const itemName = $select.find(":selected").data("name");
    const itemUnit = $select.find(":selected").data("unit");
    const quantity = parseInt($qty.val(), 10);
    const notes = $notes.val().trim();

    // Validate
    if (!itemId) {
      showToast("error", "Please select a snack item.");
      $select.focus();
      return;
    }
    if (!quantity || quantity < 1) {
      showToast("error", "Enter a valid quantity (minimum 1).");
      $qty.focus();
      return;
    }

    // Duplicate check
    if (batch.find((r) => r.id === itemId)) {
      showToast(
        "error",
        `"${itemName}" is already in this batch. Remove it first to change the quantity.`,
      );
      return;
    }

    // Add to batch array
    batch.push({ id: itemId, name: itemName, unit: itemUnit, quantity, notes });

    // Render the new row
    renderRow(batch.length - 1);
    updateBatchUI();

    // Reset inputs
    itemSelect.clear();
    $qty.val("");
    $notes.val("");
    $("#unit-display").text("units");
    $select.focus();
  });

  /* ── Allow Enter key on quantity to add row ── */
  $("#item-quantity").on("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      $("#btn-add-row").trigger("click");
    }
  });

  /* ── Render a single batch row card ── */
  function renderRow(index) {
    const r = batch[index];
    const $row = $(`
      <div class="batch-row" id="batch-row-${index}">
        <div class="batch-row-icon"><i class="bi bi-basket"></i></div>
        <div class="batch-row-info">
          <div class="batch-row-name">${escHtml(r.name)}</div>
          <div class="batch-row-meta">${escHtml(r.unit)}${r.notes ? " · " + escHtml(r.notes) : ""}</div>
        </div>
        <div class="batch-row-qty">${r.quantity.toLocaleString()}</div>
        <button class="btn-remove-row" data-index="${index}" title="Remove">
          <i class="bi bi-x"></i>
        </button>
      </div>
    `);
    $rowsList.append($row);
  }

  /* ── Remove a row ── */
  $(document).on("click", ".btn-remove-row", function () {
    const index = parseInt($(this).data("index"), 10);
    batch.splice(index, 1);
    rebuildRows();
    updateBatchUI();
  });

  /* ── Rebuild all rows (after removal) ── */
  function rebuildRows() {
    $rowsList.empty();
    batch.forEach((_, i) => renderRow(i));
  }

  /* ── Update count pill, empty state, submit area ── */
  function updateBatchUI() {
    const count = batch.length;
    $batchCount.text(count === 1 ? "1 item" : `${count} items`);

    if (count === 0) {
      $emptyState.show();
      $rowsList.hide();
      $submitArea.hide();
    } else {
      $emptyState.hide();
      $rowsList.show();
      $submitArea.show();
      const totalQty = batch.reduce((s, r) => s + r.quantity, 0);
      $batchSummary.html(
        `<span><strong>${count}</strong> item type${count !== 1 ? "s" : ""} &nbsp;·&nbsp; <strong>${totalQty.toLocaleString()}</strong> total units</span>` +
          `<button class="btn-clear-batch" id="btn-clear-batch">Clear all</button>`,
      );
    }
  }

  /* ── Clear batch ── */
  $(document).on("click", "#btn-clear-batch", function () {
    new bootstrap.Modal("#modal-clear-batch").show();
  });

  $("#btn-confirm-clear").on("click", function () {
    batch.length = 0;
    rebuildRows();
    updateBatchUI();
    bootstrap.Modal.getInstance("#modal-clear-batch").hide();
  });

  /* ── Submit batch ── */
  $("#btn-submit-batch").on("click", function () {
    const $btn = $(this);
    const productionDate = $("#production-date").val();
    hideFormError("#batch-submit-error");

    if (!productionDate) {
      showFormError("#batch-submit-error", "Please set a production date.");
      return;
    }
    if (batch.length === 0) {
      showFormError(
        "#batch-submit-error",
        "Add at least one item before submitting.",
      );
      return;
    }

    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Saving...');

    const payload = {
      production_date: productionDate,
      rows: batch.map((r) => ({
        snack_item: r.id,
        quantity: r.quantity,
        notes: r.notes,
      })),
    };

    $.ajax({
      url: window.PRODUCTION_LOG_URL,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(payload),
      headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
      success: function (res) {
        if (res.success) {
          showToast("success", res.message);
          batch.length = 0;
          rebuildRows();
          updateBatchUI();
        } else {
          showFormError(
            "#batch-submit-error",
            res.error || "Something went wrong.",
          );
        }
      },
      error: function () {
        showFormError(
          "#batch-submit-error",
          "Something went wrong. Please try again.",
        );
      },
      complete: function () {
        $btn
          .prop("disabled", false)
          .html(
            '<i class="bi bi-check2-all me-1"></i> Submit Production Batch',
          );
      },
    });
  });

  /* ── Escape HTML helper ── */
  function escHtml(str) {
    return $("<div>").text(str).html();
  }
});
