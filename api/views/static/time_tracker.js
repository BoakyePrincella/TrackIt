//time_tracker tab

// On page load, check if there's a start time in localStorage
window.onload = () => {
    const savedStartTime = localStorage.getItem('startTime');
    if (savedStartTime) {
        startTime = new Date(savedStartTime);
        startTimer(startTime);
    }
};

// Handle Task Start and Stop
function startTask(){

    // let document.getElementById('start_task_form').addEventListener('click', function(e) {
    //     e.preventDefault();
    var taskName = document.querySelector('input[name="task_name"]').value;
    // Send POST request to start the task using fetch
    fetch('/start-task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'task_name=' + encodeURIComponent(taskName)
    })
    .then(response => response.text())
    .then(data => {
        alert(data);
        // document.getElementById('task_controls').style.display = 'block';
        // window.taskId = data.task_id;
        // alert('Task started at: ' + data.start_time);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.getElementById('stop_task_button').addEventListener('click', function() {
    // Send POST request to stop the task using fetch
    fetch('/stop_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'task_id=' + window.taskId
    })
    .then(response => response.json())
    .then(data => {
        alert('Task stopped at: ' + data.end_time + '\nDuration: ' + data.duration);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

// Handle Timer Start and Stop
document.getElementById('start_timer_form').addEventListener('submit', function(e) {
    e.preventDefault();
    
    var duration = document.querySelector('input[name="duration"]').value;

    // Send POST request to start the timer using fetch
    fetch('/start_timer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'duration=' + encodeURIComponent(duration)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('timer_controls').style.display = 'block';
        window.timerId = data.timer_id;
        alert('Timer started, will end at: ' + data.end_time);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

document.getElementById('stop_timer_button').addEventListener('click', function() {
    var feedback = prompt("Did you finish within the time? If not, please explain:");

    // Send POST request to stop the timer and provide feedback using fetch
    fetch('/stop_timer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'timer_id=' + window.timerId + '&feedback=' + encodeURIComponent(feedback)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message + '\nFeedback: ' + data.feedback);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

let timerInterval;
let startTime;
let activity = ''
let user_id = parseInt(document.getElementById('h_user_id').textContent);
    function startTask() {
        const form = document.getElementById('start_task_form');
        const formData = new FormData(form);
        fetch('/start-task', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            activity = data.activity;
            document.getElementById('task_message').textContent = data.message;
            document.getElementById('start_task_form').classList.add('hidden');
            document.getElementById('start_activity').classList.add('hidden');
            document.getElementById('stop_activity').classList.remove('hidden');
            startTime = new Date(data.start_time);
            localStorage.setItem('startTime', startTime);
            startTimer(startTime);
        });
    }

    function startTimer(startTime) {
        clearInterval(timerInterval);
        timerInterval = setInterval(() => {
            const currentTime = new Date();
            const elapsedTime = Math.floor((currentTime - new Date(startTime)) / 1000);
            const minutes = Math.floor(elapsedTime / 60);
            const seconds = elapsedTime % 60;
            document.getElementById('start_task_form').classList.add('hidden');
            document.getElementById('start_activity').classList.add('hidden');
            document.getElementById('stop_activity').classList.remove('hidden');
            document.getElementById('timer').textContent = `Elapsed time: ${minutes} minute(s) and ${seconds} second(s)`;
        }, 1000);
    }

    function stopTask() {
        clearInterval(timerInterval);
        const elapsedTime = Math.floor((new Date() - new Date(startTime)) / 1000);
        localStorage.removeItem('startTime');
        fetch('/stop-task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ elapsed_time: elapsedTime })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('task_message').textContent = data.message;
            document.getElementById('stop_activity').classList.add('hidden');
            document.getElementById('save_activity').classList.remove('hidden');

        });
    }

    function save() {
        const elapsedTime = Math.floor((new Date() - new Date(startTime)) / 1000);
        localStorage.removeItem('startTime');
        const data = {
            "user": user_id,
            "elapsed_time": elapsedTime,
            "activity": activity
        };
        fetch('/save-task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('task_message').classList.add('hidden');
            document.getElementById('save_message').textContent = data.message;
            document.getElementById('stop_activity').classList.add('hidden');
            document.getElementById('save_activity').classList.remove('hidden');
            setTimeout(() => {
                location.reload();
            }, 4000);
        });
    }


    

    // function stopTask() {
    //     clearInterval(timerInterval);
    //     // You can implement the stop logic here, like sending a request to the server to save the time.
    // }
