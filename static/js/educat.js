var sysdate = new Date();

// Get all rows from the table
var rows = document.querySelectorAll('#example tr');

// Iterate through each row
rows.forEach(function(row) {
  // Get the date from the first column of the current row
  var dateStr = row.cells[0].textContent.trim();
  var rowDate = new Date(dateStr);

  // Compare row date with sysdate
  if (rowDate > sysdate) {
    // Apply yellow color to the row
    row.classList.add('yellow-row');
  } else {
    // Apply red color to the row
    row.classList.add('red-row');
  }
});