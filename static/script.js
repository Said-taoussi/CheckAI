var metricCounter = 6; // Initialize a counter

function addMetric(containerId, title) {
    // Create new metric container
    var newMetricContainer = document.createElement('div');
    newMetricContainer.className = 'column'; // Set the class name to match your existing column structure

    // Create new metric title
    var newTitle = document.createElement('h3');
    newTitle.textContent = title;

    // Increment the counter for each new metric
    var metricName = 'metric' + metricCounter;
    var weightName = 'weight' + metricCounter;
    var descriptionName = 'description' + metricCounter;

    // Create new metric elements
    var newMetricElement = document.createElement('div');
    newMetricElement.className = 'metric-container';

    var newMetricTextElement = document.createElement('div');
    newMetricTextElement.className = 'text-element';
    newMetricTextElement.innerHTML = `<h4>Metric</h4><input name="${metricName}" type="text" placeholder="Enter metric...">`;

    var newweightTextElement = document.createElement('div');
    newweightTextElement.className = 'text-element weight-container';
    newweightTextElement.innerHTML = `<h4>Weight</h4><input name="${weightName}" type="number" placeholder="Enter weight..." value="0" min="0" max="20">`;

    var newDescriptionTextElement = document.createElement('div');
    newDescriptionTextElement.className = 'text-element description-container';
    newDescriptionTextElement.innerHTML = `<h4>Description</h4><textarea name="${descriptionName}" placeholder="Enter description..."></textarea>`;

    // Append new elements
    newMetricElement.appendChild(newMetricTextElement);
    newMetricElement.appendChild(newweightTextElement);
    newMetricElement.appendChild(newDescriptionTextElement);
    newMetricContainer.appendChild(newTitle);
    newMetricContainer.appendChild(newMetricElement);
    document.getElementById(containerId).appendChild(newMetricContainer);

    // Increment the counter for the next metric
    metricCounter++;
}
