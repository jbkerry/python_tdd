window.CargoLists = {};
window.CargoLists.initialize = () => {
  $('input[name="text"]').on('keypress focus', () => {
    $('.has-error').hide();
  });
};