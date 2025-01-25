
//  for modal functionality
// const addTaskButton = document.getElementById('addTaskButton');
// const closeButton = document.getElementById('closeModal');


function openModal() {
    const taskModal = document.getElementById('taskModal');
    taskModal.classList.remove('hidden');
    taskModal.classList.add('flex');

}


function closeM() {
    const taskModal = document.getElementById('taskModal');
    taskModal.classList.add('hidden');
}

function submitTask() {
    const taskForm = document.getElementById('taskForm');
    if (taskForm) {
        const title = document.getElementById('taskTitle').value;
        const description = document.getElementById('taskDescription').value;
        const tstatus = document.querySelector('input[name="status"]:checked').value;

        if (!title && !description && tstatus) {
            document.getElementById('error_msg').textContent = "Title, description and status required";
        } else if (!title) {
            document.getElementById('error_msg').textContent = "Title required";
        } else if (!description) {
            document.getElementById('error_msg').textContent = "Description required";

        } else if (!tstatus) {
            document.getElementById('error_msg').textContent = "Status required";

        } else {
            const data = {
                "title": title,
                "description": description,
                "tstatus": parseInt(tstatus)
            }

            fetch('/add-task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    location.reload();
                    // console.log(data);
                    
                })
                .catch(err => {
                    console.log('Error', err);
                })
                    // document.getElementById('activity_message').classList.add('hidden');
                    // document.getElementById('save_message').textContent = data.message;
            // alert('Form filled rightly');
        }
    }
    else {
        alert('Form required');
    }
    // event.preventDefault();
}
// }
// Open modal when button is clicked
// addTaskButton.addEventListener('click', () => {
//     alert('click');
//     taskModal.classList.remove('hidden');
// });

// // Close modal when the close button is clicked
// closeModal.addEventListener('click', () => {
//     taskModal.classList.add('hidden');
// });

// Close modal when the form is submitted (you can add more logic here to handle the form data)
taskForm.addEventListener('submit', (e) => {
    e.preventDefault();
    // Handle form data submission
    console.log('Title:', taskForm.title.value);
    console.log('Description:', taskForm.description.value);
    taskModal.classList.add('hidden');
});