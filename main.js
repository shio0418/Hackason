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

function replaceUnsupportedCharacters(element) {
  const text = element.innerText;
  const supportedText = text.replace(
    /[\u4e00-\u9faf\u3400-\u4DBF\u20000-\u2A6DF\u2A700-\u2B73F\u2B740-\u2B81F]/g,
    "?"
  );
  element.innerText = supportedText;
}

// 初期処理で文字列を置き換える
document.addEventListener("DOMContentLoaded", () => {
  // 投稿がロードされた後に漢字を?に置き換える
  loadPosts();
});

// 投稿一覧を取得して表示
async function loadPosts() {
  const response = await fetch("/posts");
  const posts = await response.json();
  const postsDiv = document.getElementById("postlist");
  postsDiv.innerHTML = "";

  posts.forEach((post) => {
    const postElement = document.createElement("div");
    postElement.classList.add("post_list");
    postElement.id = `post-${post.id}`;

    // 投稿内容を追加
    postElement.innerHTML = `
      <p class="post_date">${post.created_at}</p>
      <p class="post-text">${post.text}</p>
      <div class="actions">
        <button class="like-btn" onclick="likePost(${post.id})">
          <span class="material-symbols-outlined like_heart">favorite</span>
        </button>
        <span class="like-count">${post.likes} いいね</span>
        <button class="reply-btn" onclick="toggleReplyForm(${post.id})">
          <span class="material-symbols-outlined">reply</span>
        </button>
        <button class="reply-btn" onclick="loadReplies(${post.id})">リプライを見る</button>
      </div>
      <div id="replyForm-${post.id}" class="reply-form" style="display: none;">
        <textarea id="replyText-${post.id}" placeholder="リプライを入力"></textarea>
        <button onclick="submitReply(${post.id})">
          <span class="material-symbols-outlined">send</span>
        </button>
      </div>
      <div id="replies-${post.id}" class="replies-container" style="display: none;"></div> <!-- リプライ表示用のdiv -->
    `;

    // 投稿テキストを?に置き換える
    replaceUnsupportedCharacters(postElement.querySelector(".post-text"));

    // 投稿を画面に追加
    postsDiv.appendChild(postElement);
  });
}

// その他の関数（いいね、リプライ表示など）は省略していますが、そのままで動作します

// いいね機能
async function likePost(postId) {
  await fetch(`/posts/${postId}/like`, { method: "POST" });
  loadPosts(); // 更新
}

// 回答を取得して表示
async function loadReplies(postId) {
  const repliesDiv = document.getElementById(`replies-${postId}`); // 投稿に対応したリプライ表示用のdivを取得
  const isVisible = repliesDiv.style.display === "block"; // 現在の表示状態を取得

  if (isVisible) {
    // すでに表示されている場合は非表示にする
    repliesDiv.style.display = "none";
    return;
  }

  // リプライが表示されていない場合、リプライを取得して表示
  const response = await fetch(`/replies/${postId}`);
  const replies = await response.json();
  repliesDiv.innerHTML = ""; // 既存のリプライをクリア

  if (replies.length === 0) {
    repliesDiv.innerHTML = "<p>まだリプライはありません。</p>";
  } else {
    // リプライがある場合
    replies.forEach((reply) => {
      repliesDiv.innerHTML += `
        <div class="reply">
          <p>${reply.text}</p>
          <a href="#post-${postId}" class="post-link">この投稿に戻る</a>
          <button onclick="voteReply(${reply.id})">
            <span class="material-symbols-outlined">How_To_Vote</span> 投票
          </button>
        </div>
      `;
    });
  }

  // リプライを表示
  repliesDiv.style.display = "block";
}
// すべてのリプライを取得して表示
async function loadAllReplies(sortOrder) {
  const response = await fetch("/replies"); // 全てのリプライを取得
  const replies = await response.json();

  // 並べ替え（新しい順または投票数順）
  if (sortOrder === "most-voted") {
    replies.sort((a, b) => b.votes - a.votes); // 投票数が多い順
  } else if (sortOrder === "newest") {
    replies.sort((a, b) => new Date(b.created_at) - new Date(a.created_at)); // 新しい順
  }

  const repliesDiv = document.getElementById("replies");
  repliesDiv.innerHTML = ""; // 既存のリプライをクリア

  if (replies.length === 0) {
    repliesDiv.innerHTML = "<p>まだリプライはありません。</p>";
  } else {
    replies.forEach((reply) => {
      repliesDiv.innerHTML += `
        <div class="reply">
          <p>${reply.text}</p>
          <p>投票数: ${reply.votes}</p>
          <p><small>投稿日時: ${reply.created_at}</small></p>
          <button onclick="voteReply(${reply.id})">
            <span class="material-symbols-outlined">How_To_Vote</span>
          </button>
        </div>
      `;
    });
  }
}

// 回答に投票
async function voteReply(replyId) {
  await fetch(`/replies/${replyId}/vote`, { method: "POST" });
  loadReplies("newest"); // 更新後、表示を最新順でリロード
}

// リプライ送信
async function submitReply(postId) {
  const text = document.getElementById(`replyText-${postId}`).value;
  if (!text.trim()) return;

  // リプライを送信
  await fetch("/replies", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ post_id: postId, text }),
  });

  document.getElementById(`replyText-${postId}`).value = ""; // 送信後にテキストエリアをクリア
  loadReplies(postId); // リプライを再読み込み
}
// リプライフォームを開閉
function toggleReplyForm(postId) {
  const form = document.getElementById(`replyForm-${postId}`);
  form.style.display = form.style.display === "none" ? "block" : "none";
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
