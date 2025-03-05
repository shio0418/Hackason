// // フォームの送信イベント
// document
//   .getElementById("postForm")
//   .addEventListener("submit", function (event) {
//     event.preventDefault(); // フォームのデフォルトの送信を防ぐ

//     // ユーザーが入力したテキスト
//     const text = document.getElementById("postText").value;

//     // リクエストデータを作成
//     const data = { text: text };

//     // fetchを使ってサーバーにPOSTリクエストを送信
//     fetch("http://127.0.0.1:5000/posts", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ text: "投稿内容" }), // JSON形式で送信
//     })
//       .then((response) => response.json())
//       .then((data) => {
//         if (data.message === "Post created successfully") {
//           alert("投稿が成功しました！");
//           // 新しい投稿を表示するために画面を更新
//           loadPosts();
//         } else {
//           alert("投稿に失敗しました");
//         }
//       })
//       .catch((error) => {
//         console.error("エラー:", error);
//       });
//   });

// // 投稿を取得する関数
// function loadPosts() {
//   fetch("http://127.0.0.1:5000/posts")
//     .then((response) => response.json())
//     .then((posts) => {
//       const postList = document.getElementById("postList");
//       postList.innerHTML = ""; // 既存の投稿をリセット
//       posts.forEach((post) => {
//         const postElement = document.createElement("div");
//         postElement.innerHTML = `
//                     <p>${post.text}</p>
//                     <button onclick="likePost(${post.id})">いいね</button>
//                     <span>いいね数: ${post.likes}</span>
//                 `;
//         postList.appendChild(postElement);
//       });
//     })
//     .catch((error) => console.error("エラー:", error));
// }
// // いいねを送信する関数
// function likePost(postId) {
//   fetch(`http://127.0.0.1:5000/posts/${postId}/like`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       if (data.message === "Post liked successfully") {
//         alert("いいねしました！");
//         // 画面を更新
//         loadPosts();
//       } else {
//         alert("いいねに失敗しました");
//       }
//     })
//     .catch((error) => console.error("エラー:", error));
// }
// // 初期に投稿を読み込む
// loadPosts();

// // いいねを送信する関数
// function likePost(postId) {
//   fetch(`http://127.0.0.1:5000/posts/${postId}/like`, {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json",
//     },
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       if (data.message === "Post liked successfully") {
//         alert("いいねしました！");
//         // 画面を更新
//         loadPosts();
//       } else {
//         alert("いいねに失敗しました");
//       }
//     })
//     .catch((error) => console.error("エラー:", error));
// }
