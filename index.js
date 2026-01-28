const express = require('express');
const app = express();

app.use(express.json());


let users = [
  { id: 'u1', name: 'Aditi', skills: ['frontend', 'react'], currentTasks: [] },
  { id: 'u2', name: 'Rahul', skills: ['backend', 'node'], currentTasks: [] },
  { id: 'u3', name: 'Neha', skills: ['ml', 'python'], currentTasks: [] }
];

let tasks = [];

app.post('/tasks/create', (req, res) => {
  const { title, requiredSkills, deadline } = req.body;

  const task = {
    id: 't' + (tasks.length + 1),
    title,
    requiredSkills,
    deadline,
    status: 'todo',
    assignedTo: null
  };

  tasks.push(task);
  res.json(task);
});

function assignTask(task) {
  let bestUser = null;
  let bestScore = -1;

  users.forEach(user => {
    const matchedSkills = user.skills.filter(skill =>
      task.requiredSkills.includes(skill)
    );

    const score = matchedSkills.length / task.requiredSkills.length;

    // First user becomes baseline
    if (!bestUser) {
      bestUser = user;
      bestScore = score;
      return;
    }

    // Better skill match wins
    if (score > bestScore) {
      bestUser = user;
      bestScore = score;
      return;
    }

    // Tie-breaker: fewer current tasks wins
    if (
      score === bestScore &&
      user.currentTasks.length < bestUser.currentTasks.length
    ) {
      bestUser = user;
    }
  });

  if (bestUser && bestScore >= 0.5) {
    task.assignedTo = bestUser.id;
    bestUser.currentTasks.push(task.id);
  }

  return {
    task,
    matchScore: bestScore
  };
}

app.post('/tasks/assign', (req, res) => {
  const { taskId } = req.body;

  const task = tasks.find(t => t.id === taskId);
  if (!task) return res.status(404).json({ error: 'Task not found' });

  const result = assignTask(task);
  res.json(result);
});

app.get('/', (req, res) => {
  res.send('Task Skill Engine is running 🚀');
});

// CREATE USER
app.post('/users/create', (req, res) => {
  const { id, name, skills } = req.body;

  if (!id || !name || !skills) {
    return res.status(400).json({ error: 'Missing fields' });
  }

  users.push({
  id,
  name,
  skills,
  currentTasks: []
});
  res.json({ message: 'User created' });
});

app.listen(3000, () => {
  console.log('Server running on http://localhost:3000');
});
