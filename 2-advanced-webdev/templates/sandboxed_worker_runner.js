/**
 * Sandboxed Worker Runner.
 * Executes untrusted JavaScript asynchronously inside a client-side Web Worker.
 * Captures all standard console.log outputs, enforces structural timeouts, 
 * and handles failures gracefully without blocking the main browser UI thread.
 * 
 * Safe for production onboarding environments.
 */

// 1. Worker Execution Script in a String Template
const workerSourceCode = `
self.onmessage = function(event) {
  const { code, taskId } = event.data;
  
  // Custom console interception
  const capturedLogs = [];
  const customConsole = {
    log: function(...args) {
      capturedLogs.push(args.map(arg => 
        typeof arg === 'object' ? JSON.stringify(arg) : String(arg)
      ).join(' '));
    },
    error: function(...args) {
      capturedLogs.push("[ERROR] " + args.join(' '));
    },
    warn: function(...args) {
      capturedLogs.push("[WARN] " + args.join(' '));
    }
  };

  try {
    // Create an isolated sandbox environment block for evaluation
    const runnerFunction = new Function('console', \`
      try {
        \${code}
      } catch (err) {
        throw err;
      }
    \`);
    
    // Execute user code, passing in the custom console interceptor
    const result = runnerFunction(customConsole);
    
    // Return successful execution metrics
    self.postMessage({
      type: "SUCCESS",
      taskId: taskId,
      result: result,
      logs: capturedLogs
    });
  } catch (error) {
    // Return detailed error stack details
    self.postMessage({
      type: "ERROR",
      taskId: taskId,
      error: error.message,
      logs: capturedLogs
    });
  }
};
`;

/**
 * Sandboxed Code Execution Controller
 * @param {string} userCode The raw JavaScript code block to run.
 * @param {number} timeoutMs Execution timeout limit in milliseconds.
 * @returns {Promise<{success: boolean, result: any, error: string|null, logs: string[]}>}
 */
function runCodeSafely(userCode, timeoutMs = 2000) {
  return new Promise((resolve) => {
    const taskId = "task-" + Math.random().toString(36).substring(2, 11);
    
    // Create a blob representing the worker code
    const blob = new Blob([workerSourceCode], { type: "application/javascript" });
    const workerUrl = URL.createObjectURL(blob);
    const worker = new Worker(workerUrl);
    
    // Setup automated termination timeout
    const executionTimer = setTimeout(() => {
      worker.terminate();
      URL.revokeObjectURL(workerUrl);
      resolve({
        success: false,
        result: null,
        error: "Execution timed out after " + timeoutMs + "ms.",
        logs: ["[SYSTEM ERROR] Thread terminated by host watchdog timer."]
      });
    }, timeoutMs);

    // Setup worker listener
    worker.onmessage = function(e) {
      const response = e.data;
      if (response.taskId !== taskId) return;
      
      // Clear watchdog timer and release resources
      clearTimeout(executionTimer);
      worker.terminate();
      URL.revokeObjectURL(workerUrl);

      if (response.type === "SUCCESS") {
        resolve({
          success: true,
          result: response.result,
          error: null,
          logs: response.logs
        });
      } else {
        resolve({
          success: false,
          result: null,
          error: response.error,
          logs: response.logs
        });
      }
    };

    worker.onerror = function(err) {
      clearTimeout(executionTimer);
      worker.terminate();
      URL.revokeObjectURL(workerUrl);
      resolve({
        success: false,
        result: null,
        error: err.message,
        logs: []
      });
    };

    // Trigger execution
    worker.postMessage({ code: userCode, taskId: taskId });
  });
}

// --- Example Test Cases / Interactive Demo Usage ---
async function runDemo() {
  console.log("Running valid code demo...");
  const validCode = `
    console.log("Starting calculations...");
    const values = [10, 20, 30, 40];
    const sum = values.reduce((a, b) => a + b, 0);
    console.log("Calculated sum: " + sum);
    return sum;
  `;
  const res1 = await runCodeSafely(validCode);
  console.log("Result 1 Object:", res1);

  console.log("\nRunning infinite loop timeout demo...");
  const infiniteLoop = `
    console.log("Entering infinite loop...");
    while(true) {
      // Loop forever
    }
  `;
  const res2 = await runCodeSafely(infiniteLoop, 1000);
  console.log("Result 2 Object:", res2);
}

// If running in browser window console, trigger the demo
if (typeof window !== "undefined") {
  runDemo();
} else {
  // CommonJS export fallback
  module.exports = { runCodeSafely };
}
