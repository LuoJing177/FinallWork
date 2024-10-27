<template>
  <div>
    <!-- 导航栏 -->
    <nav class="navbar navbar-light bg-light">
      <div class="container-fluid d-flex justify-content-between align-items-center">
        <span class="navbar-brand">{{ userInfo.username }}已登录</span> <!-- 显示当前登录用户的用户名 -->
        <div class="d-flex">
          <router-link to="/cart" class="btn btn-outline-success me-2">购物车</router-link>
          <router-link to="/my-orders" class="btn btn-outline-info me-2">我的订单</router-link>
          <!-- 订单查询部分 -->
          <select v-model="selectedOrder" class="form-select me-2" style="width: 150px;" aria-label="选择订单">
            <option value="" disabled>选择订单号</option> <!-- 默认提示 -->
            <option v-for="order in orders" :key="order.id" :value="order.id">
              {{ order.id }} <!-- 循环显示用户的订单号 -->
            </option>
          </select>
          <button class="btn btn-outline-primary" @click="checkOrderStatus">查询订单状态</button>
        </div>
      </div>
    </nav>

    <!-- 消息提示框 -->
    <div class="alert-container" v-if="message">
      <p class="alert alert-info text-center">{{ message }}</p> <!-- 显示消息内容 -->
    </div>

    <div class="container mt-5">
      <h1 class="text-center mb-4">Coffee Menu——在线咖啡点餐</h1>
      <div class="row">
        <div class="col-md-4" v-for="item in menu" :key="item.id">
          <div class="card mb-4 shadow-sm">
            <img :src="`/images/${item.image}`" alt="Coffee Item" class="card-img-top img-fluid" style="height: 200px; object-fit: cover;">
            <div class="card-body">
              <h5 class="card-title">{{ item.name }}</h5> <!-- 显示商品名称 -->
              <p class="card-text">{{ item.description }}</p> <!-- 显示商品描述 -->
              <span class="badge bg-primary">{{ formatPrice(item.price) }}</span> <!-- 显示商品价格 -->
              <button class="btn btn-success mt-2" @click="addToCart(item.id)">加入购物车</button> <!-- 加入购物车按钮 -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      menu: [], // 商品菜单
      message: "", // 消息提示内容
      userInfo: {}, // 用户信息
      selectedOrder: null, // 当前选择的订单号
      orders: [] // 用户的订单列表
    };
  },
  methods: {
    // 获取商品菜单
    async fetchMenu() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/menu');
        console.log("Menu data fetched:", response.data);
        this.menu = response.data.menu; // 将返回的商品菜单数据赋值
      } catch (error) {
        console.error("Error fetching menu:", error);
      }
    },

    // 获取用户信息
    async fetchUserInfo() {
      const username = localStorage.getItem('username'); // 从 localStorage 获取用户名
      if (username) {
        this.userInfo.username = username; // 设置用户名
      } else {
        console.error("No username found in localStorage.");
        this.userInfo.username = "Guest"; // 默认用户名
      }
    },

    // 获取用户的订单列表
    async fetchOrders() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/orders', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}` // 使用 token 进行身份验证
          }
        });
        console.log("Orders fetched:", response.data);
        this.orders = response.data; // 将返回的订单数据赋值
      } catch (error) {
        console.error("Error fetching orders:", error);
      }
    },

    // 查询订单状态
    async checkOrderStatus() {
      if (!this.selectedOrder) {
        alert("请先选择一个订单号"); // 如果未选择订单号，则提示
        return;
      }

      try {
        const response = await axios.get(`http://127.0.0.1:5000/api/orders/${this.selectedOrder}/status`, {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}` // 使用 token 进行身份验证
          }
        });
        alert(`订单状态: ${response.data.status}`); // 显示订单状态
      } catch (error) {
        console.error("Error fetching order status:", error);
      }
    },

    // 将商品添加到购物车
    async addToCart(itemId) {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.post('http://127.0.0.1:5000/api/cart/add', { item_id: itemId }, {
          headers: {
            'Authorization': `Bearer ${token}`
          },
          withCredentials: true
        });

        console.log("Item added to cart:", response.data.message);
        this.message = `${response.data.message} - 已加入购物车`; // 显示成功消息
        setTimeout(() => {
          this.message = "";  // 3秒后清空消息
        }, 3000);
      } catch (error) {
        console.error("Error adding item to cart:", error);
        this.message = "商品已加入购物车，无需重复添加"; // 显示失败消息
        setTimeout(() => {
          this.message = "";  // 3秒后清空消息
        }, 3000);
      }
    },

    // 格式化价格
    formatPrice(value) {
      return value ? value.toFixed(2) : 'N/A'; // 显示两位小数
    }
  },
  mounted() {
    this.fetchMenu(); // 组件挂载时获取商品菜单
    this.fetchUserInfo(); // 获取用户信息
    this.fetchOrders(); // 获取用户订单
  }
};
</script>

<style scoped>
.card {
  transition: transform 0.2s;
}

.card:hover {
  transform: scale(1.05); /* 鼠标悬停时放大效果 */
}

.card-title {
  font-weight: bold; /* 商品名称加粗 */
}

.card-text {
  color: #555; /* 商品描述字体颜色 */
}

/* 消息提示框样式 */
.alert-container {
  position: absolute; /* 绝对定位 */
  top: 70px; /* 根据导航栏的高度调整 */
  left: 20px; /* 距离左侧20px */
  z-index: 1000; /* 确保在最上层 */
  width: auto; /* 根据需要调整宽度 */
}

.alert {
  margin: 0; /* 去掉默认的外边距 */
}
</style>
