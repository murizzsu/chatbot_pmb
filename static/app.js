class Chatbox {
    constructor() {
      this.args = {
        openButton: document.querySelector(".chatbox__button"),
        chatBox: document.querySelector(".chatbox__support"),
        sendButton: document.querySelector(".send__button"),
      };
  
      this.state = false;
      this.messages = [];
      this.tutorialButton = document.createElement("button");
      this.tutorialButton.classList.add("tutorial-button"); // Add the "tutorial-button" class
  
    }
  
    display() {
      const { openButton, chatBox, sendButton } = this.args;
  
      openButton.addEventListener("click", () => this.toggleState(chatBox));
  
      sendButton.addEventListener("click", () => this.onSendButton(chatBox));
  
      const node = chatBox.querySelector("input");
      node.addEventListener("keyup", ({ key }) => {
        if (key === "Enter") {
          this.onSendButton(chatBox);
        }
      });
    }

    showTutorial() {
      const chatBox = this.args.chatBox;
      const chatmessage = chatBox.querySelector(".chatbox__messages");
      chatmessage.innerHTML = "Tutorial penggunaan chatbot: <br> 1. Ketik pesan atau pertanyaan anda di kotak input.<br>2. Tekan Enter atau klik tombol Kirim untuk mengirim pesan dan tunggu beberapa saat.<br>3. Chatbot akan merespons dengan jawaban atau informasi yang relevan.<br><br>Selamat menggunakan chatbot!";
    }
  
    
    toggleState(chatbox) {
      this.state = !this.state;
    
      // show or hides the box
      if (this.state) {
        chatbox.classList.add("chatbox--active");
        this.tutorialButton.style.display = "block"; // Menampilkan tutorial-button
        this.tutorialButton.innerText = "Tutorial Penggunaan"; // Tambahkan teks ke dalam tombol
        const chatMessages = chatbox.querySelector(".chatbox__messages");
        chatMessages.appendChild(this.tutorialButton); // Tambahkan tombol ke dalam chatbox__messages
        this.tutorialButton.addEventListener("click", this.showTutorial.bind(this));
      } else {
        chatbox.classList.remove("chatbox--active");
        this.tutorialButton.style.display = "none"; // Menyembunyikan tutorial-button
    
        // Hapus inner HTML dari tutorial jika chatbot tidak aktif
        const chatMessages = chatbox.querySelector(".chatbox__messages");
        chatMessages.innerHTML = "";
      }
    }
    
  
    onSendButton(chatbox) {
      var textField = chatbox.querySelector("input");
      let text1 = textField.value;
      if (text1 === "") {
        return;
      }
  
      let msg1 = { name: "User", message: text1 };
      this.messages.push(msg1);
  
      fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: JSON.stringify({ message: text1 }),
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((r) => r.json())
        .then((r) => {
          let msg2 = { name: "Ki", message: r.answer };
          this.messages.push(msg2);
          this.updateChatText(chatbox);
          textField.value = "";
        })
        .catch((error) => {
          console.error("Error:", error);
          this.updateChatText(chatbox);
          textField.value = "";
        });
    }
  
    updateChatText(chatbox) {
      var html = "";
      this.messages
        .slice()
        .reverse()
        .forEach(function (item, index) {
          if (item.name === "Ki") {
            html +=
              '<div class="messages__item messages__item--visitor">' +
              item.message +
              "</div>";
          } else {
            html +=
              '<div class="messages__item messages__item--operator">' +
              item.message +
              "</div>";
          }
        });
  
      const chatmessage = chatbox.querySelector(".chatbox__messages");
      chatmessage.innerHTML = html;
    }
  }
  
  const chatbox = new Chatbox();
  chatbox.display();