const iconOnPath = '/static/icon-on.png';
const iconOffPath = '/static/icon-off.png';

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
 document.querySelectorAll('.favorite-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        const turtleId = this.dataset.turtleId;
        const isFavorite = this.checked;

        fetch('/update_favorite', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ turtle_id: turtleId, favorite: isFavorite })
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                alert('Error updating favorite status!');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error updating favorite status!');
        });
    });
});

// Button to toggle inactive turtles
const toggleInactiveButton = document.getElementById('toggle-inactive');
toggleInactiveButton.addEventListener('click', function() {
    document.querySelectorAll('.turtle-item.inactive').forEach(item => {
        item.classList.toggle('hidden');
    });

    const img = toggleInactiveButton.querySelector('img');
    if (toggleInactiveButton.classList.toggle('active')) {
        img.src = iconOnPath;
    } else {
        img.src = iconOffPath;
    }
});

// Button to toggle turtles with no description
const toggleNoDescriptionButton = document.getElementById('toggle-no-description');
toggleNoDescriptionButton.addEventListener('click', function() {
      document.querySelectorAll('.turtle-item.turtle-info.turtle-description.short-description').forEach(item => {
        item.classList.toggle('hidden');
    });

    const img = toggleNoDescriptionButton.querySelector('img');
    if (toggleNoDescriptionButton.classList.toggle('active')) {
         img.src = iconOnPath;
    } else {
        img.src = iconOffPath;
    }
});