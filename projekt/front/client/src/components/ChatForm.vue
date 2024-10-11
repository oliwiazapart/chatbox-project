<template>
    <div class="container mt-5">
      <div class="panel panel-default mx-auto" style="width: 67%; text-align: center;">
        <div>
          <img src="https://i.imgur.com/MyoOjNh.png" alt="Logo" width="80" class="mx-auto d-block">
        </div>
        <div class="panel-heading" style="font-size: 40px; font-family: 'Lato', sans-serif;">Fragrance advisor</div>
        <div class="panel-body">
            <br>
          <form @submit.prevent="sendMessage" class="mb-3">
            <div class="input-group">
              <input v-model="question" type="text" class="form-control" placeholder="Ask a question" required />
              <button type="submit" class="btn btn-primary">Send</button>
            </div>
          </form>
          <p v-if="loading" class="alert alert-info">Loading...</p>
          <p v-if="answer" class="alert alert-success">{{ answer }}</p>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        question: '',
        loading: false,
        answer: '',
      };
    },
    methods: {
      sendMessage() {
        if (this.question.trim() !== '') {
          this.loading = true;
          this.$socket.send(JSON.stringify({ question: this.question }));
        }
      },
    },
    mounted() {
      this.$options.sockets.onmessage = (event) => {
        const data = JSON.parse(event.data);
        this.answer = data.answer;
        this.loading = false;
      };
    },
  };
  </script>
  

  <style scoped>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300&display=swap');
    img {
      margin-top: 20px; 
    }

    .btn.btn-primary {
        background-color: #ffa343;
        border: none;
    }

    .btn-danger:primary {
        background-color: #ff8a10!important;
        border-color: #ff8a10!important;
        color: white; 
    }
  </style>
  