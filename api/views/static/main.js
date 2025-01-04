// function dropdown() {
//     document.querySelector("#submenu").classList.toggle("hidden");
//     document.querySelector("#arrow").classList.toggle("rotate-0");
// }
// dropdown();

function openSidebar() {
    document.querySelector(".sidebar").classList.toggle("hidden");
}

// Function to handle screen resizing
function handleResize() {
    const sidebar = document.querySelector('.sidebar');
    const button = document.querySelector('.absolute');

    if (window.innerWidth >= 1024) {
        sidebar.classList.remove('hidden');
        button.classList.add('hidden');
    } else {
        sidebar.classList.add('hidden');
        button.classList.remove('hidden');
    }
}

window.addEventListener('resize', handleResize);
handleResize();


document.addEventListener('DOMContentLoaded', function () {
    const contentDiv = document.getElementById('dynamic-content');
    const loader = document.getElementById('loader');

    //fetch home page by default
    let url = window.location.pathname || '/home';
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            loader.classList.add('hidden');
            contentDiv.innerHTML = html;
            history.pushState(null, '', url);
        })
        .catch(error => {
            console.error("Error fetching the page:", error);
            loader.classList.add('hidden');
            contentDiv.innerHTML = '<p>Error loading content</p>';
        });


    document.addEventListener('click', function (e) {
        const link = e.target.closest('.sidebar-link');
        if (link) {
            e.preventDefault();
            url = link.getAttribute('data-url');
            contentDiv.innerHTML = '';
            loader.classList.remove('hidden');

            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`);
                    }
                    return response.text();
                })
                .then(html => {
                    loader.classList.add('hidden');
                    contentDiv.innerHTML = html;
                    history.pushState(null, '', url); // Update the URL without reloading

                })
                .catch(error => {
                    console.error("Error fetching the page:", error);
                    loader.classList.add('hidden');
                    contentDiv.innerHTML = '<p>Error loading content</p>';
                });
        }
    });

    window.addEventListener('popstate', function () {
        const currentUrl = window.location.pathname;
        fetch(currentUrl)
            .then(response => response.text())
            .then(html => {
                contentDiv.innerHTML = html; // Load content based on current URL
            })
            .catch(error => {
                console.error("Error fetching the page on popstate:", error);
                contentDiv.innerHTML = '<p>Error loading content</p>'; // Display error message
            });
    });


});
