<template>
  <div class="admin-page">
    <aside class="sidebar">
      <h2 class="admin-info">管理员您好</h2>
      <p>用户名: <strong>{{ username }}</strong></p>
      <hr class="info-divider" />
      <p>角色: <strong>{{ role }}</strong></p>
      <hr class="divider" />
      <nav class="nav">
        <ul>
          <li><router-link to="/orders" class="nav-link">订单管理</router-link></li>
          <li><router-link to="/stock" class="nav-link">库存管理</router-link></li>
        </ul>
      </nav>
    </aside>
    <main class="content">
      <div class="welcome-section">
        <img src="\images\Cold Brew.jpg" alt="Cold Brew" class="welcome-image" />
        <h1 class="welcome-text">欢迎进入在线咖啡点餐系统后台</h1>
      </div>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: localStorage.getItem('username') || '管理员', // 动态获取的用户名
      role: 'admin' // 角色
    };
  }
};
</script>

<style scoped>
.admin-page {
  display: flex;
  height: 100vh; /* 设置页面高度为视口高度 */
  font-family: Arial, sans-serif;
}

.sidebar {
  width: 250px;
  background-color: #343a40; /* 深色背景 */
  color: #ffffff; /* 白色字体 */
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
  border-right: 1px solid #ccc; /* 添加右边框以分隔内容 */
  display: flex;
  flex-direction: column; /* 垂直布局 */
}

.admin-info {
  text-align: center;
  margin-bottom: 20px; /* 增加标题与内容之间的距离 */
}

.admin-info strong {
  font-size: 1.2em;
  color: #ffc107; /* 突出显示用户名和角色的颜色 */
}

.info-divider {
  border: none; /* 移除默认边框 */
  height: 1px;
  background-color: rgba(255, 255, 255, 0.5); /* 淡色分隔线 */
  margin: 15px 0; /* 增加分隔线上下间距 */
}

.divider {
  border: none; /* 移除默认边框 */
  height: 1px;
  background-color: rgba(255, 255, 255, 0.5); /* 淡色分隔线 */
  margin: 15px 0; /* 分隔线上下间距 */
}

.nav {
  margin-top: auto; /* 将导航推至底部 */
}

.nav ul {
  list-style: none;
  padding: 0;
}

.nav li {
  margin: 15px 0;
}

.nav-link {
  text-decoration: none;
  color: #ffc107; /* 链接的颜色 */
  padding: 10px 15px; /* 增加内边距 */
  border-radius: 5px; /* 圆角效果 */
  transition: background-color 0.3s; /* 平滑过渡效果 */
}

.nav-link:hover {
  background-color: #007bff; /* 悬停时改变背景颜色 */
  color: white; /* 悬停时改变字体颜色 */
}

.content {
  flex-grow: 1;
  padding: 20px;
  background-color: #ffffff; /* 内容区域的背景颜色 */
  border-radius: 5px; /* 内容区域的圆角 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex; /* 使用 flex 布局 */
  flex-direction: column; /* 垂直布局 */
  align-items: center; /* 居中对齐内容 */
}

.welcome-section {
  position: relative; /* 为绝对定位的子元素提供相对定位的上下文 */
  text-align: center; /* 文字居中 */
  margin-bottom: 20px; /* 下方间距 */
}

.welcome-image {
  max-width: 100%; /* 图片最大宽度 */
  max-height: 600px; /* 限制图片高度 */
  height: auto; /* 高度自适应 */
  border-radius: 10px; /* 圆角效果 */
  opacity: 0.7; /* 设置透明度 */
}

.welcome-text {
  position: absolute; /* 绝对定位 */
  top: 10%; /* 位置调整 */
  left: 50%; /* 居中对齐 */
  transform: translateX(-50%); /* 水平居中 */
  color: #ffffff; /* 白色文字 */
  font-size: 3em; /* 字体大小 */
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7); /* 添加文字阴影 */
}
</style>
