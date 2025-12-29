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
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  transition: border-color 0.3s;
  background: #282c34;
}

.code-editor-container:focus-within {
  border-color: #667eea;
}

.code-editor {
  width: 100%;
  height: 300px;
  padding: 15px;
  border: none;
  background: #282c34;
  color: #abb2bf;
  font-family: 'Courier New', 'Monaco', 'Menlo', monospace;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  outline: none;
  tab-size: 2;
  -moz-tab-size: 2;
}

.code-editor::placeholder {
  color: #5c6370;
}

.code-editor:focus {
  outline: none;
}
</style>

