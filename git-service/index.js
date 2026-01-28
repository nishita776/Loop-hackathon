require("dotenv").config();
const express = require("express");
const axios = require("axios");

const app = express();
const PORT = process.env.PORT || 3000;

app.get("/", (req, res) => {
  res.send("Git service is alive");
});

const cache = {};

app.get("/git/activity/:username", async (req, res) => {
  const { username } = req.params;

  if (cache[username] && Date.now() - cache[username].time < 5 * 60 * 1000) {
    return res.json(cache[username].data);
  }

  try {
    const response = await axios.get(
      `https://api.github.com/users/${username}/events`,
      {
        headers: {
          Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
          Accept: "application/vnd.github+json"
        }
      }
    );

    const commits = [];

    response.data.forEach(event => {
      if (event.type === "PushEvent") {
        event.payload.commits.forEach(commit => {
          commits.push({
            repo: event.repo.name,
            message: commit.message,
            timestamp: event.created_at
          });
        });
      }
    });

    const data = {
  user: username,
  totalCommits: commits.length,
  commits
};

    cache[username] = {
      data,
      time: Date.now()
    };

    res.json(data);

  } catch (error) {
    console.error("⚠️ GitHub API failed:", error.message);

    const mockData = {
      user: username,
      commits: [
        {
          repo: "demo-repo",
          message: "Mock commit (GitHub API fallback)",
          timestamp: new Date().toISOString()
        }
      ]
    };

    res.json(mockData);
  }
});

app.listen(PORT, () => {
  console.log(`Git service running on port ${PORT}`);
});
