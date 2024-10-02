document.addEventListener('DOMContentLoaded', async function() {
    const userId = localStorage.getItem('user_id'); // Fetch the user ID from local storage
    const postId = new URLSearchParams(window.location.search).get('post_id'); // Get post ID from the URL
    const postTitle = document.getElementById('post-title');
    const postContent = document.getElementById('post-content');
    const postImage = document.getElementById('post-image');
    const postTags = document.getElementById('post-tags');

    // Fetch the single blog post details
    try {
        const response = await fetch(`http://127.0.0.1:8000/blog-posts/detail/${userId}/${postId}/`);

        if (!response.ok) {
            throw new Error('Failed to fetch blog post');
        }

        const data = await response.json();

        // Populate the HTML with the blog post details
        postTitle.textContent = data.title;
        postContent.innerHTML = data.content; // Allow for rich text content
        
        // If the post has an image, display it
        if (data.image) {
            postImage.src = data.image;
            postImage.style.display = 'block'; // Show image only if it exists
        }

        // Display tags if available
        postTags.textContent = `Tags: ${data.tags || 'No tags available'}`;

    } catch (error) {
        console.error('Error fetching post:', error);
        alert('Error occurred while fetching the post details. Please try again.');
    }
});
