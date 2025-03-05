// 新しい投稿を送信する
async function submitPost() {
  const text = document.getElementById("postText").value;
  if (!text.trim()) return; // 空投稿を防ぐ
  await fetch("/posts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  document.getElementById("postText").value = ""; // 投稿後に入力欄をクリア
  loadPosts(); // 投稿後に一覧を更新
}

// 投稿一覧を取得して表示
async function loadPosts() {
  const response = await fetch("/posts");
  const posts = await response.json();
  const postsDiv = document.getElementById("postlist");
  postsDiv.innerHTML = "";
  posts.forEach((post) => {
    postsDiv.innerHTML += `
        <p>
          ${post.text}
          <button onclick="likePost(${post.id})">♡</button> ${post.likes} いいね
          <button onclick="loadReplies(${post.id})">回答を見る</button>
        </p>
      `;
  });
}

// いいね機能
async function likePost(postId) {
  await fetch(`/posts/${postId}/like`, { method: "POST" });
  loadPosts(); // 更新
}

// 大喜利回答を取得して表示
async function loadReplies(postId) {
  const response = await fetch(`/replies/${postId}`);
  const replies = await response.json();
  const repliesDiv = document.getElementById("replies");
  repliesDiv.innerHTML = "";
  replies.forEach((reply) => {
    repliesDiv.innerHTML += `
        <p>${reply.text} <button onclick="voteReply(${reply.id})">投票</button></p>
      `;
  });
}

// 回答に投票
async function voteReply(replyId) {
  await fetch(`/replies/${replyId}/vote`, { method: "POST" });
  loadReplies(); // 更新
}

// フォーム送信時の処理
document.addEventListener("DOMContentLoaded", () => {
  document
    .getElementById("postForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      submitPost();
    });

  loadPosts(); // 初期ロード
});
