function addLeadingZero(num) {
  return num.toString().length == 2 ? num.toString() : "0" + num.toString();
}

function getTime() {
  const d = new Date();
  let hh = addLeadingZero(d.getHours());
  let mm = addLeadingZero(d.getMinutes());
  let ss = addLeadingZero(d.getSeconds());
  return `${hh}:${mm}:${ss}`;
}
