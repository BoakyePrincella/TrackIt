// Get status counts from the Flask template (you could also use AJAX if needed)
// const statusCounts = {{ status_counts|tojson }};

const statusCounts = 5;


// Pie chart data
const data = {
    labels: ['Not Started', 'In Progress', 'Finished'],
    datasets: [{
        label: 'Task Status Distribution',
        data: [statusCounts['Not Started'], statusCounts['In Progress'], statusCounts['Finished']],
        backgroundColor: ['#FF5733', '#FFBD33', '#33FF57'],
        hoverOffset: 4
    }]
};

// Pie chart options
const options = {
    responsive: true,
    plugins: {
        legend: {
            position: 'top',
        },
        tooltip: {
            callbacks: {
                label: function(tooltipItem) {
                    return tooltipItem.label + ': ' + tooltipItem.raw;
                }
            }
        }
    }
};

// Initialize the pie chart
const ctx = document.getElementById('taskStatusChart').getContext('2d');
new Chart(ctx, {
    type: 'pie',
    data: data,
    options: options
});