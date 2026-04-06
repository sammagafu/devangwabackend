# Devangwa Frontend - Vue.js Application

The frontend application for the Devangwa Coaching platform, built with Vue.js 3, Vite, and modern web technologies. Provides an intuitive user interface for course consumption, user management, and community interaction.

## 🚀 Features

- **User Authentication:** Login, registration, profile management
- **Course Platform:** Browse, purchase, and consume courses
- **Interactive Learning:** Video playback, quizzes, progress tracking
- **Community Features:** Discussion forums and user interactions
- **Payment Integration:** Secure course purchasing
- **Responsive Design:** Mobile-first approach with Bootstrap
- **Real-time Updates:** Dynamic content loading and state management
- **Accessibility:** WCAG compliant components

## 🛠 Tech Stack

- **Framework:** Vue.js 3 (Composition API)
- **Build Tool:** Vite
- **State Management:** Pinia
- **Routing:** Vue Router 4
- **UI Framework:** Bootstrap 5 + Bootstrap Vue Next
- **HTTP Client:** Axios
- **Icons:** FontAwesome + Oh Vue Icons
- **Video Player:** Plyr
- **Charts:** ApexCharts
- **Form Handling:** Native Vue + Bootstrap forms
- **Styling:** SCSS with Bootstrap customization

## 📁 Project Structure

```
devangwacoaching/
├── public/                   # Static assets
│   ├── favicon.ico
│   └── assets/              # Images, fonts, etc.
├── src/
│   ├── assets/              # Compiled assets (SCSS, images)
│   │   ├── scss/           # Global styles
│   │   └── images/         # Static images
│   ├── components/          # Reusable Vue components
│   │   ├── AdvanceMenu.vue
│   │   ├── ApexChart.vue
│   │   ├── PaymentForm.vue
│   │   └── ...             # UI components
│   ├── views/               # Page-level components
│   │   ├── pages/
│   │   │   ├── auth/       # Authentication pages
│   │   │   ├── course/     # Course-related pages
│   │   │   ├── accounts/   # User account pages
│   │   │   └── ...         # Other feature pages
│   │   └── layouts/        # Layout components
│   ├── stores/              # Pinia state management
│   │   ├── auth.js         # Authentication state
│   │   ├── cart.js         # Shopping cart state
│   │   └── layout.ts       # UI layout state
│   ├── services/            # API service layer
│   │   └── authService.js  # Authentication & API calls
│   ├── router/              # Vue Router configuration
│   │   └── index.js        # Route definitions
│   ├── helpers/             # Utility functions
│   │   ├── constants.ts    # App constants
│   │   ├── utils.ts        # Helper functions
│   │   ├── http-client.ts  # Axios configuration
│   │   └── ...             # Other utilities
│   ├── types/               # TypeScript type definitions
│   ├── main.js              # Application entry point
│   └── App.vue              # Root component
├── index.html               # HTML template
├── vite.config.ts           # Vite configuration
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sammagafu/devangwacoaching.git
   cd devangwacoaching
   ```

2. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Environment setup:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

5. **Build for production:**
   ```bash
   npm run build
   ```

## ⚙️ Configuration

### Environment Variables

```bash
# API Configuration
VITE_API_URL=http://localhost:8000/api/v1/

# Development
VITE_APP_ENV=development

# Optional: Analytics, etc.
VITE_ANALYTICS_ID=your-analytics-id
```

### Vite Configuration

Key settings in `vite.config.ts`:
- Vue plugin configuration
- Bootstrap Vue resolver
- Path aliases (`@/` for `src/`)
- Build optimization settings

## 🎨 UI Components

### Layout Components
- **PagesLayout:** Main page wrapper with navigation
- **StudentLayout:** Student dashboard layout
- **InstructorLayout:** Instructor dashboard layout

### Feature Components
- **CourseCard:** Course display component
- **VideoPlayer:** Custom video player with Plyr
- **PaymentForm:** Secure payment form
- **ProfileDropdown:** User menu component

### Form Components
- **ChoicesSelect:** Enhanced select dropdowns
- **CustomTinySlider:** Carousel/slider component
- **ApexChart:** Data visualization charts

## 🔄 State Management

### Pinia Stores

#### Auth Store (`stores/auth.js`)
```javascript
// State
user: null
isAuthenticated: false
isStaff: false
isAdmin: false

// Actions
login(credentials, rememberMe)
register(userData)
logout()
updateRoles()
```

#### Cart Store (`stores/cart.js`)
```javascript
// State
cartItems: []
isLoading: false

// Actions
addToCart(item)
removeFromCart(itemId)
fetchCartItems()
clearCart()
```

## 🌐 Routing

### Route Structure
```javascript
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },
  {
    path: '/auth',
    children: [
      { path: 'sign-in', component: SignIn },
      { path: 'sign-up', component: SignUp }
    ]
  },
  {
    path: '/courses',
    children: [
      { path: '', component: CourseList },
      { path: ':slug', component: CourseDetail }
    ]
  },
  {
    path: '/student',
    component: StudentLayout,
    children: [
      { path: 'dashboard', component: StudentDashboard },
      { path: 'courses', component: MyCourses }
    ],
    meta: { requiresAuth: true }
  }
]
```

