window.addEventListener('load', function() {
    // 1. Select ALL elements whose ID contains the string '"type":"sub_task_email"'
    const targets = document.querySelectorAll("[id*='\"type\":\"sub_task_email\"']");
    console.log("Targets found:");
    // 2. Loop through each found element and attach the event listener
    targets.forEach(target => {
        // Find the dcc.Store component (this can be outside the loop if it's always the same)
        const store = document.getElementById('task-email-event-store');

        const handleMouseClick = (event) => {
            // Prevent the default right-click menu
            if (event.type === 'contextmenu') {
                event.preventDefault();
            }

            // Get the full ID of the specific element that was clicked
            const clickedId = JSON.parse(target.id);

            // Create a data payload to send to Python
            const payload = {
                click_type: (event.type === 'click') ? 'left' : 'right',
                shift_key: event.shiftKey,
                // Include the ID of the element that was clicked
                source_id: clickedId,
                // Add a timestamp to ensure the callback always fires
                ts: new Date().getTime()
            };

            // Update the dcc.Store with our payload
            if (store) {
                store.setAttribute('data_email_just_clicked', JSON.stringify(payload));
            }
        };

        // Attach listeners to the current target element
        target.addEventListener('click', handleMouseClick);
        target.addEventListener('contextmenu', handleMouseClick);
    });
});