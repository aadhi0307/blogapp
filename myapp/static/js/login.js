document.getElementById('loginForm').addEventListener('submit', async function (e) {
    e.preventDefault(); // Prevent form submission

    const username = document.getElementById('username').value; // Get username/email
    const password = document.getElementById('password').value; // Get password

    try {
        const response = await fetch('http://127.0.0.1:8000/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        });

        // Log the response status for debugging
        console.log('Response status:', response.status);

        // Check if the response is not ok (HTTP status not in the range 200-299)
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Fetch error:', errorData);
            document.getElementById('message').textContent = errorData.error || 'Login failed';
            return; // Exit the function if there's an error
        }

        const data = await response.json(); // Parse the JSON response
        console.log('Response:', data); // Log the successful response

        // Store tokens and user ID in local storage
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('user_id', data.user.user_id);

        // Inform the user about the successful login
        document.getElementById('message').textContent = 'Login successful';
        // Optionally redirect to the create blog post page
        window.location.href = 'http://127.0.0.1:8000/blog_list/' ;
    } catch (error) {
        console.error('Error:', error); // Log any errors
        document.getElementById('message').textContent = 'Error occurred. Please check the console for more details.';
    }
});
