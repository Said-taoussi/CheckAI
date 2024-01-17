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

    // Check the file type
    var fileName = fileInput.files[0].name;
    var fileType = fileName.split('.').pop().toLowerCase();
    
    // Check if the file type is either CSV or Excel
    var allowedTypes = ['csv', 'xlsx', 'xls'];
    if (!allowedTypes.includes(fileType)) {
        alert('Please upload a valid CSV or Excel file.');
        return false;
    }

    // Allow form submission if the file is selected and the type is valid
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

function submitForm() {
    // Validate the form before submission
    if (!validateForm()) {
        return;
    }

    // Show the loader
    document.getElementById("loaderContainer").style.display = "flex";
  
}



function validateForm1() {
    var problem = document.getElementById("problemTextarea").value.trim();
    var solution = document.getElementById("solutionTextarea").value.trim();

    if (problem === "" || solution === "") {
        alert("Please fill in both the problem and solution fields.");
        return false;
    }

    // Additional validation logic can be added if needed

    return true;
}



  function submitForm1() {
    // Get form data
    var problem = document.getElementById("problemTextarea").value.trim();
    var solution = document.getElementById("solutionTextarea").value.trim();
  
    // Perform form validation
    if (problem === "" || solution === "") {
      alert("Please fill in both the problem and solution fields.");
      return;
    }
  
    // Show the loader
    document.getElementById("loaderContainer").style.display = "flex";
  }
  
function fillTextAreas() {
    // Predefined text values
    var predefinedProblem = "The construction industry is indubitably one of the significant contributors to global waste, contributing approximately 1.3 billion tons of waste annually, exerting significant pressure on our landfills and natural resources. Traditional construction methods entail single-use designs that require frequent demolitions, leading to resource depletion and wastage.";
    var predefinedSolution = "Herein, we propose an innovative approach to mitigate this problem: Modular Construction. This method embraces recycling and reuse, taking a significant stride towards a circular economy.   Modular construction involves utilizing engineered components in a manufacturing facility that are later assembled on-site. These components are designed for easy disassembling, enabling them to be reused in diverse projects, thus significantly reducing waste and conserving resources.  Not only does this method decrease construction waste by up to 90%, but it also decreases construction time by 30-50%, optimizing both environmental and financial efficiency. This reduction in time corresponds to substantial financial savings for businesses. Moreover, the modular approach allows greater flexibility, adapting to changing needs over time.  We believe, by adopting modular construction, the industry can transit from a 'take, make and dispose' model to a more sustainable 'reduce, reuse, and recycle' model, driving the industry towards a more circular and sustainable future. The feasibility of this concept is already being proven in markets around the globe, indicating its potential for scalability and real-world application.";

    // Set the values to the text areas
    document.getElementById("problemTextarea").value = predefinedProblem;
    document.getElementById("solutionTextarea").value = predefinedSolution;
}

function clearTextAreas() {
    // Predefined text values
    var predefinedProblem = "";
    var predefinedSolution = "";

    // Set the values to the text areas
    document.getElementById("problemTextarea").value = predefinedProblem;
    document.getElementById("solutionTextarea").value = predefinedSolution;
}

function sendMessage() {
    var userMessage = document.getElementById('user-input').value;

    if (userMessage.trim() === '') {
        return;
    }
    
    document.getElementById('chat-box').innerHTML += '<p><strong style="color: #3498db; font-weight: bold;">You:</strong> ' + userMessage + '</p>';
    var requestData = new URLSearchParams();
    requestData.append('user_message', userMessage);
    requestData.append('additional_data', JSON.stringify(additionalData));
    // Send user message to Flask server
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded', // Set content type to URL-encoded
        },
        body: requestData,
    })
    .then(response => response.json())
    .then(data => {
        var chatBotResponse = data.response;
        document.getElementById('chat-box').innerHTML += '<p><strong style="color: #3498db; font-weight: bold;">CheckAI:</strong> ' + chatBotResponse + '</p>';
    });

    document.getElementById('user-input').value = '';
}

// Listen for "Enter" key press
document.getElementById('user-input').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        // Prevent the default behavior (form submission)
        event.preventDefault();
        
        // Call the sendMessage function
        sendMessage();
    }
});
