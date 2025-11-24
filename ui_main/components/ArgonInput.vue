<script setup>
const emit = defineEmits(["update:modelValue"]);

defineProps({
  size: {
    type: String,
    default: "default",
  },
  success: {
    type: Boolean,
    default: false,
  },
  error: {
    type: Boolean,
    default: false,
  },
  icon: {
    type: String,
    default: "",
  },
  iconDir: {
    type: String,
    default: "",
  },
  name: {
    type: String,
    default: "",
  },
  id: {
    type: String,
    default: "",
  },
  modelValue: {
    type: String,
    default: "",
  },
  placeholder: {
    type: String,
    default: "",
  },
  type: {
    type: String,
    default: "text",
  },
  isRequired: {
    type: Boolean,
    default: false,
  },
});

const getClasses = (size, success, error) => {
  let sizeValue, isValidValue;

  // Adjust size value
  sizeValue = size === "default" ? "py-2 px-4" : size === "small" ? "py-1 px-3 text-sm" : "py-3 px-5";

  // Determine validation classes
  if (error) {
    isValidValue = "border-red-500";
  } else if (success) {
    isValidValue = "border-green-500";
  } else {
    isValidValue = "border-gray-300";
  }

  return `${sizeValue} ${isValidValue} focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-md`;
};

const getIcon = (icon) => (icon ? icon : null);
const hasIcon = (icon) => (icon ? "flex items-center" : null);
</script>
<template>
  <div class="mb-4">
    <div :class="hasIcon(icon)" class="flex items-center relative">
      <span v-if="iconDir === 'left'" class="absolute left-3">
        <i :class="getIcon(icon)" class="text-gray-400"></i>
      </span>

      <input
        :id="id"
        :type="type"
        :name="name"
        :value="modelValue"
        :placeholder="placeholder"
        :required="isRequired"
        :class="getClasses(size, success, error)"
        class="w-full pl-10 pr-3 py-2"
        @input="emit('update:modelValue', $event.target.value)"
      />
      
      <span v-if="iconDir === 'right'" class="absolute right-3">
        <i :class="getIcon(icon)" class="text-gray-400"></i>
      </span>
    </div>
  </div>
</template>
