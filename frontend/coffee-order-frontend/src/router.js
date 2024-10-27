import { createRouter, createWebHistory } from 'vue-router';
import RegisterForm from './components/RegisterForm.vue';
import LoginForm from './components/LoginForm.vue';
import CoffeeMenu from './components/CoffeeMenu.vue';
import ShoppingCart from './components/ShoppingCart.vue';
import MyOrder from './components/MyOrder.vue'; // 确保导入 MyOrder 组件
import AdminPage from './components/AdminPage.vue';
import OrderPage from './components/OrderPage.vue';
import StockPage from './components/StockPage.vue';

const routes = [
  { path: '/register', component: RegisterForm },
  { path: '/login', component: LoginForm },
  { path: '/menu', component: CoffeeMenu, meta: { requiresAuth: true } }, // 需要身份验证
  { path: '/cart', component: ShoppingCart, meta: { requiresAuth: true } }, // 需要身份验证
  { path: '/admin', component: AdminPage, meta: { requiresAuth: true } }, // 需要身份验证
  { path: '/orders', component: OrderPage, meta: { requiresAuth: true } }, // 需要身份验证
  { path: '/stock', component: StockPage, meta: { requiresAuth: true } }, // 需要身份验证
  { path: '/my-orders', name: 'MyOrder', component: MyOrder, meta: { requiresAuth: true } }, // 使用 MyOrder 组件并重命名为 'MyOrder'
  { path: '/', redirect: '/login' },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 全局导航守卫
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token'); // 检查是否有 token

  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    // 如果路由需要身份验证且用户未登录，重定向到登录页面
    next({ path: '/login' });
  } else {
    next(); // 允许访问路由
  }
});

export default router;

