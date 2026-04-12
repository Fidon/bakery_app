$(function () {
  /* ── Sidebar toggle (mobile) ── */
  const $sidebar = $("#sidebar");
  const $overlay = $("#sidebar-overlay");

  $("#sidebar-toggle").on("click", function () {
    $sidebar.toggleClass("open");
    $overlay.toggleClass("open");
  });

  $overlay.on("click", function () {
    $sidebar.removeClass("open");
    $overlay.removeClass("open");
  });

  /* ── Topbar user pill dropdown ── */
  const $userPill = $("#user-pill-toggle");
  const $userDropdown = $("#user-dropdown");
  const $chevron = $("#user-pill-chevron");

  $userPill.on("click", function (e) {
    e.stopPropagation();
    const isOpen = $userDropdown.hasClass("open");
    $userDropdown.toggleClass("open", !isOpen);
    $chevron.toggleClass("open", !isOpen);
  });

  // Close when clicking anywhere outside
  $(document).on("click", function (e) {
    if (!$userPill.is(e.target) && $userPill.has(e.target).length === 0) {
      $userDropdown.removeClass("open");
      $chevron.removeClass("open");
    }
  });

  // Close on Escape key
  $(document).on("keydown", function (e) {
    if (e.key === "Escape") {
      $userDropdown.removeClass("open");
      $chevron.removeClass("open");
    }
  });

  /* ── Toast helper ── */
  window.showToast = function (type, msg) {
    const icons = {
      success: "check-circle-fill",
      error: "x-circle-fill",
      warning: "exclamation-triangle-fill",
    };
    const $t = $(`
      <div class="toast-item ${type}" data-autohide="true">
        <span class="toast-icon"><i class="bi bi-${icons[type] || "info-circle-fill"}"></i></span>
        <div class="toast-body">${msg}</div>
        <button class="toast-close" onclick="$(this).parent().remove()"><i class="bi bi-x"></i></button>
      </div>`);
    if (!$("#toast-container").length)
      $("body").append('<div id="toast-container"></div>');
    $("#toast-container").append($t);
    setTimeout(() => $t.fadeTo(400, 0, () => $t.remove()), 4500);
  };

  /* ── Auto-dismiss toasts ── */
  $('.toast-item[data-autohide="true"]').each(function () {
    const $toast = $(this);
    setTimeout(function () {
      $toast.fadeTo(400, 0, function () {
        $toast.remove();
      });
    }, 4500);
  });

  /* ── Global form error helper ── */
  window.showFormError = function (selector, message) {
    const $el = $(selector);
    $el.find("span").text(message);
    $el.show();
  };

  window.hideFormError = function (selector) {
    $(selector).hide().find("span").text("");
  };

  /* ── Global Ajax session-expiry handler ── */
  $(document).ajaxError(function (event, xhr) {
    if (xhr.status === 401) {
      try {
        const res = JSON.parse(xhr.responseText);
        if (res.session_expired) {
          // Show a toast if the container exists, then redirect to login
          if (typeof showToast === "function") {
            showToast(
              "warning",
              res.error || "Session expired. Redirecting to login...",
            );
          }
          setTimeout(function () {
            window.location.href =
              "/login/?next=" + encodeURIComponent(window.location.pathname);
          }, 1800);
        }
      } catch (e) {
        window.location.href = "/login/";
      }
    }
  });
});

/* ── Searchable select — global utility ── */
window.makeSearchable = function (selector, options) {
  const defaults = {
    placeholder: "Search or select...",
    allowEmptyOption: true,
    maxOptions: 200,
    highlight: true,
  };
  const config = Object.assign({}, defaults, options || {});
  const instances = {};
  document.querySelectorAll(selector).forEach(function (el) {
    if (el.tomselect) return;
    instances[el.id || selector] = new TomSelect(el, config);
  });
  return instances;
};
