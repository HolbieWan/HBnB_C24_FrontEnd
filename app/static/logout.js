// async function logout() {
//     try {
//         const response = await fetch('/api/v1/auth/logout', {
//             method: 'POST',
//             headers: {
//                 'Authorization': `Bearer ${getCookie('jwt_token')}`
//             }
//         });

//         if (response.ok) {
//             clearCookies();
//             window.location.href = "/HBnB/login";
//         } else {
//             console.error('Failed to log out');
//         }
//     } catch (error) {
//         console.error('Error logging out:', error);
//     }
// }

// document.getElementById('logout-button').addEventListener('click', logout);

// function clearCookies() {
//   document.cookie =
//     "jwt_token=; path=/; expires=0; secure; SameSite=Strict";
//   document.cookie =
//     "user_id=; path=/; expires=0; secure; SameSite=Strict";
// }

