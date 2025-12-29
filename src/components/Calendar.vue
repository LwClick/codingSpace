<template>
  <div class="calendar-container">
    <div class="calendar-header">
      <button @click="previousMonth" class="nav-btn">‹</button>
      <h2>{{ currentYear }}年 {{ currentMonth + 1 }}月</h2>
      <button @click="nextMonth" class="nav-btn">›</button>
    </div>
    
    <div class="calendar-grid">
      <div class="weekday" v-for="day in weekdays" :key="day">{{ day }}</div>
      <div 
        v-for="day in calendarDays" 
        :key="day.key"
        class="calendar-day"
        :class="{ 
          'other-month': !day.isCurrentMonth,
          'today': day.isToday,
          'has-problems': day.problemCount > 0
        }"
        @click="selectDate(day.date)"
      >
        <div class="day-number">{{ day.day }}</div>
        <div v-if="day.problemCount > 0" class="problem-badge">
          {{ day.problemCount }}题
        </div>
        <button 
          class="add-btn"
          @click.stop="addProblem(day.dateKey)"
          title="添加题目"
        >
          +
        </button>
      </div>
    </div>
    
    <div v-if="selectedDateProblems.length > 0" class="problems-list">
      <h3>{{ selectedDateText }} 的题目</h3>
      <div class="problem-items">
        <div 
          v-for="problem in selectedDateProblems" 
          :key="problem.id"
          class="problem-item"
          @click="viewProblem(problem)"
        >
          <div class="problem-title">{{ problem.title || '未命名题目' }}</div>
          <div class="problem-actions">
            <button @click.stop="editProblem(problem)" class="edit-btn">编辑</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { getDateKey } from '../utils/storage.js'

const props = defineProps({
  problems: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['add-problem', 'edit-problem', 'view-problem'])

const currentDate = ref(new Date())
const selectedDateKey = ref('')

const weekdays = ['日', '一', '二', '三', '四', '五', '六']

const currentYear = computed(() => currentDate.value.getFullYear())
const currentMonth = computed(() => currentDate.value.getMonth())

const today = new Date()
const todayKey = getDateKey(today)

const calendarDays = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value
  
  // 获取当月第一天
  const firstDay = new Date(year, month, 1)
  const firstDayWeek = firstDay.getDay()
  
  // 获取当月最后一天
  const lastDay = new Date(year, month + 1, 0)
  const lastDayDate = lastDay.getDate()
  
  const days = []
  
  // 上个月的日期
  const prevMonthLastDay = new Date(year, month, 0).getDate()
  for (let i = firstDayWeek - 1; i >= 0; i--) {
    const date = new Date(year, month - 1, prevMonthLastDay - i)
    days.push(createDayObject(date, false))
  }
  
  // 当月的日期
  for (let day = 1; day <= lastDayDate; day++) {
    const date = new Date(year, month, day)
    days.push(createDayObject(date, true))
  }
  
  // 下个月的日期（补齐到42天，6行）
  const remainingDays = 42 - days.length
  for (let day = 1; day <= remainingDays; day++) {
    const date = new Date(year, month + 1, day)
    days.push(createDayObject(date, false))
  }
  
  return days
})

function createDayObject(date, isCurrentMonth) {
  const dateKey = getDateKey(date)
  const dayProblems = props.problems[dateKey] || []
  const isToday = dateKey === todayKey
  
  return {
    date,
    dateKey,
    day: date.getDate(),
    isCurrentMonth,
    isToday,
    problemCount: dayProblems.length
  }
}

const selectedDateProblems = computed(() => {
  if (!selectedDateKey.value) return []
  return props.problems[selectedDateKey.value] || []
})

const selectedDateText = computed(() => {
  if (!selectedDateKey.value) return ''
  const [year, month, day] = selectedDateKey.value.split('-')
  return `${year}年${month}月${day}日`
})

function previousMonth() {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
}

function nextMonth() {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
}

function selectDate(date) {
  selectedDateKey.value = getDateKey(date)
}

function addProblem(dateKey) {
  emit('add-problem', dateKey)
}

function editProblem(problem) {
  emit('edit-problem', problem)
}

function viewProblem(problem) {
  emit('view-problem', problem)
}
</script>

<style scoped>
.calendar-container {
  background: white;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.calendar-header h2 {
  margin: 0;
  color: #333;
  font-size: 1.8em;
}

.nav-btn {
  background: #667eea;
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  transition: all 0.3s;
}

.nav-btn:hover {
  background: #5568d3;
  transform: scale(1.1);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 10px;
  margin-bottom: 30px;
}

.weekday {
  text-align: center;
  font-weight: 600;
  color: #667eea;
  padding: 10px;
  font-size: 1.1em;
}

.calendar-day {
  aspect-ratio: 1;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  background: #f9f9f9;
}

.calendar-day:hover {
  border-color: #667eea;
  background: #f0f0ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(102, 126, 234, 0.2);
}

.calendar-day.other-month {
  opacity: 0.4;
  background: #f5f5f5;
}

.calendar-day.today {
  border-color: #667eea;
  background: #e8eaff;
  font-weight: 600;
}

.calendar-day.has-problems {
  border-color: #4caf50;
  background: #e8f5e9;
}

.day-number {
  font-size: 1.2em;
  color: #333;
  margin-bottom: 4px;
}

.problem-badge {
  background: #4caf50;
  color: white;
  font-size: 0.7em;
  padding: 2px 6px;
  border-radius: 10px;
  margin-top: auto;
}

.add-btn {
  position: absolute;
  top: 4px;
  right: 4px;
  background: #667eea;
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  opacity: 0;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.calendar-day:hover .add-btn {
  opacity: 1;
}

.add-btn:hover {
  background: #5568d3;
  transform: scale(1.2);
}

.problems-list {
  margin-top: 30px;
  padding-top: 30px;
  border-top: 2px solid #e0e0e0;
}

.problems-list h3 {
  color: #333;
  margin-bottom: 15px;
}

.problem-items {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.problem-item {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.problem-item:hover {
  background: #e8eaff;
  transform: translateX(5px);
}

.problem-title {
  font-weight: 500;
  color: #333;
}

.problem-actions {
  display: flex;
  gap: 10px;
}

.edit-btn {
  background: #667eea;
  color: white;
  border: none;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
  transition: all 0.3s;
}

.edit-btn:hover {
  background: #5568d3;
}
</style>

