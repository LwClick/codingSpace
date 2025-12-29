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
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 2px solid #e0e0e0;
}

.modal-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.5em;
}

.close-btn {
  background: none;
  border: none;
  font-size: 32px;
  color: #999;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.close-btn:hover {
  color: #333;
  transform: rotate(90deg);
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 30px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-label {
  font-weight: 600;
  color: #333;
  font-size: 1.1em;
  margin-bottom: 8px;
}

.description-input,
.analysis-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.3s;
}

.description-input:focus,
.analysis-input:focus {
  outline: none;
  border-color: #667eea;
}

.run-btn {
  background: #4caf50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9em;
  transition: all 0.3s;
}

.run-btn:hover:not(:disabled) {
  background: #45a049;
  transform: translateY(-1px);
}

.run-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.code-output,
.code-error {
  margin-top: 10px;
  padding: 12px;
  border-radius: 6px;
  font-size: 0.9em;
}

.code-output {
  background: #e8f5e9;
  border: 1px solid #4caf50;
}

.code-error {
  background: #ffebee;
  border: 1px solid #f44336;
}

.output-label,
.error-label {
  font-weight: 600;
  margin-bottom: 8px;
}

.output-label {
  color: #2e7d32;
}

.error-label {
  color: #c62828;
}

.code-output pre,
.code-error pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px 30px;
  border-top: 2px solid #e0e0e0;
}

.cancel-btn,
.save-btn {
  padding: 10px 24px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.3s;
}

.cancel-btn {
  background: #e0e0e0;
  color: #333;
}

.cancel-btn:hover {
  background: #d0d0d0;
}

.save-btn {
  background: #667eea;
  color: white;
}

.save-btn:hover {
  background: #5568d3;
  transform: translateY(-1px);
}
</style>

