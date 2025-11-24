<script setup>
defineProps({
  color: {
    type: String,
    default: "green", // Mặc định là màu xanh lá, có thể thay đổi thành bất kỳ màu nào trong Tailwind CSS
  },
  size: {
    type: String,
    default: "md", // Các kích thước như sm, md, lg
  },
  variant: {
    type: String,
    default: "fill", // Chế độ "fill" (nền đầy) hoặc "outline" (viền)
  },
  fullWidth: {
    type: Boolean,
    default: false,
  },
  active: {
    type: Boolean,
    default: false,
  },
});

const getClasses = (variant, color, size, fullWidth, active) => {
  let colorValue, sizeValue, fullWidthValue, activeValue;

  // Setting the button variant and color
  if (variant === "gradient") {
    colorValue = `bg-gradient-to-r from-${color}-500 to-${color}-700`;
  } else if (variant === "outline") {
    colorValue = `border-2 border-${color}-500 text-${color}-500 hover:bg-${color}-500 hover:text-white`;
  } else {
    colorValue = `bg-${color}-500 text-white hover:bg-${color}-700`;
  }

  // Size classes for different button sizes
  sizeValue = size === "sm" ? "py-1 px-3 text-sm" : size === "lg" ? "py-3 px-6 text-lg" : "py-2 px-4";

  // Full-width button
  fullWidthValue = fullWidth ? "w-full" : "";

  // Active state class
  activeValue = active ? "active" : "";

  return `${colorValue} ${sizeValue} ${fullWidthValue} ${activeValue} rounded-md focus:outline-none`;
};
</script>
<template>
  <button
    class="btn mb-0"
    :class="getClasses(variant, color, size, fullWidth, active)"
  >
    <slot />
  </button>
</template>
