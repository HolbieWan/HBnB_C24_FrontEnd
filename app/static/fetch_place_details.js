document.addEventListener('DOMContentLoaded', function () {
    const placeDetailsSection = document.getElementById('place-details');
    const reviewListSection = document.getElementById('review-list');
    const addReviewSection = document.getElementById('add-review');

    // Function to get a cookie by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Function to get query parameter by name
    function getQueryParam(name) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    // Function to fetch place details
    async function fetchPlaceDetails() {
        const token = getCookie('jwt_token');
        const placeId = getQueryParam('id');

        if (!placeId) {
            console.error('Place ID is missing in the URL');
            return;
        }

        try {
            const response = await fetch(`/api/v1/places/${placeId}`, {
                method: 'GET',
                headers: token ? { 'Authorization': `Bearer ${token}` } : {}
            });

            console.log('Place details response status:', response.status);  // Debug log

            if (!response.ok) {
                console.error('Failed to fetch place details');
                return;
            }

            const placeDetails = await response.json();
            console.log('Place details:', placeDetails);  // Log the place details data
            renderPlaceDetails(placeDetails);

        } catch (error) {
            console.error('Error fetching place details:', error);
        }
    }

    // Function to render place details
    function renderPlaceDetails(place) {
        placeDetailsSection.innerHTML = '';

        const placeCard = document.createElement('div');
        placeCard.classList.add('place-details-card');

        const placeImage = document.createElement('img');
        placeImage.src = place.image_url || `/static/images/beach-house.jpeg`; // Change this to place.image_url if available
        placeImage.alt = place.title;
        placeImage.classList.add('place-image-large');

        const placeTitle = document.createElement('h2');
        placeTitle.textContent = place.title;

        const placePrice = document.createElement('p');
        placePrice.innerHTML = `<strong>Price per night:</strong> ${place.price} €`;

        const placeLocation = document.createElement('p');
        placeLocation.innerHTML = `<strong>Location:</strong> ${place.city_id}, ${place.country_name}`;

        const placeDescription = document.createElement('p');
        placeDescription.innerHTML = `<strong>Description:</strong> ${place.description}`;

        const placeOwner = document.createElement('p');
        placeOwner.innerHTML = `<strong>Owner:</strong> ${place.owner_id}`;

        placeCard.appendChild(placeTitle);
        placeCard.appendChild(placeImage);
        placeCard.appendChild(placePrice);
        placeCard.appendChild(placeLocation);
        placeCard.appendChild(placeDescription);
        placeCard.appendChild(placeOwner);

        placeDetailsSection.appendChild(placeCard);
    }

    // Function to render reviews
    function renderReviews(reviews) {
        reviewListSection.innerHTML = '';
        if (reviews.length === 0) {
            const noReviews = document.createElement('p');
            noReviews.textContent = 'No reviews available for this place.';
            reviewListSection.appendChild(noReviews);
        } else {
            reviews.forEach(review => {
                const reviewCard = document.createElement('div');
                reviewCard.classList.add('review-card');

                const reviewerName = document.createElement('p');
                reviewerName.innerHTML = `<strong>${review.place_name}</strong>`;

                const reviewText = document.createElement('p');
                reviewText.textContent = review.text;

                const reviewRating = document.createElement('p');
                reviewRating.innerHTML = `<strong>Rating:</strong> ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}`;

                reviewCard.appendChild(reviewerName);
                reviewCard.appendChild(reviewText);
                reviewCard.appendChild(reviewRating);

                reviewListSection.appendChild(reviewCard);
            });
        }
    }

    // Function to fetch reviews
    async function fetchReviews() {
        const token = getCookie('jwt_token');
        const placeId = getQueryParam('id');

        if (!placeId) {
            console.error('Place ID is missing in the URL');
            return;
        }

        try {
            const response = await fetch(`/api/v1/reviews/places/${placeId}/reviews`, {
                method: 'GET',
                headers: token ? { 'Authorization': `Bearer ${token}` } : {}
            });

            console.log('Reviews response status:', response.status);  // Debug log

            if (!response.ok) {
                console.error('Failed to fetch reviews');
                return;
            }

            const reviews = await response.json();
            console.log('Reviews:', reviews);  // Log the reviews data
            renderReviews(reviews);

        } catch (error) {
            console.error('Error fetching reviews:', error);
        }
    }

    // Check if the user is authenticated and show the review form if true
    function checkAuthentication() {
        const token = getCookie('jwt_token');
        if (token) {
            addReviewSection.style.display = 'block';
        } else {
            addReviewSection.style.display = 'none';
        }
    }

    // Fetch place details and reviews if the user is logged in
    fetchPlaceDetails();
    fetchReviews();
    checkAuthentication();
});
