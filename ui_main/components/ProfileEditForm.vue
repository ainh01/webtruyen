<template>
    <div>
      <label>Tên:</label>
      <input v-model="editedUser.name" type="text" />
      
      <label>Email:</label>
      <input v-model="editedUser.email" type="email" />
      
      <label>Số điện thoại:</label>
      <input v-model="editedUser.phone" type="tel" />
  
      <button @click="save">Lưu</button>
      <button @click="cancel">Hủy</button>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      user: Object
    },
    data() {
      return {
        editedUser: { ...this.user }
      }
    },
    methods: {
      save() {
        this.$emit('save', this.editedUser);
      },
      cancel() {
        this.$emit('save', this.user);
      }
    }
  }
  </script>
  