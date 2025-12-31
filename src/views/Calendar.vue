<template>
  <div class="calendar-page">
    <div class="page-header">
      <button @click="goBack" class="back-btn">← 返回</button>
      <h1>算法刷题日历</h1>
    </div>
    <div class="page-content">
      <Calendar 
        :problems="problems" 
        @add-problem="handleAddProblem"
        @edit-problem="handleEditProblem"
        @view-problem="handleViewProblem"
      />
    </div>
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
import { useRouter } from 'vue-router'
import Calendar from '../components/Calendar.vue'
import ProblemModal from '../components/ProblemModal.vue'
import { loadProblems, saveProblems } from '../utils/storage.js'

const router = useRouter()

const problems = ref({})
const showModal = ref(false)
const currentProblem = ref(null)
const selectedDate = ref('')

onMounted(() => {
  problems.value = loadProblems()
})

function goBack() {
  router.push('/')
}

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
    const index = problems.value[date].findIndex(p => p.id === currentProblem.value.id)
    if (index !== -1) {
      problems.value[date][index] = { ...problemData, id: currentProblem.value.id }
    }
  } else {
    const newProblem = {
      ...problemData,
      id: Date.now().toString(),
      createdAt: Date.now()
    }
    problems.value[date].push(newProblem)
  }
  
  saveProblems(problems.value)
  handleCloseModal()
}
</script>

<style scoped>
.calendar-page {
  min-height: 100vh;
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.back-btn {
  padding: 10px 20px;
  background: rgba(10, 14, 39, 0.6);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 8px;
  color: #00ffff;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.3s;
}

.back-btn:hover {
  background: rgba(0, 255, 255, 0.1);
  border-color: rgba(0, 255, 255, 0.5);
}

.page-header h1 {
  margin: 0;
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2em;
  font-weight: 700;
}

.page-content {
  max-width: 1400px;
  margin: 0 auto;
}
</style>

