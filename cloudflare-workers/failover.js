addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request))
})

const PRIMARY_URL = 'https://empire-backend.onrender.com'
const BACKUP_URLS = [
  'https://empire-backend-production.up.railway.app',
  'https://empire-os.fly.dev',
  'https://empire-os.koyeb.app'
]

async function handleRequest(request) {
  let response
  let lastError
  
  // Try primary first
  try {
    response = await fetchWithTimeout(PRIMARY_URL + request.url, {
      method: request.method,
      headers: request.headers,
      body: request.body
    }, 3000)
    
    if (response.status < 500) {
      return response
    }
  } catch (err) {
    lastError = err
  }
  
  // Try backups in order
  for (const backupUrl of BACKUP_URLS) {
    try {
      response = await fetchWithTimeout(backupUrl + request.url, {
        method: request.method,
        headers: request.headers,
        body: request.body
      }, 3000)
      
      if (response.status < 500) {
        // Log the failover
        console.log(`Failed over to ${backupUrl}`)
        return response
      }
    } catch (err) {
      lastError = err
      continue
    }
  }
  
  // All failed
  return new Response('Service unavailable', {
    status: 503,
    headers: { 'Content-Type': 'text/plain' }
  })
}

async function fetchWithTimeout(url, options, timeout) {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)
  
  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal
    })
    clearTimeout(timeoutId)
    return response
  } catch (err) {
    clearTimeout(timeoutId)
    throw err
  }
}
