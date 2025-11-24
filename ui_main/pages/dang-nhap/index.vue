<script>
import axios from "axios";


const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export default {
  data() {
    return {
      isLogin: true,
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      error: null,
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post(`${API_BASE_URL}/login/`, {
          email: this.email,
          password: this.password,
        });
        console.log("token:", response.data.token);
        // Lưu token vào localStorage
        localStorage.setItem('token', response.data.token);

        window.location.href = "/";
      } catch (error) {
        this.error = error.response.detail || "Đã xảy ra lỗi.";
      }
    },
    async register() {
      try {

        if (this.password !== this.confirmPassword) {
          this.error = "Mật khẩu xác nhận không khớp.";
          return;
        }

        const response = await axios.post(`${API_BASE_URL}/register/`, {
          username: this.username,
          email: this.email,  // Pass email here
          password: this.password,
        });
        alert(response.data.message);
        this.isLogin = true;
      } catch (error) {
        this.error = error.response.data.detail || "Đã xảy ra lỗi.";
      }
    }
  },
};
</script>

<template>
  <div class="relative pt-12 px-4 min-h-screen bg-gray-100">
    <div class="absolute top-0 inset-x-0 h-80 bg-gradient-to-b from-indigo-500 to-[#2dce89] -z-10"></div>
    <div class="max-w-md mx-auto p-8 bg-white rounded-lg shadow-lg border border-gray-200">
      <h2 class="text-3xl font-bold text-center text-[#2dce89] mb-6">
        {{ isLogin ? "ĐĂNG NHẬP" : "ĐĂNG KÝ" }}
      </h2>
      
      <!-- Form -->
      <form @submit.prevent="isLogin ? login() : register()" class="space-y-6">
        <div v-if="!isLogin">
          <label for="username" class="block text-sm font-medium text-gray-700">Username</label>
          <input
            type="text"
            v-model="username"
            id="username"
            required
            class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div>
          <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
          <input
            type="email"
            v-model="email"
            id="email"
            required
            class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        
        <div>
          <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            v-model="password"
            id="password"
            required
            class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <div v-if="!isLogin">
          <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Xác nhận Mật khẩu</label>
          <input
            type="password"
            v-model="confirmPassword"
            id="confirmPassword"
            required
            class="w-full mt-2 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <button
          type="submit"
          class="w-full py-2 bg-[#2dce89] text-white font-semibold rounded-lg hover:bg-[#2dce80] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-opacity-50"
        >
          {{ isLogin ? "Đăng Nhập" : "Đăng Ký" }}
        </button>
      </form>
      
      <!-- Thông báo Lỗi -->
      <div v-if="error" class="text-red-500 text-sm mt-4">{{ error }}</div>
      
      <!-- Liên kết Chuyển đổi -->
      <div class="text-center mt-6">
        <a
          href="#"
          class="text-[#2dce89] hover:text-[#2dce89] text-sm"
          @click.prevent="isLogin = !isLogin"
        >
          {{ isLogin ? "Chưa có tài khoản? Đăng ký ngay" : "Đã có tài khoản? Đăng nhập" }}
        </a>
      </div>
    </div>
  </div>
</template>

