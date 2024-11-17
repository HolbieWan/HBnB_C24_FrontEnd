document.addEventListener('DOMContentLoaded', function () {
    const placesList = document.getElementById('places-list');

    // Store places globally so they can be accessed by filter_by_country.js
    window.allPlaces = [];

    // Function to get a cookie by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Function to fetch places
    async function fetchPlaces() {

        try {
            const response = await fetch('/api/v1/places/', {
                method: 'GET'
            });

            if (!response.ok) {
                console.error('Failed to fetch places');
                return;
            }

            const places = await response.json();
            window.allPlaces = places; // Store the fetched places globally
            renderPlaces(places);

        } catch (error) {
            console.error('Error fetching places:', error);
            alert('User not logged in. Please go to loggin page.');
        }
    }

    // Function to render places
    function renderPlaces(places) {
        placesList.innerHTML = '';
        places.forEach(place => {
            const placeCard = document.createElement('div');
            placeCard.classList.add('place-card');

            const placeImage = document.createElement('img');
            placeImage.src = `../static/images/beach-house.jpeg`;
            placeImage.alt = place.name;
            placeImage.classList.add('place-image');

            const placeTitle = document.createElement('h3');
            placeTitle.textContent = place.title;

            const placePrice = document.createElement('p');
            placePrice.innerHTML = `<strong>Price per night:</strong> ${place.price} €`;

            const placeLocation = document.createElement('p');
            placeLocation.innerHTML = `<strong>Location:</strong> ${place.city_id}`;

            const detailsButton = document.createElement('button');
            detailsButton.textContent = 'View Details';
            detailsButton.classList.add('details-button');
            detailsButton.addEventListener('click', function() {
                window.location.href = `/HBnB/place?id=${place.id}`;
            });

            placeCard.appendChild(placeTitle);
            placeCard.appendChild(placeImage);
            placeCard.appendChild(placePrice);
            placeCard.appendChild(placeLocation);
            placeCard.appendChild(detailsButton);

            placesList.appendChild(placeCard);
        });
    }

    // Fetch places if the user is logged in
    fetchPlaces();

    // Expose the renderPlaces function globally
    window.renderPlaces = renderPlaces;
});
