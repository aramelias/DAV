// Run all imported scripts
function run_scripts () {
  var z = document.getElementsByTagName("script");
  for (var i = 0; i < z.length; i++) {
    var elem = z[i];
    var check = elem.getAttribute("script-imported-run-please");
    if (check && check == "True") {
      check = elem.getAttribute("src");
      if (check) {
        // Check is now the source location, so let's fetch it
        console.log("Found script w/source, downloading source...")
        xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
          if (this.readyState == 4) {
            if (this.status == 200) {
              console.log("Running script source...")
              var code = JSON.parse(this.responseText);
              console.log(code);
              eval(code);
            }
            else {console.log("Download of script failed (" + this.status + ")");}
            // Remove the attribute, so no endless loops
            elem.removeAttribute("script-imported-run-please");
            // Try all over again
            run_scripts();
          }
        }
        xhttp.open("GET", check, true);
        xhttp.send();
        return;
      }
      // No source, run script inner HTML
      if (elem.innerHTML.length > 0) {
        console.log("Running script...");
        eval(elem.innerHTML);
      }
      // Remove tag & try again
      elem.removeAttribute("script-imported-run-please");
      run_scripts();
      return;
    }
  }
  console.log("No to-be-run scripts are found.")
}

// Include HTML into the current HTML file
function include_html() {
  ERROR_CODES = {0:"undef", 200:"OK", 404:"NotFound"}

  var z = document.getElementsByTagName("*");
  for (var i = 0; i < z.length; i++) {
    var elem = z[i];
    // Get the elements with the include tag
    file = elem.getAttribute("html-file-url");
    if (file) {
      // Do an HTTP request for the file
      console.log("Found tag, importing '" + file + "'");
      xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
          console.log("HTTP request result: " + this.status + " (" + ERROR_CODES[this.status] + ")")
          console.log("Importing HTML...")
          if (this.status == 200) {
            elem.innerHTML = this.responseText;
            console.log("Flagging new scripts so they can be run later...")
            var new_code = elem.innerHTML;
            var elems = elem.getElementsByTagName("script");
            for (var j = 0; j < elems.length; j++) {
              elems[j].setAttribute("script-imported-run-please", "True");
            }
          }
          else if (this.status == 404) {elem.innerHTML = "Page not found";}
          else {elem.innerHTML = "Could not import HTML"}
          // Remove the attribute, so no endless loops
          elem.removeAttribute("html-file-url");
          console.log("Done, looking for further includes")
          include_html();
        }
      }
      xhttp.open("GET", file, true);
      xhttp.send();
      return;
    }
  }
  console.log("No includes found");
  // Now check for any scripts that need to run
  run_scripts();
}
