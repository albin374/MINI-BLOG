document.addEventListener('DOMContentLoaded', function () {
    const likeButtons = document.querySelectorAll('.like-btn');
    const dislikeButtons = document.querySelectorAll('.dislike-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.dataset.id;
            fetch(`/like/${postId}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById(`like-count-${postId}`).innerText = data.likes;
                    document.getElementById(`dislike-count-${postId}`).innerText = data.dislikes;
                });
        });
    });

    dislikeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = this.dataset.id;
            fetch(`/dislike/${postId}/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById(`like-count-${postId}`).innerText = data.likes;
                    document.getElementById(`dislike-count-${postId}`).innerText = data.dislikes;
                });
        });
    });
});
