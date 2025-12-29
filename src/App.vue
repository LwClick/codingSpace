<template>
  <div id="app">
    <header class="app-header">
      <h1>算法刷题日历</h1>
    </header>
    <main class="app-main">
      <Calendar 
        :problems="problems" 
        @add-problem="handleAddProblem"
        @edit-problem="handleEditProblem"
        @view-problem="handleViewProblem"
      />
    </main>
    <ProblemModal
      v-if="showModal"
      :problem="currentProblem"
      :date="selectedDate"
      @close="handleCloseModal"
      @save="handleSaveProblem"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Calendar from './components/Calendar.vue'
import ProblemModal from './components/ProblemModal.vue'
import { loadProblems, saveProblems } from './utils/storage.js'

const problems = ref({})
const showModal = ref(false)
const currentProblem = ref(null)
const selectedDate = ref('')

onMounted(() => {
  problems.value = loadProblems()
})

const handleAddProblem = (date) => {
  selectedDate.value = date
  currentProblem.value = null
  showModal.value = true
}

const handleEditProblem = (problem) => {
  currentProblem.value = { ...problem }
  selectedDate.value = problem.date
  showModal.value = true
}

const handleViewProblem = (problem) => {
  currentProblem.value = { ...problem }
  selectedDate.value = problem.date
  showModal.value = true
}

const handleCloseModal = () => {
  showModal.value = false
  currentProblem.value = null
  selectedDate.value = ''
}

const handleSaveProblem = (problemData) => {
  const date = problemData.date
  if (!problems.value[date]) {
    problems.value[date] = []
  }
  
  if (currentProblem.value && currentProblem.value.id) {
    // 编辑模式
    const index = problems.value[date].findIndex(p => p.id === currentProblem.value.id)
    if (index !== -1) {
      problems.value[date][index] = { ...problemData, id: currentProblem.value.id }
    }
  } else {
    // 新增模式
    const newProblem = {
      ...problemData,
      id: Date.now().toString()
    }
    problems.value[date].push(newProblem)
  }
  
  saveProblems(problems.value)
  handleCloseModal()
}
</script>

<style scoped>
#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.app-header {
  background: rgba(255, 255, 255, 0.95);
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.app-header h1 {
  margin: 0;
  color: #333;
  font-size: 2.5em;
  font-weight: 600;
}

.app-main {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}
</style>

