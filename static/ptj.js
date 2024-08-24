
  const navMenu = document.getElementById("nav-menu"),
    navToggle = document.getElementById("nav-toggle");
  navClose = document.getElementById("nav-close");
  if (navToggle) {
    navToggle.addEventListener("click", () => {
      navMenu.classList.add("show-menu");
    });
  }

  if (navClose) {
    navClose.addEventListener("click", () => {
      navMenu.classList.remove("show-menu");
    });
  }

  /*==================== REMOVE MENU MOBILE ====================*/
  const navLink = document.querySelectorAll(".nav__link");

  function linkAction() {
    const navMenu = document.getElementById("nav-menu");
    // When we click on each nav__link, we remove the show-menu class
    navMenu.classList.remove("show-menu");
  }
  navLink.forEach((n) => n.addEventListener("click", linkAction));

  /*======================= ACCORD SKILLS ======================*/

  const skillsContent = document.getElementsByClassName("skills__content"),
    skillsHeader = document.querySelectorAll(".skills__header");

  function toggleSkills() {
    let itemClass = this.parentNode.className;

    for (i = 0; i < skillsContent.length; i++) {
      skillsContent[i].className = "skills__content skills__close";
    }
    if (itemClass === "skills__content skills__close") {
      this.parentNode.className = "skills__content skills__open";
    }
  }

  skillsHeader.forEach((el) => {
    el.addEventListener("click", toggleSkills);
  });


  /*======================= Services Modal ===================*/
  const modalViews = document.querySelectorAll(".services__modal"),
    modalBtns = document.querySelectorAll(".services__button"),
    modalCloses = document.querySelectorAll(".services__modal-close");

  let modal = function (modalClick) {
    modalViews[modalClick].classList.add("active-modal");
  };

  modalBtns.forEach((modalBtn, i) => {
    modalBtn.addEventListener("click", () => {
      modal(i);
    });
  });

  modalCloses.forEach((modalClose) => {
    modalClose.addEventListener("click", () => {
      modalViews.forEach((modalView) => {
        modalView.classList.remove("active-modal");
      });
    });
  });

  /*======================= Swiper ===================*/
  var swiper = new Swiper(".portfolio__container", {
    cssMode: true,
    loop: true,

    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });

  /*==================== SCROLL SECTIONS ACTIVE LINK ====================*/
  const sections = document.querySelectorAll("section[id]");

  function scrollActive() {
    const scrollY = window.pageYOffset;

    sections.forEach((current) => {
      const sectionHeight = current.offsetHeight;
      const sectionTop = current.offsetTop - 50;
      sectionId = current.getAttribute("id");

      if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
        document
          .querySelector(".nav__menu a[href*=" + sectionId + "]")
          .classList.add("active-link");
      } else {
        document
          .querySelector(".nav__menu a[href*=" + sectionId + "]")
          .classList.remove("active-link");
      }
    });
  }
  window.addEventListener("scroll", scrollActive);

  /*==================== CHANGE BACKGROUND HEADER ====================*/
  function scrollHeader() {
    const nav = document.getElementById("header");
    // When the scroll is greater than 200 viewport height, add the scroll-header class to the header tag
    if (this.scrollY >= 80) nav.classList.add("scroll-header");
    else nav.classList.remove("scroll-header");
  }
  window.addEventListener("scroll", scrollHeader);

  /*==================== SHOW SCROLL up ====================*/
  function scrollUp() {
    const scrollUp = document.getElementById("scroll-up");
    // When the scroll is higher than 560 viewport height, add the show-scroll class to the a tag with the scroll-top class
    if (this.scrollY >= 560) scrollUp.classList.add("show-scroll");
    else scrollUp.classList.remove("show-scroll");
  }
  window.addEventListener("scroll", scrollUp);

  /*==================== DARK LIGHT THEME ====================*/
  const themeButton = document.getElementById("theme-button");
  const darkTheme = "dark-theme";
  const iconTheme = "uil-sun";

  // Previously selected topic (if user selected)
  const selectedTheme = localStorage.getItem("selected-theme");
  const selectedIcon = localStorage.getItem("selected-icon");

  // We obtain the current theme that the interface has by validating the dark-theme class
  const getCurrentTheme = () =>
    document.body.classList.contains(darkTheme) ? "dark" : "light";
  const getCurrentIcon = () =>
    themeButton.classList.contains(iconTheme) ? "uil-moon" : "uil-sun";

  // We validate if the user previously chose a topic
  if (selectedTheme) {
    // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
    document.body.classList[selectedTheme === "dark" ? "add" : "remove"](
      darkTheme,
    );
    themeButton.classList[selectedIcon === "uil-moon" ? "add" : "remove"](
      iconTheme,
    );
  }

  // Activate / deactivate the theme manually with the button
  themeButton.addEventListener("click", () => {
    // Toggle the dark / icon theme
    const newTheme = document.body.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.body.setAttribute('data-theme', newTheme);
    themeButton.classList.toggle(iconTheme);
    
    // Save the theme and icon in localStorage
    localStorage.setItem("selected-theme", newTheme);
    localStorage.setItem("selected-icon", getCurrentIcon());});

  // Activate / deactivate the theme manually with the button
  themeButton.addEventListener("click", () => {
    // Add or remove the dark / icon theme
    document.body.classList.toggle(darkTheme);
    themeButton.classList.toggle(iconTheme);
    // We save the theme and the current icon that the user chose
    localStorage.setItem("selected-theme", getCurrentTheme());
    localStorage.setItem("selected-icon", getCurrentIcon());
    
  });

  document.addEventListener('DOMContentLoaded', function () {
    const patientForm = document.getElementById('patientForm');
    
    if (patientForm) {
        patientForm.addEventListener('submit', function (event) {
            event.preventDefault(); // Prevent default form submission

            const formData = new FormData(patientForm);

            // Show the loading overlay using SweetAlert2
            Swal.fire({
                title: 'Processing...',
                text: 'Please wait while we process your data.',
                didOpen: () => {
                    Swal.showLoading(); // Show the loading spinner
                },
                allowOutsideClick: false // Prevent closing the loading overlay by clicking outside
            });

            fetch('/submit', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(result => {
                const sepsis_status = result.sepsis_status;

                // Hide the loading overlay and show the alert based on the sepsis_status
                Swal.fire({
                    title: sepsis_status === 'Positive' ? 'Alert' : 'No Threat',
                    text: sepsis_status === 'Positive' ? 'Sepsis Status is Positive! Early intervention is required.' : 'No sepsis threat found.',
                    icon: sepsis_status === 'Positive' ? 'warning' : 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    // Create a new row object based on the form data
                    const newRow = {
                        'First Name': formData.get('fname'),
                        'Last Name': formData.get('Lname'),
                        'Gender': formData.get('gender'),
                        'Temperature': formData.get('temperature'),
                        'Heart Rate': formData.get('heart-rate'),
                        'Respiratory Rate': formData.get('respiratory-rate'),
                        'White Blood Cells': formData.get('wcb'),
                        'Blood Group': formData.get('blood-group'),
                        'Your Concerns': formData.get('You Concerns'),
                        'Sepsis': sepsis_status
                    };

                    // Add the new row to the table
                    const tableBody = document.querySelector('#alert-table tbody');
                    const tableRow = createTableRow(newRow);
                    tableBody.innerHTML = tableRow + tableBody.innerHTML; // Insert the new row at the top

                    // Reset the form after submission
                    patientForm.reset();

                    // Reload the CSV data to reflect any changes
                    loadCSV();
                });
            })
            .catch(error => {
                console.error('Error:', error);

                // Hide the loading overlay and show an error alert
                Swal.fire({
                    title: 'Error',
                    text: 'An error occurred while processing your request.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                }).then(() => {
                    // Optionally, you can reset or update the form here
                });
            });
        });
    }

    // Path to your CSV file
    const csvFilePath = '../static/data.csv';

    // Variable to keep track of how many rows are currently displayed
    let rowsDisplayed = 0;
    let csvData = [];

    // Function to create a table row
    function createTableRow(data) {
        return `
            <tr>
                <td>${data['First Name']}</td>
                <td>${data['Last Name']}</td>
                <td>${data['Gender']}</td>
                <td>${data['Temperature']}°C</td>
                <td>${data['Heart Rate']} bpm</td>
                <td>${data['Respiratory Rate']} breaths/min</td>
                <td>${data['White Blood Cells']} /mm³</td>
                <td>${data['Blood Group']}</td>
                <td>${data['Your Concerns']}</td>
                <td>${data['Sepsis']}</td>
            </tr>
        `;
    }

    // Function to load and process the CSV data
    function loadCSV() {
        Papa.parse(csvFilePath, {
            download: true,
            header: true,
            complete: function(results) {
                csvData = results.data.slice(0, -1); // Remove the last row (if needed)
                displayRows(); // Display the initial set of rows
            }
        });
    }

    // Function to display rows (initially 5 and then 5 more each time)
    function displayRows() {
        const tableBody = document.querySelector('#alert-table tbody');
        const rowsToDisplay = csvData.slice(rowsDisplayed, rowsDisplayed + 5); // Get the next 5 rows

        rowsToDisplay.forEach(row => {
            const tableRow = createTableRow(row);
            tableBody.innerHTML += tableRow;
        });

        rowsDisplayed += 5; // Update the number of displayed rows

        // Hide the "Load More" button if all rows are displayed
        if (rowsDisplayed >= csvData.length) {
            document.querySelector('#load-more-btn').style.display = 'none';
        }
    }

    // Event listener for the "Load More" button
    document.querySelector('#load-more-btn').addEventListener('click', displayRows);

    // Load CSV data on page load
    window.onload = loadCSV;
});
