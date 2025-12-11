// Load top keywords JSON (we will create this file below)
fetch("assets/keyword_stats.json")
  .then(r => r.ok ? r.json() : Promise.reject("no keyword file"))
  .then(data => {
    const list = data.top_keywords || [];
    if(list.length === 0) {
      document.getElementById("keywords").innerText = "No keywords found.";
      return;
    }
    const html = "<ol>" + list.map(k => `<li>${k}</li>`).join("") + "</ol>";
    document.getElementById("keywords").innerHTML = html;
  })
  .catch(()=> { document.getElementById("keywords").innerText = "No keywords available"; });

// Load network stats CSV into the stats panel
fetch("assets/network_statistics.csv")
  .then(r => r.ok ? r.text() : Promise.reject("no csv"))
  .then(text => {
    const rows = text.trim().split("\n").slice(0,20).join("\n");
    document.getElementById("stats").innerText = rows;
  })
  .catch(()=> { document.getElementById("stats").innerText = "No network statistics found"; });
