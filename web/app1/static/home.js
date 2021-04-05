/*function myFunction() {
      document.getElementById("myDropdown").classList.toggle("show");
}*/

    // Close the dropdown menu if the user clicks outside of it

    /* Open when someone clicks on the span element */
    function openNav() {
      document.getElementById("myNav").style.width = "100%";
      document.getElementsByTagName("BODY")[0].style.overflow = "hidden";
    }

    /* Close when someone clicks on the "x" symbol inside the overlay */
    function closeNav() {
      document.getElementById("myNav").style.width = "0%";
      document.getElementsByTagName("BODY")[0].style.overflow = "auto";
    }

// Get the modal
var modal = document.getElementById("myModal");

// Get the button that opens the modal
var tutorial = document.getElementById("tutorial");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

window.onload = function() {
  // Get the modal
  modal = document.getElementById("myModal");

  // Get the button that opens the modal
  tutorial = document.getElementById("modelP");

  // Get the <span> element that closes the modal
  span = document.getElementsByClassName("close")[0];

};

// HOME

tutorial.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    document.getElementById("btnTop").style.display = "block";
  } else {
    document.getElementById("btnTop").style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}

window.onclick = function(event) {
  if (event.target == myDropdown) {
    myDropdown.style.display = "none";
  }
}
