const projects = [
  {
    name: "Embedded Test Automation Platform",
    summary:
      "Pytest-driven embedded API testing with automated artifacts and docs pipeline.",
    stack: ["Python", "Pytest", "Sphinx", "Pandoc", "Confluence API"],
    impact: 14,
  },
  {
    name: "Cloud Governance Automation Suite",
    summary:
      "AWS governance checks for exposure risks, tagging compliance, and infrastructure reporting.",
    stack: ["Python", "Boto3", "AWS EC2", "CSV/JSON Reporting"],
    impact: 11,
  },
  {
    name: "Infra Self-Service Portal",
    summary:
      "Internal request API that validates infrastructure metadata and queues provisioning workflows.",
    stack: ["Python", "HTTP APIs", "TeamCity API", "Validation"],
    impact: 9,
  },
  {
    name: "Workflow Orchestration Hub",
    summary:
      "Reusable event-routing architecture for n8n and internal engineering automations.",
    stack: ["Python", "n8n", "Event Routing", "Retries/DLQ Patterns"],
    impact: 8,
  },
  {
    name: "Reddit Wallpaper Archiver (Go)",
    summary:
      "Go automation for pulling, filtering, deduplicating, and archiving wallpaper assets.",
    stack: ["Go", "Scheduling", "API Integration", "Manifest Storage"],
    impact: 6,
  },
];

const stats = [
  { value: "5", label: "Major Projects" },
  { value: "48+", label: "Estimated Hours Saved / Week" },
  { value: "4", label: "Automation Domains" },
  { value: "2", label: "Primary Languages" },
];

const skills = [
  "Pytest Automation",
  "Embedded API Testing",
  "Boto3 Automation",
  "AWS Governance",
  "CI/CD Pipeline Design",
  "TeamCity API",
  "Confluence Publishing",
  "n8n Workflow Engineering",
  "Infrastructure Reporting",
  "Go Automation Services",
  "Reliability Engineering",
  "Platform Tooling",
];

function renderStats() {
  const grid = document.getElementById("stats-grid");
  stats.forEach((item) => {
    const card = document.createElement("article");
    card.className = "stat-card";
    card.innerHTML = `<h3>${item.value}</h3><p>${item.label}</p>`;
    grid.appendChild(card);
  });
}

function renderProjects() {
  const grid = document.getElementById("project-grid");
  projects.forEach((project) => {
    const card = document.createElement("article");
    card.className = "project-card";
    const chips = project.stack.map((s) => `<span class="chip">${s}</span>`).join("");
    card.innerHTML = `
      <h3>${project.name}</h3>
      <p>${project.summary}</p>
      <div class="chip-list">${chips}</div>
    `;
    grid.appendChild(card);
  });
}

function renderTags() {
  const cloud = document.getElementById("tag-cloud");
  skills.forEach((skill) => {
    const tag = document.createElement("span");
    tag.className = "tag";
    tag.textContent = skill;
    cloud.appendChild(tag);
  });
}

function renderHoursChart() {
  const chart = document.getElementById("hours-chart");
  const width = 800;
  const height = 360;
  const padding = 48;
  const maxValue = Math.max(...projects.map((p) => p.impact));
  const barWidth = 110;
  const gap = 30;

  const axis = document.createElementNS("http://www.w3.org/2000/svg", "line");
  axis.setAttribute("x1", String(padding));
  axis.setAttribute("x2", String(width - padding));
  axis.setAttribute("y1", String(height - padding));
  axis.setAttribute("y2", String(height - padding));
  axis.setAttribute("stroke", "rgba(255,255,255,0.4)");
  chart.appendChild(axis);

  projects.forEach((project, index) => {
    const x = padding + index * (barWidth + gap) + 8;
    const scaledHeight = (project.impact / maxValue) * 220;
    const y = height - padding - scaledHeight;

    const bar = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    bar.setAttribute("x", String(x));
    bar.setAttribute("y", String(y));
    bar.setAttribute("width", String(barWidth));
    bar.setAttribute("height", String(scaledHeight));
    bar.setAttribute("rx", "10");
    bar.setAttribute("fill", "url(#bar-gradient)");
    bar.setAttribute("opacity", "0.95");
    chart.appendChild(bar);

    const value = document.createElementNS("http://www.w3.org/2000/svg", "text");
    value.setAttribute("x", String(x + barWidth / 2));
    value.setAttribute("y", String(y - 8));
    value.setAttribute("text-anchor", "middle");
    value.setAttribute("fill", "#dff7ff");
    value.setAttribute("font-size", "14");
    value.textContent = `${project.impact}h`;
    chart.appendChild(value);

    const label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", String(x + barWidth / 2));
    label.setAttribute("y", String(height - 16));
    label.setAttribute("text-anchor", "middle");
    label.setAttribute("fill", "#a9b5d4");
    label.setAttribute("font-size", "11");
    label.textContent = `P${index + 1}`;
    chart.appendChild(label);
  });

  const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
  defs.innerHTML = `
    <linearGradient id="bar-gradient" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#6cb1ff"></stop>
      <stop offset="100%" stop-color="#4fe1b4"></stop>
    </linearGradient>
  `;
  chart.appendChild(defs);
}

function renderSkillRadar() {
  const canvas = document.getElementById("skill-canvas");
  const ctx = canvas.getContext("2d");
  const labels = ["Testing", "Cloud", "Platform", "DevOps", "Docs", "Orchestration"];
  const values = [88, 85, 82, 80, 75, 84];
  const centerX = canvas.width / 2;
  const centerY = canvas.height / 2;
  const radius = 145;
  const levels = 5;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.strokeStyle = "rgba(255,255,255,0.16)";
  ctx.lineWidth = 1;

  for (let level = 1; level <= levels; level += 1) {
    const r = (radius * level) / levels;
    ctx.beginPath();
    labels.forEach((_, i) => {
      const angle = (-Math.PI / 2) + (i * 2 * Math.PI) / labels.length;
      const x = centerX + Math.cos(angle) * r;
      const y = centerY + Math.sin(angle) * r;
      if (i === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.closePath();
    ctx.stroke();
  }

  labels.forEach((label, i) => {
    const angle = (-Math.PI / 2) + (i * 2 * Math.PI) / labels.length;
    const x = centerX + Math.cos(angle) * (radius + 22);
    const y = centerY + Math.sin(angle) * (radius + 22);
    ctx.fillStyle = "#c4d1f0";
    ctx.font = "12px Inter, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(label, x, y);
  });

  ctx.beginPath();
  values.forEach((v, i) => {
    const angle = (-Math.PI / 2) + (i * 2 * Math.PI) / labels.length;
    const r = (v / 100) * radius;
    const x = centerX + Math.cos(angle) * r;
    const y = centerY + Math.sin(angle) * r;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.closePath();
  ctx.fillStyle = "rgba(89, 225, 194, 0.3)";
  ctx.strokeStyle = "#64ffd2";
  ctx.lineWidth = 2;
  ctx.fill();
  ctx.stroke();
}

renderStats();
renderProjects();
renderTags();
renderHoursChart();
renderSkillRadar();
