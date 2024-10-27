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
      <div class="order-management">
        <h2>所有订单</h2>
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>订单ID</th>
                <th>总金额</th>
                <th>状态</th>
                <th>创建时间</th>
                <th>商品详情</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.id">
                <td>{{ order.id }}</td>
                <td>{{ order.total_amount }}</td>
                <td>{{ order.status }}</td>
                <td>{{ new Date(order.created_at).toLocaleString() }}</td>
                <td>
                  <ul>
                    <li v-for="item in order.items" :key="item.id">
                      {{ item.name }} (数量: {{ item.quantity }})
                    </li>
                  </ul>
                </td>
                <td>
                  <button
                    v-if="order.status === '制作中'"
                    class="complete-button"
                    @click="completeOrder(order.id)">
                    标记为已完成
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: localStorage.getItem('username') || '管理员',
      role: 'admin',
      orders: [] // 存储所有订单的数组
    };
  },
  created() {
    this.fetchOrders(); // 在组件创建时获取所有订单
  },
  methods: {
    async fetchOrders() {
      try {
        const token = localStorage.getItem('token'); // 获取 token
        const response = await axios.get('http://127.0.0.1:5000/api/ordersadmin', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.orders = response.data; // 将获取到的订单数据赋值给 orders
      } catch (error) {
        console.error('获取订单失败:', error);
      }
    },
    async completeOrder(orderId) {
      try {
        await axios.put(`http://127.0.0.1:5000/api/ordersadmin/${orderId}/complete`, {}, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}` // 使用JWT
          }
        });
        await this.fetchOrders();
      } catch (error) {
        console.error('更新订单状态失败:', error);
      }
    }
  }
};
</script>

<style scoped>
.admin-page {
  display: flex;
  height: 100vh;
  font-family: Arial, sans-serif;
}

.sidebar {
  width: 250px;
  background-color: #343a40;
  color: #ffffff;
  padding: 20px;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.2);
  border-right: 1px solid #ccc;
  display: flex;
  flex-direction: column;
}

.admin-info {
  text-align: center;
  margin-bottom: 20px;
}

.admin-info strong {
  font-size: 1.2em;
  color: #ffc107;
}

.info-divider,
.divider {
  border: none;
  height: 1px;
  background-color: rgba(255, 255, 255, 0.5);
  margin: 15px 0;
}

.nav {
  margin-top: auto;
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
  color: #ffc107;
  padding: 10px 15px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

.nav-link:hover {
  background-color: #007bff;
  color: white;
}

.content {
  flex-grow: 1;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center; /* 使内容居中 */
}

.order-management {
  width: 100%; /* 占满宽度 */
  max-width: 1200px; /* 设置最大宽度 */
  padding: 20px;
}

.table-container {
  width: 100%;
  overflow-x: auto; /* 允许水平滚动 */
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ccc;
  padding: 10px;
  text-align: left;
}

th {
  background-color: #f4f4f4;
  position: sticky;
  top: 0; /* 使表头固定 */
  z-index: 1; /* 保证表头在前 */
}

.complete-button {
  background-color: #28a745; /* 绿色背景 */
  color: white; /* 白色字体 */
  border: none; /* 无边框 */
  padding: 8px 12px; /* 内边距 */
  border-radius: 5px; /* 圆角效果 */
  cursor: pointer; /* 鼠标样式 */
  transition: background-color 0.3s;
}

.complete-button:hover {
  background-color: #218838; /* 悬停时颜色变化 */
}

.order-divider {
  border: none;
  height: 1px;
  background-color: rgba(0, 0, 0, 0.1);
  margin: 10px 0; /* 增加上下间距 */
}
</style>
