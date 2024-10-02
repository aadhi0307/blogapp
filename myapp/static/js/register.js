document.getElementById('registerForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const form = document.getElementById('registerForm');
    const formData = new FormData(form);

    try {
        const response = await fetch('http://127.0.0.1:8000/register/', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('message').textContent = 'Account created successfully';
            document.getElementById('message').classList.remove('text-red-500');
            document.getElementById('message').classList.add('text-green-500');
        } else {
            document.getElementById('message').textContent = data.message || 'Failed to create account';
        }
    } catch (error) {
        document.getElementById('message').textContent = 'Error occurred. Please try again.';
    }
});
