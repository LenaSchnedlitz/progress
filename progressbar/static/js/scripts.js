/**
 * Toggles the color input visibility.
 */
function toggleColorBox(show) {
  const colorBox = document.getElementById('color-input-wrapper');
  if (show) {
    colorBox.classList.remove('hidden');
  } else {
    colorBox.classList.add('hidden');
  }
}

/**
 * Returns the currently selected theme-input option.
 */
function selectedOption() {
  const selection = document.getElementById('theme-input');
  return selection.options[selection.selectedIndex].value;
}
