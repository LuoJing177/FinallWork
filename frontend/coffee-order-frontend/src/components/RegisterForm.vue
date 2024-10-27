<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-md-6">
        <img src="/images/Macchiato.jpg" alt="Macchiato" class="mocha-image" />
      </div>
      <div class="col-md-6 d-flex justify-content-center align-items-center">
        <div class="container">
          <h2 class="text-center mb-4">新用户请注册</h2>
          <form @submit.prevent="registerUser" class="register-form">
            <div class="mb-3">
              <label for="username" class="form-label">用户名</label>
              <input type="text" id="username" v-model="username" class="form-control" required />
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">邮箱</label>
              <input type="email" id="email" v-model="email" class="form-control" required />
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">密码</label>
              <input type="password" id="password" v-model="password" class="form-control" required />
            </div>
            <button type="submit" class="btn btn-primary">注册</button>
          </form>
          <p v-if="message" class="alert alert-info text-center mt-3">{{ message }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterForm',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/register', {
          username: this.username,
          email: this.email,
          password: this.password
        });
        this.message = response.data.message;
        this.username = '';
        this.email = '';
        this.password = '';

        // 注册成功后跳转到登录页面
        console.log('Response received:', response.data);
        if (response.data.success) {
          this.$router.push('/login');
        }
      } catch (error) {
        console.error("Registration error:", error);
        this.message = error.response?.data?.error || "Registration failed. Please try again.";
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
  justify-content: center; /* 使注册框在右侧垂直居中 */
  height: 100%; /* 使容器的高度占满父元素 */
  padding: 0 20px; /* 适当的内边距 */
}

.register-form {
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

.alert {
  border-radius: 5px; /* 圆角 */
}
</style>
