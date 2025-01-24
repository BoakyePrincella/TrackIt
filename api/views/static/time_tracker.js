//time_tracker tab

// On page load, check if there's a start time in localStorage
window.onload = () => {
    const savedStartTime = localStorage.getItem('startTime');
    if (savedStartTime) {
        startTime = new Date(savedStartTime);
        startTimer(startTime);
    }
};

// Stop the ongoing activity
document.getElementById('stop_activity_button').addEventListener('click', function () {
    // Send POST request to stop the activity using fetch
    fetch('/stop_activity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'activity_id=' + window.activityId
    })
        .then(response => response.json())
        .then(data => {
            alert('activity stopped at: ' + data.end_time + '\nDuration: ' + data.duration);
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

// Handle Timer Start and Stop
document.getElementById('start_timer_form').addEventListener('submit', function (e) {
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

document.getElementById('stop_timer_button').addEventListener('click', function () {
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
let [minutes, seconds] = [];

// Starts the activity
function startActivity() {
    if (document.getElementById('activity_name').value) {

        const form = document.getElementById('start_activity_form');
        const formData = new FormData(form);
        fetch('/start-activity', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                activity = data.activity;
                document.getElementById('activity_message').textContent = data.message;
                document.getElementById('start_activity_form').classList.add('hidden');
                document.getElementById('start_activity').classList.add('hidden');
                document.getElementById('stop_activity').classList.remove('hidden');
                startTime = new Date(data.start_time);
                localStorage.setItem('startTime', startTime);
                startTimer(startTime);
            });
    } else {
        alert('Activity name must be set');
    }
}
// The time counting function
function startTimer(startTime) {
    clearInterval(timerInterval);
    timerInterval = setInterval(() => {
        const currentTime = new Date();
        const elapsedTime = Math.floor((currentTime - new Date(startTime)) / 1000);
        const minutes = Math.floor(elapsedTime / 60);
        const seconds = elapsedTime % 60;
        document.getElementById('start_activity_form').classList.add('hidden');
        document.getElementById('start_activity').classList.add('hidden');
        document.getElementById('stop_activity').classList.remove('hidden');
        document.getElementById('timer').textContent = `Elapsed time: ${minutes} minute(s) and ${seconds} second(s)`;
    }, 1000);
}


function stopActivity() {
    clearInterval(timerInterval);
    const elapsedTime = Math.floor((new Date() - new Date(startTime)) / 1000);
    localStorage.removeItem('startTime');
    fetch('/stop-activity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ elapsed_time: elapsedTime })
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('activity_message').textContent = data.message;
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
    fetch('/save-activity', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('activity_message').classList.add('hidden');
            document.getElementById('save_message').textContent = data.message;
            document.getElementById('stop_activity').classList.add('hidden');
            document.getElementById('save_activity').classList.remove('hidden');
            setTimeout(() => {
                location.reload();
            }, 4000);
        });
}


let timerInterval_ct;

// Set timer for a set duration(count down)
function setTimer() {
    const durationInput = document.getElementById('duration').value;
    if (durationInput) {
        const form = document.getElementById('start_timer_form');
        const formData = new FormData(form);
        fetch('/start-timer', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                [minutes, seconds] = [data.min, data.sec];
                document.getElementById('start_timer_form').classList.add('hidden');
                document.getElementById('stop_timer_button').classList.remove('hidden');
                startCountdown(minutes, seconds);
                // document.getElementById('activity_message').textContent = data.message;
            });
    } else {
        alert('Duration for timer must be set');
    }

}

function startCountdown(minutes, seconds) {
    let totalTime = minutes * 60 + seconds;
    document.getElementById('timer_controls').classList.remove('hidden');

    timerInterval_ct = setInterval(() => {
        if (totalTime <= 0) {
            clearInterval(timerInterval_ct);
            playSound()
            document.getElementById('timerr').classList.add('hidden');
            document.getElementById('time_up').innerHTML = "Time's Up";
            document.getElementById('save_timer').classList.remove('hidden');
            document.getElementById('stop_timer_button').classList.add('hidden');

            return;
        }

        totalTime--;
        const mins = Math.floor(totalTime / 60);
        const secs = totalTime % 60;
        document.getElementById('countdown_timer').textContent = `${mins} min ${secs} sec`;
    }, 1000);
}


function saveTimer() {
    let totalSeconds = minutes * 60 + seconds;
    const data = {
        "user": user_id,
        "set_time": totalSeconds
    };
    fetch('/save-timer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            // alert(data.message)
            document.getElementById('time_up').classList.add('hidden');
            document.getElementById('timer_message').textContent = data.message;
            document.getElementById('save_timer').classList.add('hidden');
            // document.getElementById('save_activity').classList.remove('hidden');
            setTimeout(() => {
                location.reload();
            }, 2000);
        });
}

function playSound() {
    const sound = document.getElementById('timer_sound');
    sound.play();

}

function stopSound() {
    const sound = document.getElementById('timer_sound');
    sound.pause();
    sound.currentTime = 0;
}

function stopTimer() {
    clearInterval(timerInterval_ct);
    alert('Timer stopped');
    // stopSound();
}

function loadHistory(tab){
    // const url = {{ url_for(user_bp.timer_history)}};
    if (tab == 'activities'){
        document.getElementById('timers_hist').classList.remove('underline')
        document.getElementById('activities_hist').classList.add('underline')
    } else if (tab == 'timers'){
        document.getElementById('activities_hist').classList.remove('underline')
        document.getElementById('timers_hist').classList.add('underline')

        fetch('/timers-history')
        .then(res => {
            if(!res.ok){
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return res.json()
        })
        .then(data => {
            document.getElementById('activities_hist_content').classList.add('hidden')
            console.log(data)  
        })
    }
    // alert(tab);
}