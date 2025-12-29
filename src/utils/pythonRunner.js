let pyodide = null
let loading = false

async function loadPyodide() {
  if (pyodide) {
    return pyodide
  }
  
  if (loading) {
    // 等待加载完成
    while (loading) {
      await new Promise(resolve => setTimeout(resolve, 100))
    }
    return pyodide
  }
  
  loading = true
  try {
    // 从 CDN 动态加载 Pyodide（避免打包问题）
    if (typeof window !== 'undefined' && !window.loadPyodide) {
      // 检查是否已经加载了脚本
      if (!document.querySelector('script[src*="pyodide"]')) {
        // 动态加载 Pyodide 脚本
        await new Promise((resolve, reject) => {
          const script = document.createElement('script')
          script.src = 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js'
          script.onload = resolve
          script.onerror = () => reject(new Error('Failed to load Pyodide script'))
          document.head.appendChild(script)
        })
        
        // 等待 loadPyodide 函数可用
        let retries = 0
        while (!window.loadPyodide && retries < 50) {
          await new Promise(resolve => setTimeout(resolve, 100))
          retries++
        }
        
        if (!window.loadPyodide) {
          throw new Error('Pyodide failed to initialize')
        }
      }
    }
    
    // 使用全局的 loadPyodide 函数
    const loadPyodideModule = window.loadPyodide
    if (!loadPyodideModule) {
      throw new Error('loadPyodide function not found')
    }
    
    pyodide = await loadPyodideModule({
      indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.24.1/full/'
    })
    return pyodide
  } catch (error) {
    console.error('加载 Pyodide 失败:', error)
    throw error
  } finally {
    loading = false
  }
}

export async function runPythonCode(code) {
  try {
    const pyodideInstance = await loadPyodide()
    
    // 捕获输出
    let output = ''
    pyodideInstance.setStdout({
      write: (text) => {
        output += text
      }
    })
    
    pyodideInstance.setStderr({
      write: (text) => {
        output += text
      }
    })
    
    // 运行代码
    try {
      await pyodideInstance.runPythonAsync(code)
      return {
        output: output.trim() || '(代码执行成功，无输出)',
        error: null
      }
    } catch (error) {
      return {
        output: output.trim(),
        error: error.message || String(error)
      }
    }
  } catch (error) {
    return {
      output: '',
      error: `无法运行代码: ${error.message}`
    }
  }
}

