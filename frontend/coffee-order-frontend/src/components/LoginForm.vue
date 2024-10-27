<template>
  <div class="row no-gutters">
    <div class="col-md-6 d-flex align-items-center justify-content-center">
      <img src="/images/Mocha.jpg" alt="Mocha" class="img-fluid mocha-image" />
    </div>
    <div class="col-md-6 d-flex align-items-center justify-content-center">
      <div class="container">
        <h2 class="text-center mb-4">欢迎您使用在线咖啡订餐系统，请登录</h2>
        <form @submit.prevent="loginUser" class="login-form">
          <div class="mb-3">
            <label for="username" class="form-label">用户名</label>
            <input type="text" id="username" v-model="username" class="form-control" required />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">密码</label>
            <input type="password" id="password" v-model="password" class="form-control" required />
          </div>
          <div class="text-center">
            <button type="submit" class="btn btn-primary">登录</button>
            <router-link to="/register" class="btn btn-secondary ml-2">新用户注册</router-link>
          </div>
        </form>
        <p v-if="message" class="alert alert-info text-center mt-3">{{ message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'LoginForm',
  data() {
    return {
      username: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/login', {
          username: this.username,
          password: this.password
        });

        this.message = response.data.message;

        // 存储用户名和 JWT 到 localStorage
        localStorage.setItem('username', this.username);
        localStorage.setItem('token', response.data.token); // 存储 token

        // 根据用户角色跳转
        const role = response.data.role; // 从响应中获取用户角色
        if (role === 'admin') {
          this.$router.push('/admin'); // 管理员跳转到AdminPage.vue
        } else {
          this.$router.push('/menu'); // 普通用户跳转到CoffeeMenu.vue
        }

        // 清空表单
        this.username = '';
        this.password = '';
      } catch (error) {
        console.error("Login error:", error);
        this.message = error.response?.data?.error || "Login failed. Please try again.";
      }
    }
  }
};
</script>

<style scoped>
.mocha-image {
  height: 100vh; /* 设置图片高度为视口高度 */
  width: 100%; /* 设置图片宽度为100% */
  object-fit: cover; /* 保持图片比例，覆盖容器 */
}

.row {
  height: 100vh; /* 使整个行的高度为视口高度 */
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center; /* 使登录框在右侧垂直居中 */
  height: 100%; /* 使容器的高度占满父元素 */
  padding: 0 20px; /* 适当的内边距 */
}

.login-form {
  background: rgba(255, 255, 255, 0.9); /* 半透明背景 */
  padding: 30px;
  border-radius: 10px; /* 圆角 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* 立体效果 */
}

.form-control {
  border: 1px solid #ced4da;
  border-radius: 5px; /* 圆角 */
  transition: border-color 0.3s; /* 平滑过渡 */
}

.form-control:focus {
  border-color: #007bff; /* 聚焦时边框颜色 */
  box-shadow: 0 0 5px rgba(0, 123, 255, 0.5); /* 聚焦时阴影效果 */
}

.btn {
  border-radius: 5px; /* 圆角 */
  padding: 10px 20px; /* 按钮内边距 */
  font-weight: bold; /* 加粗 */
  transition: background-color 0.3s, transform 0.3s; /* 平滑过渡 */
}

.btn-primary {
  background-color: #007bff; /* 按钮背景色 */
  border: none; /* 去掉边框 */
}

.btn-primary:hover {
  background-color: #0056b3; /* 悬停时的背景色 */
  transform: translateY(-2px); /* 悬停时抬起效果 */
}

.btn-secondary {
  background-color: #6c757d; /* 次级按钮背景色 */
  border: none; /* 去掉边框 */
}

.btn-secondary:hover {
  background-color: #5a6268; /* 悬停时的背景色 */
  transform: translateY(-2px); /* 悬停时抬起效果 */
}

.alert {
  border-radius: 5px; /* 圆角 */
}
</style>
