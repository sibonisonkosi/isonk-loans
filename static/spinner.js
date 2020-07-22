$(document).ready(function() {
    $("#btnFetch").click(function() {
      $(this).prop("disabled", true);
      $(this).html(
        `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Loadingg...`
      );
    });
});