### Navigation Guards
- Authentication checks
- Role-based access control
- Route redirects for unauthenticated users

## 🔗 API Integration

### Service Layer

#### AuthService (`services/authService.js`)
- JWT token management
- Automatic token refresh
- Request/response interceptors
- Error handling

#### API Calls
```javascript
// Authentication
const response = await api.post('auth/jwt/create/', credentials)
const user = await api.get('auth/users/me/')

// Courses
const courses = await api.get('course/courses/')
const course = await api.get(`course/courses/${slug}/`)

// Profile
const profile = await api.get('auth/profile/')
await api.put('auth/profile/', formData)
```

### Error Handling
- Global error interceptor
- User-friendly error messages
- Automatic logout on 401 errors
- Loading states management

## 🎨 Styling

### Bootstrap Integration
- Bootstrap 5 core styles
- Bootstrap Vue Next components
- Custom SCSS variables
- Responsive breakpoints

### Custom Styles
```scss
// src/assets/scss/style.scss
@import 'bootstrap/scss/bootstrap';

// Custom variables
$primary-color: #0d6efd;
$secondary-color: #6c757d;

// Component styles
.course-card {
  border-radius: 0.5rem;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}
```

## 📱 Responsive Design

### Breakpoints
- **xs:** < 576px (mobile)
- **sm:** ≥ 576px (small tablets)
- **md:** ≥ 768px (tablets)
- **lg:** ≥ 992px (desktops)
- **xl:** ≥ 1200px (large desktops)
- **xxl:** ≥ 1400px (extra large)

### Mobile-First Approach
- Progressive enhancement
- Touch-friendly interactions
- Optimized performance on mobile devices

## 🔧 Development

### Available Scripts

```bash
# Development
npm run dev          # Start dev server
npm run preview      # Preview production build

# Building
npm run build        # Production build
npm run type-check   # TypeScript checking

# Code Quality
npm run lint         # ESLint checking
npm run format       # Prettier formatting
```

### Code Style
- **ESLint:** Vue 3 recommended rules
- **Prettier:** Consistent code formatting
- **TypeScript:** Type checking for better DX

### Component Development
```vue
<template>
  <div class="my-component">
    <h1>{{ title }}</h1>
    <button @click="handleClick">Click me</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  title: String
})

const emit = defineEmits(['custom-event'])

const handleClick = () => {
  emit('custom-event', 'button clicked')
}
</script>

<style scoped>
.my-component {
  padding: 1rem;
}
</style>
```

## 🧪 Testing

### Testing Setup
```bash
npm install -D @vue/test-utils vitest
```

### Test Structure
```
src/
├── components/
│   ├── __tests__/
│   │   └── MyComponent.test.js
├── stores/
│   ├── __tests__/
│   │   └── auth.test.js
└── services/
    ├── __tests__/
    │   └── authService.test.js
```

## 🚀 Deployment

### Build Process
```bash
# Build for production
npm run build

# Output in dist/ directory
# - index.html
# - assets/ (JS, CSS, images)
```

### Environment-Specific Builds
- Development: `npm run dev`
- Staging: `npm run build` with staging env vars
- Production: `npm run build` with production env vars

### Docker Integration
The frontend is built into the backend container:
```dockerfile
# Build frontend
COPY devangwacoaching/ ./devangwacoaching/
WORKDIR /app/devangwacoaching
RUN npm install && npm run build

# Copy built files to backend
RUN cp -r /app/devangwacoaching/dist/* /app/devangwabackend/static/
```

## 🔍 Performance

### Optimization Features
- **Vite:** Fast HMR and optimized builds
- **Code Splitting:** Automatic route-based splitting
- **Asset Optimization:** Image compression, CSS minification
- **Lazy Loading:** Component and route lazy loading
- **Caching:** Aggressive caching strategies

### Bundle Analysis
```bash
npm run build -- --mode analyze
```

## 🐛 Debugging

### Vue DevTools
- Component tree inspection
- State management debugging
- Performance monitoring
- Time travel debugging

### Browser DevTools
- Network tab for API calls
- Console for error logging
- Application tab for storage inspection

## 📚 Resources

### Official Documentation
- [Vue.js 3 Guide](https://vuejs.org/guide/introduction.html)
- [Vite Documentation](https://vitejs.dev/)
- [Pinia Guide](https://pinia.vuejs.org/)
- [Vue Router 4](https://router.vuejs.org/)

### UI Libraries
- [Bootstrap 5](https://getbootstrap.com/docs/5.0/)
- [Bootstrap Vue Next](https://bootstrap-vue-next.github.io/)
- [FontAwesome](https://fontawesome.com/)

### Development Tools
- [Vue DevTools](https://devtools.vuejs.org/)
- [Vite Plugin Vue](https://github.com/vitejs/vite-plugin-vue)

## 🤝 Contributing

1. Follow the existing code style
2. Write tests for new features
3. Update documentation
4. Create feature branches
5. Submit pull requests

## 📞 Support

For frontend-specific issues:
1. Check browser console for errors
2. Verify API endpoints are accessible
3. Test with different browsers
4. Check network tab for failed requests
5. Review Vue DevTools for component state</content>
<parameter name="filePath">/Users/codexl-008/devangwa/devangwabackend/FRONTEND_README.md