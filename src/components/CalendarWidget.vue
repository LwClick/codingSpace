<template>
  <div class="calendar-widget">
    <div class="widget-header">
      <h3>日历</h3>
      <button @click="toggleExpanded" class="toggle-btn">
        {{ isExpanded ? '−' : '+' }}
      </button>
    </div>
    <div v-if="isExpanded" class="widget-content">
      <div class="mini-calendar">
        <div class="mini-calendar-header">
          <button @click="previousMonth" class="mini-nav-btn">‹</button>
          <span class="mini-month">{{ currentYear }}年{{ currentMonth + 1 }}月</span>
          <button @click="nextMonth" class="mini-nav-btn">›</button>
        </div>
        <div class="mini-calendar-grid">
          <div class="mini-weekday" v-for="day in weekdays" :key="day">{{ day }}</div>
          <div 
            v-for="day in calendarDays" 
            :key="day.key"
            class="mini-day"
            :class="{ 
              'other-month': !day.isCurrentMonth,
              'today': day.isToday,
              'has-problems': day.problemCount > 0,
              'selected': day.dateKey === selectedDateKey
            }"
            @click="selectDate(day)"
          >
            {{ day.day }}
          </div>
        </div>
      </div>
      <div v-if="selectedDateKey && selectedDateRecords.length > 0" class="date-records">
        <div class="records-header">
          <h4>{{ selectedDateText }}</h4>
        </div>
        <div class="records-list">
          <div 
            v-for="record in selectedDateRecords" 
            :key="record.id"
            class="record-item"
          >
            <div class="record-title">{{ record.title || '未命名' }}</div>
            <div class="record-time">{{ formatTime(record.createdAt) }}</div>
          </div>
        </div>
      </div>
      <div v-else-if="selectedDateKey" class="no-records">
        这一天还没有记录
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { getDateKey } from '../utils/storage.js'

const props = defineProps({
  problems: {
    type: Object,
    default: () => ({})
  }
})

const isExpanded = ref(true)
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
  
  const firstDay = new Date(year, month, 1)
  const firstDayWeek = firstDay.getDay()
  const lastDay = new Date(year, month + 1, 0)
  const lastDayDate = lastDay.getDate()
  
  const days = []
  
  const prevMonthLastDay = new Date(year, month, 0).getDate()
  for (let i = firstDayWeek - 1; i >= 0; i--) {
    const date = new Date(year, month - 1, prevMonthLastDay - i)
    days.push(createDayObject(date, false))
  }
  
  for (let day = 1; day <= lastDayDate; day++) {
    const date = new Date(year, month, day)
    days.push(createDayObject(date, true))
  }
  
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

const selectedDateRecords = computed(() => {
  if (!selectedDateKey.value) return []
  return props.problems[selectedDateKey.value] || []
})

const selectedDateText = computed(() => {
  if (!selectedDateKey.value) return ''
  const [year, month, day] = selectedDateKey.value.split('-')
  const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day))
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  return weekdays[date.getDay()]
})

function toggleExpanded() {
  isExpanded.value = !isExpanded.value
}

function previousMonth() {
  currentDate.value = new Date(currentYear.value, currentMonth.value - 1, 1)
}

function nextMonth() {
  currentDate.value = new Date(currentYear.value, currentMonth.value + 1, 1)
}

function selectDate(day) {
  selectedDateKey.value = day.dateKey
}

function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(parseInt(timestamp))
  if (isNaN(date.getTime())) return ''
  return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}
</script>

<style scoped>
.calendar-widget {
  position: fixed;
  top: 80px;
  right: 20px;
  width: 320px;
  max-width: calc(100vw - 40px);
  background: rgba(10, 14, 39, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 255, 255, 0.3);
  border-radius: 15px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
  z-index: 100;
  max-height: calc(100vh - 100px);
  display: flex;
  flex-direction: column;
}

@media (max-width: 768px) {
  .calendar-widget {
    width: calc(100vw - 20px);
    right: 10px;
    top: 70px;
  }
}

.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid rgba(0, 255, 255, 0.2);
}

.widget-header h3 {
  margin: 0;
  background: linear-gradient(135deg, #00ffff 0%, #0080ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 1.2em;
  font-weight: 700;
}

.toggle-btn {
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  color: #00ffff;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.toggle-btn:hover {
  background: rgba(0, 255, 255, 0.2);
  transform: scale(1.1);
}

.widget-content {
  padding: 15px;
  overflow-y: auto;
  flex: 1;
}

.mini-calendar {
  margin-bottom: 15px;
}

.mini-calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.mini-month {
  color: #00ffff;
  font-weight: 600;
  font-size: 0.9em;
}

.mini-nav-btn {
  background: rgba(0, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 255, 0.3);
  color: #00ffff;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.mini-nav-btn:hover {
  background: rgba(0, 255, 255, 0.2);
  transform: scale(1.1);
}

.mini-calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 4px;
}

.mini-weekday {
  text-align: center;
  font-size: 0.75em;
  color: rgba(0, 255, 255, 0.6);
  padding: 4px 0;
  font-weight: 600;
}

.mini-day {
  aspect-ratio: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid rgba(0, 255, 255, 0.1);
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.85em;
  color: rgba(224, 224, 224, 0.7);
  transition: all 0.3s;
  background: rgba(10, 14, 39, 0.4);
}

.mini-day:hover {
  border-color: rgba(0, 255, 255, 0.4);
  background: rgba(0, 255, 255, 0.1);
  color: #00ffff;
}

.mini-day.other-month {
  opacity: 0.3;
}

.mini-day.today {
  border-color: rgba(0, 255, 255, 0.6);
  background: rgba(0, 255, 255, 0.15);
  color: #00ffff;
  font-weight: 700;
}

.mini-day.has-problems {
  border-color: rgba(0, 255, 136, 0.4);
  background: rgba(0, 255, 136, 0.1);
}

.mini-day.selected {
  border-color: #00ffff;
  background: rgba(0, 255, 255, 0.2);
  color: #ffffff;
  font-weight: 700;
  box-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.date-records {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
}

.records-header h4 {
  margin: 0 0 10px 0;
  color: #00ffff;
  font-size: 1em;
  font-weight: 700;
}

.records-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  max-height: 200px;
  overflow-y: auto;
}

.record-item {
  background: rgba(10, 14, 39, 0.6);
  padding: 10px;
  border-radius: 8px;
  border: 1px solid rgba(0, 255, 255, 0.2);
}

.record-title {
  color: #e0e0e0;
  font-size: 0.9em;
  margin-bottom: 4px;
}

.record-time {
  color: rgba(224, 224, 224, 0.6);
  font-size: 0.75em;
}

.no-records {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid rgba(0, 255, 255, 0.2);
  color: rgba(224, 224, 224, 0.6);
  text-align: center;
  font-size: 0.9em;
}
</style>

