window.CargoLists = {};
window.CargoLists.initialize = function () {
  $('input[name="text"]').on('keypress focus', function () {
    $('.has-error').hide();
  });
};