<template>
    <div>
      <p><strong>Tên:</strong> {{ user.name }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Số điện thoại:</strong> {{ user.phone }}</p>
      <button @click="$emit('edit')">Chỉnh sửa</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      user: Object
    }
  }
  </script>
  