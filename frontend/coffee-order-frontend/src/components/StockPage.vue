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

    <div class="content">
      <div class="inventory-management">
        <!-- 商品列表 -->
        <div class="table-container">
          <h1>库存管理</h1>
          <table class="menu-table">
            <thead>
              <tr>
                <th>商品名称</th>
                <th>库存</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in menuItems" :key="item.id">
                <td>{{ item.name }}</td>
                <td>
                  <input type="number" v-model="item.stock" />
                </td>
                <td>
                  <button class="btn update-btn" @click="updateStock(item.id, item.stock)">更新库存</button>
                  <button class="btn delete-btn" @click="deleteMenuItem(item.id)">删除商品</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- 添加新商品 -->
        <div class="add-item-form">
          <h3>添加新商品</h3>
          <form @submit.prevent="addNewMenuItem">
    <input v-model="newItem.name" placeholder="商品名称" />
    <input v-model="newItem.description" placeholder="商品描述" />
    <input v-model="newItem.price" type="text" placeholder="价格" min="0" step="0.01" />
    <input v-model.number="newItem.stock" type="number" placeholder="库存" min="0" />
    <input type="file" @change="handleFileUpload" />
    <button class="btn add-btn" @click="addNewMenuItem">添加商品</button>
</form>
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
      username: localStorage.getItem('username') || '管理员',
      role: 'admin',
      newItem: {
        name: '',
        description: '',
        price: null,  // 修改为 null
        stock: null,  // 修改为 null
      },
      selectedFile: null, // 用户选择的文件
      menuItems: [],
      isSubmitting: false // 防止重复提交的锁
    };
  },
  methods: {
    async fetchMenuItems() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/menu_items_show', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}` // JWT认证
          }
        });
        this.menuItems = response.data;
      } catch (error) {
        console.error('获取商品信息失败:', error);
      }
    },
    async updateStock(id, stock) {
      try {
        await axios.put(`http://127.0.0.1:5000/api/menu_items/${id}`, { stock }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        alert('库存更新成功');
        this.fetchMenuItems();
      } catch (error) {
        console.error('更新库存失败:', error);
      }
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0]; // 获取上传的文件
    },
    async addNewMenuItem() {
  if (this.isSubmitting) return; // 如果已经在提交，阻止重复提交
  this.isSubmitting = true; // 开始提交

  try {
    // 检查文件和名称是否已选择
    if (this.selectedFile && this.newItem.name) {
      // 将价格转换为小数
      const price = parseFloat(this.newItem.price);

      // 确保价格是有效的小数且非负
      if (isNaN(price) || price < 0) {
          alert('价格必须是一个有效的非负小数');
          return;
      }

      const formData = new FormData();
      formData.append('name', this.newItem.name);
      formData.append('description', this.newItem.description);
      formData.append('price', price); // 使用小数价格
      formData.append('stock', this.newItem.stock);
      formData.append('file', this.selectedFile);

      // 提交数据到后端
      await axios.post('http://127.0.0.1:5000/api/menu_items_insert', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });

      alert('商品添加成功');
      // 重置表单
      this.newItem = { name: '', description: '', price: '', stock: 0 }; // price 设为 ''
      this.selectedFile = null;
      this.fetchMenuItems();
    } else {
      alert('请填写商品名称并选择图片文件');
    }
  } catch (error) {
    console.error('添加商品失败:', error);
  } finally {
    this.isSubmitting = false; // 提交完成后解除锁
  }
},
    async deleteMenuItem(id) {
      try {
        await axios.delete(`http://127.0.0.1:5000/api/menu_items/${id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        alert('商品删除成功');
        this.fetchMenuItems();
      } catch (error) {
        console.error('删除商品失败:', error);
      }
    }
  },
  mounted() {
    this.fetchMenuItems();
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

.info-divider, .divider {
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
  display: flex;
  justify-content: space-between;
}

.inventory-management {
  display: flex;
  width: 100%;
  justify-content: space-between;
}

.table-container {
  width: 65%;
  max-height: 70vh;
  overflow-y: auto; /* 表格滚动条 */
  padding-right: 20px;
}

.menu-table {
  width: 100%;
  border-collapse: collapse;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.menu-table th, .menu-table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: center;
}

.menu-table th {
  background-color: #007bff;
  color: white;
}

.menu-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.menu-table tr:hover {
  background-color: #f1f1f1;
}

.add-item-form {
  width: 30%;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.add-item-form h3 {
  margin-bottom: 20px;
}

.add-item-form input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.update-btn {
  background-color: #28a745;
  color: white;
}

.update-btn:hover {
  background-color: #218838;
}

.delete-btn {
  background-color: #dc3545;
  color: white;
}

.delete-btn:hover {
  background-color: #c82333;
  }

.add-btn {
  background-color: #007bff;
  color: white;
  width: 100%;
}

.add-btn:hover {
  background-color: #0056b3;
}

.add-item-form input[type="file"] {
  padding: 3px;
  border: none;
}

.table-container::-webkit-scrollbar {
  width: 10px;
}

.table-container::-webkit-scrollbar-thumb {
  background-color: rgba(0, 123, 255, 0.7);
  border-radius: 10px;
}

.table-container::-webkit-scrollbar-track {
  background-color: #f8f9fa;
}

.add-item-form button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}
</style>