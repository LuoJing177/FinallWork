<template>
  <div class="shopping-cart">
    <h1 class="title">购物车</h1>
    <div v-if="cartItems.length === 0" class="empty-cart">
      <p>购物车是空的。</p>
    </div>
    <div v-else>
      <table class="cart-table">
        <thead>
          <tr>
            <th>选择</th>
            <th>商品名称</th>
            <th>描述</th>
            <th>价格 (元)</th>
            <th>数量</th>
            <th>库存</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in cartItems" :key="item.id">
            <td><input type="checkbox" v-model="item.selected" /></td>
            <td>{{ item.menu_item.name }}</td>
            <td>{{ item.menu_item.description }}</td>
            <td>{{ item.menu_item.price.toFixed(2) }}</td>
            <td>
            <div class="quantity-container">
            <button class="quantity-btn" @click="changeQuantity(item, -1)" :disabled="item.quantity <= 1">-</button>
            <span class="quantity-display">{{ item.quantity }}</span>
            <button class="quantity-btn" @click="changeQuantity(item, 1)" :disabled="item.quantity >= item.menu_item.stock">+</button>
            </div>
            </td>
            <td>{{ item.menu_item.stock }}</td>
            <td><button class="btn btn-danger" @click="deleteItem(item.id)">删除</button></td>
          </tr>
        </tbody>
      </table>
      <div class="total">
        <h2>总费用: {{ totalAmount.toFixed(2) }} 元</h2>
        <button class="checkout-button" @click="openCheckoutModal">结账</button>
      </div>
    </div>
  </div>

  <!-- 结账确认弹出窗口 -->
  <div v-if="showModal" class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>结账确认</h2>
      <div v-for="item in selectedItems" :key="item.id" class="cart-item">
        <p>商品名称: {{ item.menu_item.name }}</p>
        <p>价格: ¥{{ item.menu_item.price.toFixed(2) }}</p>
        <p>数量: {{ item.quantity }}</p>
      </div>
      <h3>总金额: ¥{{ totalAmount.toFixed(2) }}</h3>
      <button @click="processPayment">付款</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: 'ShoppingCart',
  data() {
    return {
      cartItems: [], // 购物车中的商品列表
      showModal: false // 控制结账弹窗的显示与隐藏
    };
  },
  computed: {
    // 计算总金额，只计算被选中的商品
    totalAmount() {
      return this.cartItems.reduce((total, item) => {
        return item.selected ? total + item.menu_item.price * item.quantity : total;
      }, 0);
    },
    // 获取被选中的商品
    selectedItems() {
      return this.cartItems.filter(item => item.selected);
    }
  },
  methods: {
    // 获取购物车中的商品
    async fetchCartItems() {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://127.0.0.1:5000/api/cart', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.cartItems = response.data.cart_items;
      } catch (error) {
        console.error('Error fetching cart items:', error);
      }
    },
    // 删除购物车中的商品
    async deleteItem(itemId) {
      try {
        const token = localStorage.getItem('token');
        await axios.delete(`http://127.0.0.1:5000/api/cart/${itemId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.cartItems = this.cartItems.filter(item => item.id !== itemId);
      } catch (error) {
        console.error('Error deleting cart item:', error);
      }
    },
    // 修改商品数量
    async changeQuantity(item, change) {
      const newQuantity = item.quantity + change;
      if (newQuantity >= 1 && newQuantity <= item.menu_item.stock) {
        item.quantity = newQuantity;
        try {
          const token = localStorage.getItem('token');
          await axios.put(`http://127.0.0.1:5000/api/cart/${item.id}`, { quantity: newQuantity }, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
        } catch (error) {
          console.error('Error updating quantity:', error);
          item.quantity -= change;
        }
      } else {
        alert('数量无效或超出库存！');
      }
    },
    // 打开结账确认弹窗
    openCheckoutModal() {
      if (this.selectedItems.length === 0) {
        alert('请选择至少一个商品进行结账');
      } else {
        this.showModal = true;
      }
    },
    // 关闭结账确认弹窗
    closeModal() {
      this.showModal = false;
    },
    // 处理付款逻辑
    async processPayment() {
    try {
      const token = localStorage.getItem('token');

      // 将选中的商品转移到订单中
      const response = await axios.post('http://127.0.0.1:5000/api/order', {
        items: this.selectedItems,
        total_amount: this.totalAmount
      }, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });

      alert('支付成功！');
      this.showModal = false;

      // 跳转到 MyOrder.vue 页面
      this.$router.push({ name: 'MyOrder', params: { orderId: response.data.order_id } });

    } catch (error) {
      console.error('Error processing payment:', error);
      alert('支付失败，请重试');
    }
  }
},
  async created() {
    await this.fetchCartItems();
  }
};
</script>

<style scoped>
/* 样式与之前相同 */
.shopping-cart {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  margin-bottom: 20px;
}

.cart-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.cart-table th,
.cart-table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.cart-table th {
  background-color: #f2f2f2;
}

.total {
  text-align: right;
  font-weight: bold;
}

.btn {
  padding: 5px 10px;
  cursor: pointer;
}

.checkout-button {
  background-color: #2ecc71;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  cursor: pointer;
}

.checkout-button:hover {
  background-color: #27ae60;
}





/* 弹窗外层的遮罩层 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* 背景透明度加深 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000; /* 提高弹窗层级，避免被其他元素遮挡 */
}

/* 弹窗内容 */
.modal-content {
  background-color: white;
  padding: 30px; /* 增加内边距 */
  border-radius: 10px; /* 使弹窗边缘更加圆润 */
  max-width: 600px; /* 弹窗宽度稍微加大 */
  width: 90%; /* 自适应不同屏幕宽度 */
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3); /* 添加阴影增强立体感 */
  animation: slide-down 0.4s ease-out; /* 添加进入动画 */
}

/* 弹窗关闭按钮 */
.close {
  cursor: pointer;
  font-size: 24px; /* 增大关闭按钮的字体 */
  font-weight: bold;
  color: #333;
  position: absolute;
  top: 15px;
  right: 20px; /* 右上角对齐 */
  transition: color 0.3s; /* 颜色过渡效果 */
}

.close:hover {
  color: #e74c3c; /* 悬停时变成红色 */
}

/* 每个商品条目的样式 */
.cart-item {
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f9f9f9;
  border-radius: 5px; /* 每个条目的圆角 */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* 轻微阴影 */
}

/* 商品名称、价格、数量等信息 */
.cart-item p {
  margin: 5px 0;
  font-size: 16px;
}

/* 总金额标题 */
h3 {
  margin-top: 20px;
  font-size: 20px;
  color: #2c3e50;
}

/* 付款按钮 */
button {
  background-color: #3498db;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #2980b9; /* 悬停时颜色变深 */
}


/* 修改加减按钮样式 */
.quantity-btn {
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 30px;
  display: inline-flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  font-size: 18px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
  transition: background-color 0.3s ease;
}

.quantity-btn:hover {
  background-color: #2980b9;
}

.quantity-container {
  display: flex;
  align-items: center;
}

.quantity-display {
  margin: 0 10px;
  font-weight: bold;
  font-size: 16px;
}

.quantity-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

/* 弹窗的下拉动画 */
@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
