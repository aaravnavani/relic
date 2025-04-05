async function exportMessages() {
    const status = document.getElementById("status");
    status.innerText = "📤 Exporting...";
  
    try {
      const result = await window.api.exportMessages();
      status.innerText = `✅ Export complete! File saved to: ${result}`;
    } catch (err) {
      status.innerText = `❌ Error: ${err}`;
    }
  }