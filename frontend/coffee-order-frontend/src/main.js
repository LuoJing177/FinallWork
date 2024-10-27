import { createApp } from 'vue';
import App from './App.vue';
import 'bootstrap/dist/css/bootstrap.min.css';
import router from './router'; // 导入 router
import 'bootstrap';


// 创建 Vue 应用并使用 router
createApp(App)
  .use(router) // 注册路由
  .mount('#app');
