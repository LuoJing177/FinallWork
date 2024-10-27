<template>
  <div class="order-container">
    <h1 class="title">我的订单</h1>
    <div v-if="orders.length === 0" class="no-orders">没有订单记录</div>
    <div v-else class="order-grid">
      <div v-for="order in orders" :key="order.id" class="order-card">
        <h2 class="order-id">订单 ID: {{ order.id }}</h2>
        <p class="order-total">总金额: <span class="total-amount">{{ order.total_amount }} 元</span></p>
        <p class="order-status">状态: <span class="status">{{ order.status }} <span v-if="order.status === '已完成'">☕️</span><span v-else-if="order.status === '待处理'">😊</span></span></p>
        <p class="order-date">创建时间: {{ new Date(order.created_at).toLocaleString() }}</p>
        <h3 class="items-title">订单商品:</h3>
        <ul class="items-list">
          <li v-for="item in order.items" :key="item.id" class="item">
            {{ item.name }} (数量: {{ item.quantity }}, 单价: <span class="item-price">{{ item.price }} 元</span>)
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      orders: []
    };
  },
  created() {
    this.fetchOrders();
  },
  methods: {
    async fetchOrders() {
      try {
        const token = localStorage.getItem('token'); // 获取 token
        const response = await axios.get('http://127.0.0.1:5000/api/orders', { // 确保 URL 正确
          headers: {
            Authorization: `Bearer ${token}` // 修复了这里的反引号
          }
        });
        this.orders = response.data; // 设置订单数据
      } catch (error) {
        console.error('获取订单失败:', error); // 错误处理
      }
    }
  }
};
</script>

<style scoped>
.order-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.no-orders {
  text-align: center;
  color: #999;
  font-size: 18px;
}

.order-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.order-card {
  background-color: #fff;
  border: 1px solid #e1e1e1;
  border-radius: 5px;
  padding: 15px;
  transition: box-shadow 0.3s;
  text-align: center; /* Center text within card */
}

.order-card:hover {
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.order-id {
  color: #007bff;
}

.order-total,
.order-status,
.order-date {
  margin: 5px 0;
}

.total-amount {
  font-weight: bold;
}

.status {
  color: #28a745; /* Green for status */
}

.items-title {
  margin-top: 10px;
  color: #555;
}

.items-list {
  list-style: none;
  padding: 0;
  margin: 10px 0 0 0;
}

.item {
  background-color: #f1f1f1;
  border-radius: 4px;
  padding: 10px;
  margin: 5px 0;
}

.item-price {
  font-weight: bold;
  color: #e74c3c; /* Red for item price */
}
</style>
