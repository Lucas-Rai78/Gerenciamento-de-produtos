import { createApp } from 'vue'
import { createPinia } from 'pinia'
import '@/styles/main.css'
import App from './App.vue'
import router from './depracted/router/index.ts'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
