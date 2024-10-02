document.getElementById('blogPostForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const title = document.getElementById('title').value;
    const content = document.getElementById('content').value;
    const tags = document.getElementById('tags').value;
    const image = document.getElementById('image').files[0];

    const userId = localStorage.getItem('user_id'); // Get user ID from local storage
    const formData = new FormData();
    formData.append('title', title);
    formData.append('content', content);
    formData.append('tags', tags);
    if (image) {
        formData.append('image', image);
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/create-post/${userId}/`, {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('message').textContent = 'Blog post created successfully!';
            // Redirect to the blog list page after 2 seconds
            setTimeout(() => {
                window.location.href = '/blog_list/';
            }, 2000);
        } else {
            document.getElementById('message').textContent = data.error || 'Failed to create post';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('message').textContent = 'Error occurred. Please try again.';
    }
});
