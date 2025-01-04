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