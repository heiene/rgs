<template>
  <div class="about">
    <h1>About RGS</h1>
    <p>This is a Vue 3 + Flask application with the following architecture:</p>
    
    <div class="architecture">
      <h2>🏗️ Architecture</h2>
      <ul>
        <li><strong>Frontend:</strong> Vue 3 with Vite, Vue Router, and Pinia</li>
        <li><strong>Backend:</strong> Flask with SQLAlchemy, Marshmallow, and JWT</li>
        <li><strong>Database:</strong> PostgreSQL</li>
        <li><strong>Testing:</strong> Pytest for backend, Vitest for frontend</li>
      </ul>
    </div>
    
    <div class="principles">
      <h2>📋 Principles</h2>
      <ul>
        <li><strong>Thin Routes, Fat Services:</strong> Routes handle HTTP only, Services contain business logic</li>
        <li><strong>API-First:</strong> Frontend communicates with backend only through API routes</li>
        <li><strong>Clean Architecture:</strong> Clear separation of concerns across layers</li>
        <li><strong>Testing:</strong> Comprehensive test coverage with proper fixtures</li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: left;
}

.architecture, .principles {
  margin-top: 30px;
}

ul {
  text-align: left;
}

li {
  margin: 10px 0;
}
</style> 