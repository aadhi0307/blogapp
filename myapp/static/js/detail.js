// main.js

document.addEventListener("DOMContentLoaded", function () {
    // Fetch the blog post when the page is loaded
    const userId = 1;  // Replace with dynamic value if needed
    const postId = 1;  // Replace with dynamic value if needed
    fetchBlogPostDetails(userId, postId);
});

function fetchBlogPostDetails(userId, postId) {
    const url = `/blog-posts/detail/${userId}/${postId}/`;

    fetch(url)
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Error fetching post: ${response.statusText}`);
            }
            return response.json();
        })
        .then((data) => {
            displayBlogPost(data);
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('Unable to fetch blog post details.');
        });
}

function displayBlogPost(data) {
    const postContainer = document.getElementById("post-container");

    if (postContainer) {
        // Assuming `data` has title and content fields
        postContainer.innerHTML = `
            <h1>${data.title}</h1>
            <p>${data.content}</p>
        `;
    }
}
