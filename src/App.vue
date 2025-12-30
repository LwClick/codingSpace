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
  background: 
    radial-gradient(circle at 20% 50%, rgba(0, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(138, 43, 226, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 40% 20%, rgba(0, 100, 255, 0.1) 0%, transparent 50%),
    linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
  background-size: 100% 100%;
  position: relative;
  overflow-x: hidden;
}

#app::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(2px 2px at 20% 30%, #00ffff, transparent),
    radial-gradient(2px 2px at 60% 70%, #0080ff, transparent),
    radial-gradient(1px 1px at 50% 50%, #ffffff, transparent),
    radial-gradient(1px 1px at 80% 10%, #00ffff, transparent),
    radial-gradient(2px 2px at 90% 40%, #0080ff, transparent),
    radial-gradient(1px 1px at 33% 60%, #ffffff, transparent),
    radial-gradient(2px 2px at 10% 80%, #00ffff, transparent);
  background-repeat: repeat;
  background-size: 200% 200%;
  animation: float 20s ease-in-out infinite;
  opacity: 0.4;
  pointer-events: none;
  z-index: 0;
}

.app-header {
  background: rgba(10, 14, 39, 0.8);
  backdrop-filter: blur(10px);
  border-bottom: 2px solid rgba(0, 255, 255, 0.3);
  padding: 25px 20px;
  box-shadow: 0 4px 30px rgba(0, 255, 255, 0.2);
  text-align: center;
  position: relative;
  z-index: 1;
}

.app-header::before {
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

.app-header h1 {
  margin: 0;
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 50%, #8a2be2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2.8em;
  font-weight: 700;
  letter-spacing: 2px;
  text-shadow: 0 0 30px rgba(0, 255, 255, 0.5);
  animation: pulse 3s ease-in-out infinite;
}

.app-main {
  padding: 30px 20px;
  max-width: 1400px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}
</style>


