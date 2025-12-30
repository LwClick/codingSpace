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
  background: rgba(10, 14, 39, 0.6);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 35px;
  box-shadow: 
    0 8px 32px rgba(0, 0, 0, 0.4),
    0 0 0 1px rgba(0, 255, 255, 0.2),
    inset 0 0 60px rgba(0, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.calendar-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(0, 255, 255, 0.1) 0%, transparent 70%);
  animation: float 15s ease-in-out infinite;
  pointer-events: none;
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  position: relative;
  z-index: 1;
}

.calendar-header h2 {
  margin: 0;
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 2em;
  font-weight: 700;
  letter-spacing: 1px;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

.nav-btn {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 128, 255, 0.2));
  color: #00ffff;
  border: 2px solid rgba(0, 255, 255, 0.5);
  width: 45px;
  height: 45px;
  border-radius: 50%;
  font-size: 26px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
  position: relative;
  overflow: hidden;
}

.nav-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(0, 255, 255, 0.3);
  transform: translate(-50%, -50%);
  transition: width 0.6s, height 0.6s;
}

.nav-btn:hover::before {
  width: 200px;
  height: 200px;
}

.nav-btn:hover {
  border-color: #00ffff;
  box-shadow: 0 0 25px rgba(0, 255, 255, 0.6);
  transform: scale(1.1) rotate(5deg);
  color: #ffffff;
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 12px;
  margin-bottom: 30px;
  position: relative;
  z-index: 1;
}

.weekday {
  text-align: center;
  font-weight: 600;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.1), rgba(0, 128, 255, 0.1));
  color: #00ffff;
  padding: 12px;
  font-size: 1.1em;
  border-radius: 8px;
  border: 1px solid rgba(0, 255, 255, 0.2);
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.calendar-day {
  aspect-ratio: 1;
  border: 2px solid rgba(0, 255, 255, 0.2);
  border-radius: 12px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  background: rgba(10, 14, 39, 0.4);
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.calendar-day::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(0, 255, 255, 0.1), transparent);
  transition: left 0.5s;
}

.calendar-day:hover::before {
  left: 100%;
}

.calendar-day:hover {
  border-color: #00ffff;
  background: rgba(0, 255, 255, 0.1);
  transform: translateY(-4px) scale(1.02);
  box-shadow: 
    0 8px 25px rgba(0, 255, 255, 0.3),
    0 0 20px rgba(0, 255, 255, 0.2),
    inset 0 0 20px rgba(0, 255, 255, 0.05);
}

.calendar-day.other-month {
  opacity: 0.3;
  background: rgba(10, 14, 39, 0.2);
}

.calendar-day.today {
  border-color: #00ffff;
  background: rgba(0, 255, 255, 0.15);
  font-weight: 700;
  box-shadow: 
    0 0 20px rgba(0, 255, 255, 0.4),
    inset 0 0 20px rgba(0, 255, 255, 0.1);
  animation: glow 2s ease-in-out infinite;
}

.calendar-day.has-problems {
  border-color: #00ff88;
  background: rgba(0, 255, 136, 0.1);
  box-shadow: 0 0 15px rgba(0, 255, 136, 0.3);
}

.calendar-day.has-problems:hover {
  box-shadow: 
    0 8px 25px rgba(0, 255, 136, 0.4),
    0 0 20px rgba(0, 255, 136, 0.3);
}

.day-number {
  font-size: 1.3em;
  color: #e0e0e0;
  margin-bottom: 4px;
  font-weight: 600;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
  position: relative;
  z-index: 1;
}

.problem-badge {
  background: linear-gradient(135deg, #00ff88, #00cc6a);
  color: #0a0e27;
  font-size: 0.7em;
  padding: 3px 8px;
  border-radius: 12px;
  margin-top: auto;
  font-weight: 700;
  box-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
  position: relative;
  z-index: 1;
  animation: pulse 2s ease-in-out infinite;
}

.add-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.3), rgba(0, 128, 255, 0.3));
  color: #00ffff;
  border: 1px solid rgba(0, 255, 255, 0.5);
  width: 26px;
  height: 26px;
  border-radius: 50%;
  font-size: 18px;
  line-height: 1;
  cursor: pointer;
  opacity: 0;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
  z-index: 2;
}

.calendar-day:hover .add-btn {
  opacity: 1;
}

.add-btn:hover {
  background: linear-gradient(135deg, #00ffff, #0080ff);
  color: #0a0e27;
  border-color: #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.6);
  transform: scale(1.3) rotate(90deg);
}

.problems-list {
  margin-top: 30px;
  padding-top: 30px;
  border-top: 2px solid rgba(0, 255, 255, 0.2);
  position: relative;
  z-index: 1;
}

.problems-list h3 {
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 20px;
  font-size: 1.4em;
  font-weight: 700;
  text-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
}

.problem-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.problem-item {
  background: rgba(10, 14, 39, 0.5);
  backdrop-filter: blur(10px);
  padding: 18px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.4s;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid rgba(0, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.problem-item::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: 3px;
  background: linear-gradient(180deg, #00ffff, #0080ff);
  transform: scaleY(0);
  transition: transform 0.4s;
}

.problem-item:hover::before {
  transform: scaleY(1);
}

.problem-item:hover {
  background: rgba(0, 255, 255, 0.1);
  transform: translateX(8px);
  border-color: rgba(0, 255, 255, 0.5);
  box-shadow: 0 4px 20px rgba(0, 255, 255, 0.2);
}

.problem-title {
  font-weight: 500;
  color: #e0e0e0;
  position: relative;
  z-index: 1;
}

.problem-actions {
  display: flex;
  gap: 10px;
  position: relative;
  z-index: 1;
}

.edit-btn {
  background: linear-gradient(135deg, rgba(0, 255, 255, 0.2), rgba(0, 128, 255, 0.2));
  color: #00ffff;
  border: 1px solid rgba(0, 255, 255, 0.5);
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9em;
  transition: all 0.3s;
  font-weight: 600;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.2);
}

.edit-btn:hover {
  background: linear-gradient(135deg, #00ffff, #0080ff);
  color: #0a0e27;
  border-color: #00ffff;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);
  transform: translateY(-2px);
}
</style>


