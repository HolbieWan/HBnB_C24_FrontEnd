document.addEventListener('DOMContentLoaded', function () {
    const reviewForm = document.getElementById('review-form');
    const placeId = new URLSearchParams(window.location.search).get('id');
    const reviewText = document.getElementById('review-text');
    const reviewRating = document.getElementById('review-rating');

    // Function to get a cookie by name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    reviewForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const token = getCookie('jwt_token');
        const userId = getCookie('user_id');  // Get the user_id from the cookie

        if (!token) {
            console.error('User is not logged in');
            window.location.href = '/login';
            return;
        }

        if (!userId) {
            console.error('User ID is missing');
            console.log('Current cookies:', document.cookie);  // Debug log
            return;
        }

        const reviewData = {
          user_id: userId, // Use the user_id from the cookie
          text: reviewText.value,
          rating: parseInt(reviewRating.value, 10),
          place_id: placeId,
        };

        console.log('Submitting review data:', reviewData);  // Debugging log
        console.log('JWT token:', token);  // Debugging log

        try {
            const response = await fetch(`/api/v1/reviews/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(reviewData)
            });

            console.log('Submit review response status:', response.status);  // Debugging log

            if (!response.ok) {
                const errorText = await response.text();
                console.error('Failed to submit review:', errorText);
                return;
            }

            const newReview = await response.json();
            console.log('Review submitted:', newReview);

            // Optionally, you can re-fetch reviews and update the review list
            fetchReviews();

            // Clear the form
            reviewText.value = '';
            reviewRating.value = '';

        } catch (error) {
            console.error('Error submitting review:', error);
        }
    });

    async function fetchReviews() {
        const token = getCookie('jwt_token');

        try {
            const response = await fetch(`/api/v1/reviews/places/${placeId}/reviews`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            console.log('Reviews response status:', response.status);  // Debugging log

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

    function renderReviews(reviews) {
        const reviewListSection = document.getElementById('review-list');
        reviewListSection.innerHTML = '';
        if (reviews.length === 0) {
            const noReviews = document.createElement('p');
            noReviews.textContent = 'No reviews available for this place.';
            reviewListSection.appendChild(noReviews);
        } else {
            reviews.forEach(review => {
                const reviewCard = document.createElement('div');
                reviewCard.classList.add('review-card');

                // const placeName = document.createElement('p');
                // reviewerName.innerHTML = `<strong>${review.place_name}</strong>`;

                const reviewerName = document.createElement("p");
                reviewerName.innerHTML = `<strong>${review.user_id}</strong>`;

                const reviewText = document.createElement('p');
                reviewText.textContent = review.text;

                const reviewRating = document.createElement('p');
                reviewRating.innerHTML = `<strong>Rating:</strong> ${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}`;
                
                // reviewCard.appendChild(placeName);
                reviewCard.appendChild(reviewerName);
                reviewCard.appendChild(reviewText);
                reviewCard.appendChild(reviewRating);

                reviewListSection.appendChild(reviewCard);
            });
        }
    }

    // Initial fetch to display current reviews
    fetchReviews();
});
