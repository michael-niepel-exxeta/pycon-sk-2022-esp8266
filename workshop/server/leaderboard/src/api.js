function fetchScores () {
    fetch('localhost:8000/leaderboard/').then((response) => {
        return response
    })
}