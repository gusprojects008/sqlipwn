// frontend validatioan!
const username = document.getElementById("username");
const userComment = document.getElementById("user-comment");
//let username = document.getElementById("username");
//let userComment = document.getElementById("user-comment");
const sendData = document.getElementById("send-data");
const serverResponse = document.getElementById("server-response");
const usersComments = document.getElementById("users-comments");
const csrftoken = getCookie('csrftoken');

function getCookie(name) {
  return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=')[1];
}

function UserCommentAdd(username, comment, element) {
  username = basicSanitation(username);
  comment = basicSanitation(comment);
  const commentEl = document.createElement("p");
  commentEl.textContent = `${username} ${comment}`;
  element.appendChild(commentEl);
}

function basicSanitation(string) {
  return string
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

sendData.addEventListener("click", async (event) => {
  event.preventDefault(); // Prevents form reloading
  const usernameValue = basicSanitation(username.value.trim());
  const userCommentValue = basicSanitation(userComment.value.trim());
  console.log(usernameValue, userCommentValue);

  if (!usernameValue || usernameValue.length > 32) {
     alert("Insira um username de até 32 caracteres! (Enter a username of up 32 characters!)");
     return; // Stops function execution after executing "alert()"
     };
  if (!userCommentValue || userCommentValue.length > 32) {
     alert("Por favor, insira um comentário de até 32 caracteres! a(Please enter a comment of up to 32 charecters!)");
     return;
     };

  const userDataValues = new URLSearchParams();
  userDataValues.append("username", usernameValue);
  userDataValues.append("comment", userCommentValue);

  try {
      const response = await fetch("/sqlipwn/scripts/api/add_comment", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/x-www-form-urlencoded"
        },
        body: userDataValues.toString()
      });

    const APIresponse = await response.json();

    if (response.ok && APIresponse.status === "success") {
       serverResponse.textContent = APIresponse.message;
       UserCommentAdd(APIresponse.username, APIresponse.comment, usersComments);
    } else {
      serverResponse.textContent = APIresponse.message;
    }

  } catch (error) {
    serverResponse.textContent = "Error! server connect failed or username already exists );";
    console.log(error);
    };
});

async function loadComments() {
  try {
    const response = await fetch("/sqlipwn/scripts/api/list_comments")
    const data = await response.json();
    if (data.status !== "success") {
       console.log(response, data);
       return
    }
    usersComments.innerHTML = "";
    data.message.forEach(comment_username => {
      UserCommentAdd(comment_username.username, comment_username.comment, usersComments);
    });
  } catch (error) {
    console.log(error);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  loadComments()
  setInterval(loadComments, 2000)
})
