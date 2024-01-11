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
var initialContent = document.querySelector('.initial-content');
var oneIdeaForm = document.querySelector('.idea-form');
var multipleIdeasForm = document.querySelector('.multiple-ideas-form');

function showOneIdeaForm() {
    hideInitialContent();
    showForm(oneIdeaForm);
}

function showMultipleIdeasForm() {
    hideInitialContent();
    showForm(multipleIdeasForm);
}

function hideInitialContent() {
    if (initialContent) {
        initialContent.style.display = 'none';
    }
}

function showForm(formElement) {
    if (formElement) {
        formElement.style.display = 'block';
    }
}

function goBack() {
    if (initialContent && oneIdeaForm && multipleIdeasForm) {
        initialContent.style.display = 'block';
        oneIdeaForm.style.display = 'none';
        multipleIdeasForm.style.display = 'none';
    }
}


// Get all elements with the class 'limitedText'
var textElements = document.querySelectorAll('.limitedText');

// Iterate through each element
textElements.forEach(function (textElement) {
    // Check if the text content is longer than 150 characters
    if (textElement.textContent.length > 150) {
        // Truncate the text and append '...'
        textElement.textContent = textElement.textContent.substring(0, 150) + '...';
    }
});

function getDetails(identifier) {
    $.ajax({
        url: '/get_details/' + identifier,
        type: 'GET',
        success: function (response) {
            // Handle the response, e.g., display details in a modal
            console.log(response);
        },
        error: function (error) {
            console.error('Error:', error);
        }
    });
}

function validateForm() {
    // Get the file input element
    var fileInput = document.querySelector('input[name="csvFile"]');

    // Check if the file input is empty
    if (!fileInput.files.length) {
        // Show a pop-up message
        alert('Please upload a file.');
        // Prevent form submission
        return false;
    }

    // Allow form submission if the file is selected
    return true;
}


// here is code for expanded text
document.addEventListener("DOMContentLoaded", function() {
    var truncateContainers = document.querySelectorAll('.truncate-container');
    var readMoreLinks = document.querySelectorAll('.read-more');

    readMoreLinks.forEach(function(link, index) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            toggleReadMore(truncateContainers[index], link);
        });
    });
});

function toggleReadMore(truncateContainer, readMoreLink) {
    var expandedClass = 'expanded';
    var buttonText = readMoreLink.textContent.trim();

    truncateContainer.classList.toggle(expandedClass);

    // Toggle button text based on the current state
    if (truncateContainer.classList.contains(expandedClass)) {
        readMoreLink.textContent = 'Read less';
    } else {
        readMoreLink.textContent = 'Read more';
    }
}

