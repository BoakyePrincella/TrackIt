
//  for modal functionality
// const addTaskButton = document.getElementById('addTaskButton');
const closeButton = document.getElementById('closeModal');
const taskForm = document.getElementById('taskForm');


function openModal(){
    const taskModal = document.getElementById('taskModal');
    taskModal.classList.remove('hidden');
    taskModal.classList.add('flex');

}


function closeM(){
    const taskModal = document.getElementById('taskModal');
    taskModal.classList.add('hidden');
}

function submitTask(event){
    event.preventDefault();
    alert('Submitting')
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