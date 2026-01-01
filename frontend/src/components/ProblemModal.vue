<template>
  <div class="modal-overlay" @click.self="handleClose">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ isEditMode ? '编辑题目' : '新增题目' }}</h2>
        <button class="close-btn" @click="handleClose">×</button>
      </div>
      
      <div class="modal-body">
        <!-- 第一部分：题目描述 -->
        <div class="section">
          <label class="section-label">题目描述</label>
          <textarea
            v-model="formData.description"
            class="description-input"
            placeholder="请输入题目描述..."
            rows="6"
          ></textarea>
        </div>
        
        <!-- 第二部分：Python代码 -->
        <div class="section">
          <div class="section-header">
            <label class="section-label">Python代码</label>
            <button @click="runCode" class="run-btn" :disabled="running">
              {{ running ? '运行中...' : '运行代码' }}
            </button>
          </div>
          <CodeEditor
            v-model="formData.code"
            @run="runCode"
          />
          <div v-if="codeOutput" class="code-output">
            <div class="output-label">运行结果：</div>
            <pre>{{ codeOutput }}</pre>
          </div>
          <div v-if="codeError" class="code-error">
            <div class="error-label">错误信息：</div>
            <pre>{{ codeError }}</pre>
          </div>
        </div>
        
        <!-- 第三部分：题目解析 -->
        <div class="section">
          <label class="section-label">题目解析</label>
          <textarea
            v-model="formData.analysis"
            class="analysis-input"
            placeholder="请输入题目解析..."
            rows="6"
          ></textarea>
        </div>
      </div>
      
      <div class="modal-footer">
        <button class="cancel-btn" @click="handleClose">取消</button>
        <button class="save-btn" @click="handleSave">保存</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import CodeEditor from './CodeEditor.vue'
import { runPythonCode } from '../utils/pythonRunner.js'

