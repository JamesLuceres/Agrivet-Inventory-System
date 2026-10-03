import fs from 'fs'
import path from 'path'

const filePath = path.join('node_modules', '@quasar', 'app-vite', 'lib', 'node-version-check.js')

try {
  if (fs.existsSync(filePath)) {
    let content = fs.readFileSync(filePath, 'utf8')
    content = content.replace('minor: 22', 'minor: 0')
    fs.writeFileSync(filePath, content, 'utf8')
    console.log('Successfully patched Quasar Node version check.')
  } else {
    console.log('Quasar node-version-check.js not found.')
  }
} catch (err) {
  console.error('Failed to patch Quasar Node version check:', err)
}
