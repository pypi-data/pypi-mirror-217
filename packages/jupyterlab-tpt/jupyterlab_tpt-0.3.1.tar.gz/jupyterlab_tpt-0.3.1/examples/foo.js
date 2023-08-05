function calculateDaysBetweenDates(date1, date2) {
  // your code goes here
  return Math.abs(date1 - date2) / (1000 * 60 * 60 * 24)
}

// find all images without alternative text
// and give them a red border
function process() {
  const images = document.querySelectorAll('img')
  images.forEach(img => {
    if (!img.alt) {
      img.style.border = '2px solid red'
    }
  })
}
