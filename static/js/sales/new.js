$(function () {
  const searchableSelects = makeSearchable("#item-select", {
    placeholder: "Search snack items...",
  });
  const itemSelect = searchableSelects["item-select"];
  const cart = []; // { id, name, unit, price, quantity, subtotal }

  const $emptyState = $("#cart-empty");
  const $rowsList = $("#cart-rows");
  const $submitArea = $("#submit-area");
  const $cartCount = $("#cart-count");

  /* ── Item selected — show info box ── */
  $("#item-select").on("change", function () {
    const $opt = $(this).find(":selected");
    const price = parseFloat($opt.data("price")) || 0;
    const stock = parseInt($opt.data("stock"), 10);
    const unit = $opt.data("unit") || "units";

    if (!$(this).val()) {
      $("#item-info-box").hide();
      $("#unit-display").text("units");
      return;
    }

    $("#info-price").text("TZS " + price.toLocaleString("en-US"));
    $("#info-stock").text(
      stock > 0 ? stock.toLocaleString("en-US") + " " + unit : "Out of stock",
    );
    $("#unit-display").text(unit);
    $("#item-info-box").show();
    $("#item-quantity").focus();
  });

  /* ── Add row to cart ── */
  $("#btn-add-row").on("click", function () {
    const $select = $("#item-select");
    const $qty = $("#item-quantity");
    const itemId = $select.val();
    const $opt = $select.find(":selected");
    const itemName = $opt.data("name");
    const itemUnit = $opt.data("unit");
    const price = parseFloat($opt.data("price")) || 0;
    const stock = parseInt($opt.data("stock"), 10);
    const quantity = parseInt($qty.val(), 10);

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
    if (quantity > stock) {
      showToast(
        "error",
        `Not enough stock. Only ${stock.toLocaleString()} ${itemUnit} available.`,
      );
      $qty.focus();
      return;
    }
    if (cart.find((r) => r.id === itemId)) {
      showToast(
        "error",
        `"${itemName}" is already in the cart. Remove it first to change the quantity.`,
      );
      return;
    }

    const subtotal = price * quantity;
    cart.push({
      id: itemId,
      name: itemName,
      unit: itemUnit,
      price,
      quantity,
      subtotal,
    });
    renderRow(cart.length - 1);
    updateCartUI();

    // Reset inputs
    itemSelect.clear();
    $qty.val("");
    $("#item-info-box").hide();
    $("#unit-display").text("units");
    $select.focus();
  });

  /* ── Enter on quantity adds row ── */
  $("#item-quantity").on("keydown", function (e) {
    if (e.key === "Enter") {
      e.preventDefault();
      $("#btn-add-row").trigger("click");
    }
  });

  /* ── Render a cart row ── */
  function renderRow(index) {
    const r = cart[index];
    const $row = $(`
      <div class="cart-row" id="cart-row-${index}">
        <div class="cart-row-icon"><i class="bi bi-basket"></i></div>
        <div class="cart-row-info">
          <div class="cart-row-name">${escHtml(r.name)}</div>
          <div class="cart-row-meta">${escHtml(r.unit)} &nbsp;·&nbsp; TZS ${r.price.toLocaleString("en-US")} each</div>
        </div>
        <div class="text-end flex-shrink-0">
          <div class="cart-row-subtotal">TZS ${r.subtotal.toLocaleString("en-US")}</div>
          <div class="cart-row-qty-label">× ${r.quantity.toLocaleString()}</div>
        </div>
        <button class="btn-remove-row" data-index="${index}" title="Remove">
          <i class="bi bi-x"></i>
        </button>
      </div>
    `);
    $rowsList.append($row);
  }

  /* ── Remove row ── */
  $(document).on("click", ".btn-remove-row", function () {
    cart.splice(parseInt($(this).data("index"), 10), 1);
    rebuildRows();
    updateCartUI();
  });

  function rebuildRows() {
    $rowsList.empty();
    cart.forEach((_, i) => renderRow(i));
  }

  /* ── Update cart UI ── */
  function updateCartUI() {
    const count = cart.length;
    const totalUnits = cart.reduce((s, r) => s + r.quantity, 0);
    const grandTotal = cart.reduce((s, r) => s + r.subtotal, 0);

    $cartCount.text(count === 1 ? "1 item" : `${count} items`);

    if (count === 0) {
      $emptyState.show();
      $rowsList.hide();
      $submitArea.hide();
    } else {
      $emptyState.hide();
      $rowsList.show();
      $submitArea.show();
      $("#total-item-count").text(count);
      $("#total-units").text(totalUnits.toLocaleString());
      $("#grand-total").text("TZS " + grandTotal.toLocaleString("en-US"));
    }
  }

  /* ── Clear cart ── */
  $("#btn-clear-cart").on("click", function () {
    new bootstrap.Modal("#modal-clear-cart").show();
  });
  $("#btn-confirm-clear").on("click", function () {
    cart.length = 0;
    rebuildRows();
    updateCartUI();
    bootstrap.Modal.getInstance("#modal-clear-cart").hide();
  });

  /* ── Checkout ── */
  $("#btn-checkout").on("click", function () {
    const $btn = $(this);
    const saleDate = $("#sale-date").val();
    const notes = $("#sale-notes").val().trim();
    hideFormError("#cart-submit-error");

    if (!saleDate) {
      showFormError("#cart-submit-error", "Please set a sale date.");
      return;
    }
    if (cart.length === 0) {
      showFormError(
        "#cart-submit-error",
        "Add at least one item before checking out.",
      );
      return;
    }

    $btn
      .prop("disabled", true)
      .html('<i class="bi bi-arrow-repeat me-1"></i> Processing...');

    const payload = {
      sale_date: saleDate,
      notes: notes,
      rows: cart.map((r) => ({ snack_item: r.id, quantity: r.quantity })),
    };

    $.ajax({
      url: window.SALE_NEW_URL,
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(payload),
      headers: { "X-CSRFToken": $("[name=csrfmiddlewaretoken]").val() },
      success: function (res) {
        if (res.success) {
          showToast("success", res.message);
          setTimeout(() => {
            window.location.href = res.redirect_url;
          }, 900);
        } else {
          showFormError(
            "#cart-submit-error",
            res.error || "Something went wrong.",
          );
          $btn
            .prop("disabled", false)
            .html('<i class="bi bi-check2-all me-1"></i> Checkout');
        }
      },
      error: function () {
        showFormError(
          "#cart-submit-error",
          "Something went wrong. Please try again.",
        );
        $btn
          .prop("disabled", false)
          .html('<i class="bi bi-check2-all me-1"></i> Checkout');
      },
    });
  });

  function escHtml(str) {
    return $("<div>").text(str).html();
  }
});