const props = defineProps({
  problem: {
    type: Object,
    default: null
  },
  date: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['close', 'save'])

const formData = ref({
  description: '',
  code: '',
  analysis: ''
})

const codeOutput = ref('')
const codeError = ref('')
const running = ref(false)

const isEditMode = computed(() => !!props.problem)

onMounted(() => {
  if (props.problem) {
    formData.value = {
      description: props.problem.description || '',
      code: props.problem.code || '',
      analysis: props.problem.analysis || ''
    }
  } else {
    // 默认代码模板
    formData.value.code = `# 在这里编写你的Python代码
def solution():
    # 你的代码
    pass

# 运行示例
if __name__ == '__main__':
    result = solution()
    print(result)
`
  }
})

watch(() => props.problem, (newProblem) => {
  if (newProblem) {
    formData.value = {
      description: newProblem.description || '',
      code: newProblem.code || '',
      analysis: newProblem.analysis || ''
    }
  }
}, { immediate: true })

async function runCode() {
  if (!formData.value.code.trim()) {
    codeError.value = '代码不能为空'
    return
  }
  
  running.value = true
  codeOutput.value = ''
  codeError.value = ''
  
  try {
    const result = await runPythonCode(formData.value.code)
    if (result.error) {
      codeError.value = result.error
    } else {
      codeOutput.value = result.output || '(无输出)'
    }
  } catch (error) {
    codeError.value = error.message || '运行出错'
  } finally {
    running.value = false
  }
}

function handleClose() {
  emit('close')
}

function handleSave() {
  if (!formData.value.description.trim()) {
    alert('请输入题目描述')
    return
  }
  
  const problemData = {
    date: props.date,
    title: formData.value.description.substring(0, 50) || '未命名题目',
    description: formData.value.description,
    code: formData.value.code,
    analysis: formData.value.analysis
  }
  
  emit('save', problemData)
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.modal-content {
  background: rgba(10, 14, 39, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 
    0 20px 60px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(0, 255, 255, 0.3),
    inset 0 0 80px rgba(0, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.3);
  animation: slideUp 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

@keyframes slideUp {
  from {
    transform: translateY(30px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, 
    transparent, 
    rgba(0, 255, 255, 0.8), 
    rgba(0, 128, 255, 0.8), 
    rgba(0, 255, 255, 0.8), 
    transparent
  );
  animation: shimmer 3s infinite;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 25px 30px;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
  position: relative;
  z-index: 1;
}

.modal-header h2 {
  margin: 0;
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.8em;
  font-weight: 700;
  letter-spacing: 1px;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

.close-btn {
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  font-size: 28px;
  color: #00ffff;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
}

.close-btn:hover {
  background: rgba(0, 255, 255, 0.2);
  border-color: #00ffff;
  color: #ffffff;
  transform: rotate(90deg) scale(1.1);
  box-shadow: 0 0 25px rgba(0, 255, 255, 0.5);
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 30px;
  position: relative;
  z-index: 1;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-label {
  font-weight: 700;
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.2em;
  margin-bottom: 8px;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
}

.description-input,
.analysis-input {
  width: 100%;
  padding: 14px;
  border: 2px solid rgba(0, 255, 255, 0.2);
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  transition: all 0.3s;
  background: rgba(10, 14, 39, 0.6);
  color: #e0e0e0;
  backdrop-filter: blur(10px);
}

.description-input::placeholder,
.analysis-input::placeholder {
  color: rgba(224, 224, 224, 0.5);
}

.description-input:focus,
.analysis-input:focus {
  outline: none;
  border-color: #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
  background: rgba(10, 14, 39, 0.8);
}

.run-btn {
  background: linear-gradient(135deg, rgba(0, 255, 136, 0.2), rgba(0, 204, 106, 0.2));
  color: #00ff88;
  border: 1px solid rgba(0, 255, 136, 0.5);
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9em;
  transition: all 0.3s;
  font-weight: 600;
  box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
}

.run-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  color: #0a0e27;
  border-color: #00ff88;
  box-shadow: 0 0 25px rgba(0, 255, 136, 0.5);
  transform: translateY(-2px);
}

.run-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.code-output,
.code-error {
  margin-top: 12px;
  padding: 14px;
  border-radius: 10px;
  font-size: 0.9em;
  border: 1px solid;
}

.code-output {
  background: rgba(0, 255, 136, 0.1);
  border-color: rgba(0, 255, 136, 0.4);
  color: #00ff88;
  box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
}

.code-error {
  background: rgba(255, 68, 68, 0.1);
  border-color: rgba(255, 68, 68, 0.4);
  color: #ff6b6b;
  box-shadow: 0 0 15px rgba(255, 68, 68, 0.2);
}

.output-label,
.error-label {
  font-weight: 700;
  margin-bottom: 10px;
  font-size: 1em;
}

.output-label {
  color: #00ff88;
  text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
}

.error-label {
  color: #ff6b6b;
  text-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
}

.code-output pre,
.code-error pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
  font-family: 'Courier New', 'Monaco', monospace;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 25px 30px;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
  position: relative;
  z-index: 1;
}

.cancel-btn,
.save-btn {
  padding: 12px 28px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.3s;
  font-weight: 600;
}

.cancel-btn {
  background: rgba(224, 224, 224, 0.1);
  color: #e0e0e0;
  border: 1px solid rgba(224, 224, 224, 0.3);
}

.cancel-btn:hover {
  background: rgba(224, 224, 224, 0.2);
  border-color: rgba(224, 224, 224, 0.5);
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(224, 224, 224, 0.2);
}

.save-btn {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 128, 255, 0.2));
  color: #00ffff;
  border: 1px solid rgba(0, 255, 255, 0.5);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
}

.save-btn:hover {
  background: linear-gradient(135deg, #00ffff, #0080ff);
  color: #0a0e27;
  border-color: #00ffff;
  box-shadow: 0 0 25px rgba(0, 255, 255, 0.5);
  transform: translateY(-2px);
}
</style>


