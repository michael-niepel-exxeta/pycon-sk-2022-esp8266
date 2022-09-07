const API_ROOT = process.env.REACT_APP_API_ROOT;

const fetchScores = async () => {
  const res = await fetch(`${API_ROOT}/leaderboard/`);
  return res.json();
};

const fetchLastScores = async () => {
  const res = await fetch(`${API_ROOT}/leaderboard/?by_id=true&skip=0&limit=1`);
  return res.json();
};

const updateScore = async (data) => {
  console.log(data);
  const response = await fetch(`${API_ROOT}/leaderboard/${data.id}`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return response.json();
};

export {
    fetchScores, fetchLastScores, updateScore
}