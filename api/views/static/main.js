// function dropdown() {
//     document.querySelector("#submenu").classList.toggle("hidden");
//     document.querySelector("#arrow").classList.toggle("rotate-0");
// }
// dropdown();

function openSidebar() {
    const sidebar = document.querySelector(".sidebar");
    sidebar.classList.toggle("hidden");
    // Add an event listener to close the sidebar when clicking outside or on the close button
    if (!sidebar.classList.contains('hidden')) {
        document.addEventListener('click', handleOutsideClick, true);
    } else {
        document.removeEventListener('click', handleOutsideClick, true);
    }
}


function handleOutsideClick(event) {
    const sidebar = document.querySelector('.sidebar');
    const toggleButton = document.querySelector('.bi-filter-left');
    if (!sidebar.contains(event.target) && !toggleButton.contains(event.target)) {
        openSidebar();
    }
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

    //fetch curent path or dashboard page by default
    let url = window.location.pathname;
    if (url === '/') {
        url = '/dashboard';
    }

    document.querySelectorAll('.sidebar-link').forEach(item => {
        item.querySelector('div').classList.remove('bg-blue-600');
    });

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
            // After the content is loaded, find the sidebar link and apply the background color
            const activeLink = document.querySelector(`.sidebar-link[data-url="${url}"]`);
            if (activeLink) {
                const div = activeLink.querySelector('div');
                div.classList.add('bg-blue-600');
            }
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
            document.querySelectorAll('.sidebar-link').forEach(item => {
                item.querySelector('div').classList.remove('bg-blue-600');
            });

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
                    const div = link.querySelector('div');
                    div.classList.add('bg-blue-600');
                    history.pushState(null, '', url);
                    this.location.reload();


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

