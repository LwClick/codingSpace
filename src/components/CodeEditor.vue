<template>
  <div class="code-editor-container">
    <textarea
      ref="textareaRef"
      v-model="code"
      class="code-editor"
      placeholder="# 在这里编写你的Python代码"
      @input="handleInput"
    ></textarea>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'run'])

const textareaRef = ref(null)
const code = ref(props.modelValue)

watch(() => props.modelValue, (newValue) => {
  if (code.value !== newValue) {
    code.value = newValue
  }
})

function handleInput() {
  emit('update:modelValue', code.value)
}
</script>

<style scoped>
.code-editor-container {
  border: 2px solid rgba(0, 255, 255, 0.3);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s;
  background: #0d1117;
  position: relative;
  box-shadow: 
    0 0 20px rgba(0, 255, 255, 0.1),
    inset 0 0 30px rgba(0, 255, 255, 0.02);
}

.code-editor-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.05), transparent);
  transition: left 0.5s;
}

.code-editor-container:focus-within {
  border-color: rgba(0, 255, 255, 0.6);
  box-shadow: 
    0 0 30px rgba(0, 255, 255, 0.3),
    inset 0 0 40px rgba(0, 255, 255, 0.05);
}

.code-editor-container:focus-within::before {
  left: 100%;
}

.code-editor {
  width: 100%;
  height: 300px;
  padding: 18px;
  border: none;
  background: #0d1117;
  color: #c9d1d9;
  font-family: 'Courier New', 'Monaco', 'Menlo', 'Consolas', monospace;
  font-size: 14px;
  line-height: 1.8;
  resize: vertical;
  outline: none;
  tab-size: 2;
  -moz-tab-size: 2;
  text-shadow: 0 0 5px rgba(0, 255, 255, 0.1);
}

.code-editor::placeholder {
  color: rgba(201, 209, 217, 0.4);
}

.code-editor:focus {
  outline: none;
  color: #e6edf3;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.2);
}

/* 代码编辑器滚动条 */
.code-editor::-webkit-scrollbar {
  width: 8px;
}

.code-editor::-webkit-scrollbar-track {
  background: rgba(13, 17, 23, 0.5);
}

.code-editor::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, rgba(0, 255, 255, 0.3), rgba(0, 128, 255, 0.3));
  border-radius: 4px;
}

.code-editor::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, rgba(0, 255, 255, 0.5), rgba(0, 128, 255, 0.5));
}
</style>

