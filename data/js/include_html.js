
// Include HTML into the current HTML file
function include_html() {
  ERROR_CODES = {0:"undef", 200:"OK", 404:"NotFound"}

  var z = document.getElementsByTagName("*");
  for (var i = 0; i < z.length; i++) {
    var elem = z[i];
    // Get the elements with the include tag
    file = elem.getAttribute("html-file-path");
    if (file) {
      // Do an HTTP request for the file
      console.log("Found tag, importing '" + file + "'");
      xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
          console.log("HTTP request result: " + this.status + " (" + ERROR_CODES[this.status] + ")")
          console.log("Importing HTML...")
          if (this.status == 200) {elem.innerHTML = this.responseText;}
          else if (this.status == 404) {elem.innerHTML = "Page not found";}
          else {elem.innerHTML = "Could not import HTML"}
          // Remove the attribute, so no endless loops
          elem.removeAttribute("html-file-path");
          console.log("Done, looking for further includes")
          include_html();
        }
      }
      xhttp.open("GET", file, true);
      xhttp.send();
      return;
    }
  }
  console.log("No includes found")
}
