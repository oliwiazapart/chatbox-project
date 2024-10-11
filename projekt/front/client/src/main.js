import { createApp } from 'vue';
import App from './App.vue';
import VueNativeSock from 'vue-native-websocket-vue3';
import 'bootstrap/dist/css/bootstrap.min.css';

const app = createApp(App);

app.use(VueNativeSock, 'ws://127.0.0.1:8000/ws', {
  format: 'json',
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 3000,
});

app.mount('#app');
